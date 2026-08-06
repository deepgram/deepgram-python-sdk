"""
Additional targeted branch coverage for ``core`` internals that the broad
endpoint/utility tests do not reach: debug logging, the ``Logger`` helper,
Retry-After date / X-RateLimit-Reset header parsing, and a few remaining
encoder/serialization/construct_type shapes.
"""

import datetime as dt
import decimal
import email.utils
import time
import typing

import httpx
import pytest
import respx
import typing_extensions

import deepgram.core.http_client as http_client_module
from deepgram import DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.jsonable_encoder import jsonable_encoder
from deepgram.core.logging import ConsoleLogger, Logger, create_logger
from deepgram.core.pydantic_utilities import UniversalBaseModel
from deepgram.core.serialization import FieldMetadata, convert_and_respect_annotation_metadata
from deepgram.core.unchecked_base_model import UncheckedBaseModel, construct_type
from deepgram.environment import DeepgramClientEnvironment

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


# --------------------------------------------------------------------------- #
# Logger
# --------------------------------------------------------------------------- #
def test_logger_levels() -> None:
    logger = Logger(level="debug", logger=ConsoleLogger(), silent=False)
    assert logger.is_debug() and logger.is_info() and logger.is_warn() and logger.is_error()
    logger.debug("d")
    logger.info("i")
    logger.warn("w")
    logger.error("e")

    silent = Logger(level="error", logger=ConsoleLogger(), silent=True)
    assert silent.is_debug() is False
    silent.debug("nope")  # suppressed

    # create_logger passthrough + dict config
    assert create_logger(logger) is logger
    assert create_logger(None) is not None
    assert create_logger({"level": "warn", "silent": False}).is_warn()


def test_debug_logging_request_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(http_client_module.time, "sleep", lambda _s: None)
    client = DeepgramClient(
        environment=_environment(), api_key="secret-key", logging={"level": "debug", "silent": False}
    )
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        assert client.manage.v1.projects.list() is not None


# --------------------------------------------------------------------------- #
# Retry-After / X-RateLimit-Reset header parsing
# --------------------------------------------------------------------------- #
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(http_client_module.time, "sleep", lambda _s: None)


def test_retry_after_http_date(monkeypatch: pytest.MonkeyPatch) -> None:
    _no_sleep(monkeypatch)
    future = email.utils.formatdate(time.time() + 30, usegmt=True)
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(503, headers={"retry-after": future}, json={}))
        with pytest.raises(ApiError):
            DeepgramClient(environment=_environment(), api_key="k").manage.v1.projects.list(
                request_options={"max_retries": 1}
            )


def test_x_ratelimit_reset_future(monkeypatch: pytest.MonkeyPatch) -> None:
    _no_sleep(monkeypatch)
    reset = str(int(time.time()) + 30)
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(503, headers={"x-ratelimit-reset": reset}, json={}))
        with pytest.raises(ApiError):
            DeepgramClient(environment=_environment(), api_key="k").manage.v1.projects.list(
                request_options={"max_retries": 1}
            )


# --------------------------------------------------------------------------- #
# jsonable_encoder fallback / root model
# --------------------------------------------------------------------------- #
def test_jsonable_encoder_decimal_and_root_model() -> None:
    # Decimal is not handled inline; it goes through the jsonable fallback.
    assert jsonable_encoder(decimal.Decimal("1.5")) in (1.5, "1.5")

    # A mapping-like object reduced via dict() in the fallback path.
    class MappingLike:
        def keys(self) -> typing.List[str]:
            return ["a"]

        def __getitem__(self, key: str) -> int:
            return 1

    assert jsonable_encoder(MappingLike()) == {"a": 1}


# --------------------------------------------------------------------------- #
# serialization: set conversion + alias on a model field
# --------------------------------------------------------------------------- #
def test_serialization_set_conversion() -> None:
    class TD(typing_extensions.TypedDict):
        field: typing_extensions.Annotated[str, FieldMetadata(alias="field_name")]

    set_ann = typing.Set[str]
    # Sets pass through unchanged (no alias inside), exercising the set branch.
    out = convert_and_respect_annotation_metadata(object_={"a", "b"}, annotation=set_ann, direction="write")
    assert out == {"a", "b"}

    list_of_td = typing.List[TD]
    converted = convert_and_respect_annotation_metadata(
        object_=[{"field": "v"}], annotation=list_of_td, direction="read"
    )
    assert converted == [{"field": "v"}]


# --------------------------------------------------------------------------- #
# construct_type extra shapes
# --------------------------------------------------------------------------- #
def test_construct_type_set_of_models_and_datetime_passthrough() -> None:
    class Tag(UncheckedBaseModel):
        name: typing.Optional[str] = None

    out = construct_type(type_=typing.List[Tag], object_=[{"name": "x"}, {"name": "y"}])
    assert all(isinstance(t, Tag) for t in out)

    # datetime field that fails to parse falls back to the raw value
    assert construct_type(type_=dt.datetime, object_="not-a-date") == "not-a-date"
    assert construct_type(type_=dt.date, object_="not-a-date") == "not-a-date"


def test_construct_type_model_with_pydantic_alias_and_extras() -> None:
    import pydantic

    class Aliased(UncheckedBaseModel):
        field_name: str = pydantic.Field(alias="fieldName")

    # Supply the alias key plus an unexpected extra key to exercise the alias
    # resolution and extras-passthrough branches of UncheckedBaseModel.construct.
    built = construct_type(type_=Aliased, object_={"fieldName": "v", "surprise": 1})
    assert built.field_name == "v"


# --------------------------------------------------------------------------- #
# query_encoder: pydantic model values
# --------------------------------------------------------------------------- #
def test_query_encoder_with_pydantic_models() -> None:
    from deepgram.core.query_encoder import single_query_encoder

    class QModel(UniversalBaseModel):
        a: int = 1

    assert single_query_encoder("k", QModel(a=2)) == [("k[a]", 2)]
    assert single_query_encoder("k", [QModel(a=3)]) == [("k[a]", 3)]


# --------------------------------------------------------------------------- #
# http_client: timeout option + retry exhaustion details
# --------------------------------------------------------------------------- #
def test_request_with_timeout_option(monkeypatch: pytest.MonkeyPatch) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        client = DeepgramClient(environment=_environment(), api_key="k")
        assert client.manage.v1.projects.list(request_options={"timeout_in_seconds": 5}) is not None


def test_x_ratelimit_reset_in_past_falls_back(monkeypatch: pytest.MonkeyPatch) -> None:
    _no_sleep(monkeypatch)
    past = str(int(time.time()) - 100)
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(500, headers={"x-ratelimit-reset": past}, json={}))
        with pytest.raises(ApiError):
            DeepgramClient(environment=_environment(), api_key="k").manage.v1.projects.list(
                request_options={"max_retries": 1}
            )


async def test_async_request_with_timeout_option() -> None:
    from deepgram import AsyncDeepgramClient

    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        client = AsyncDeepgramClient(environment=_environment(), api_key="k", httpx_client=httpx.AsyncClient())
        assert await client.manage.v1.projects.list(request_options={"timeout_in_seconds": 5}) is not None


async def test_async_connect_error_exhausts(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _async_sleep(_s: float) -> None:
        return None

    monkeypatch.setattr(http_client_module.asyncio, "sleep", _async_sleep)
    from deepgram import AsyncDeepgramClient

    client = AsyncDeepgramClient(environment=_environment(), api_key="k", httpx_client=httpx.AsyncClient())
    with respx.mock:
        respx.route(host=HOST).mock(side_effect=httpx.ConnectError("boom"))
        with pytest.raises(httpx.ConnectError):
            await client.manage.v1.projects.list(request_options={"max_retries": 1})
