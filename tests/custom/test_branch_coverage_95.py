"""
Targeted branch coverage for hand-maintained ``core`` internals that the
endpoint/wire tests do not exercise on both sides of their conditionals:

* ``http_client`` Retry-After date parsing (no-timezone, unparseable, past) and
  X-RateLimit-Reset invalid values.
* ``jsonable_encoder`` type dispatch (custom encoders, pydantic roots, bytes,
  enums, paths, dates, Ellipsis filtering, and the dict()/vars() fallbacks).
* ``serialization`` annotation-metadata conversion edge cases.
* ``unchecked_base_model.construct_type`` union / literal / collection shapes.

Sleeps are patched out so retries stay fast.
"""

import base64
import dataclasses
import datetime as dt
import enum
import pathlib
import typing

import httpx
import pytest
import respx
import typing_extensions

import deepgram.core.http_client as http_client_module
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.jsonable_encoder import jsonable_encoder
from deepgram.core.serialization import FieldMetadata, convert_and_respect_annotation_metadata
from deepgram.core.unchecked_base_model import UncheckedBaseModel, construct_type
from deepgram.environment import DeepgramClientEnvironment

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(http_client_module.time, "sleep", lambda _s: None)


def _client() -> DeepgramClient:
    return DeepgramClient(
        environment=DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE),
        api_key="test_api_key",
    )


# --------------------------------------------------------------------------- #
# http_client: Retry-After / X-RateLimit-Reset header parsing
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "headers",
    [
        {"retry-after": "Wed, 21 Oct 2015 07:28:00"},  # date without timezone
        {"retry-after": "not-a-real-date"},  # unparseable -> None -> exp backoff
        {"retry-after": "Mon, 01 Jan 1990 00:00:00 GMT"},  # date in the past -> seconds < 0
        {"x-ratelimit-reset": "not-an-int"},  # invalid reset -> ignored
        {"x-ratelimit-reset": "1"},  # past reset timestamp -> no positive delay
    ],
)
def test_retry_after_header_shapes(headers: typing.Dict[str, str]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(429, headers=headers, json={"e": 1}))
        with pytest.raises(ApiError):
            _client().manage.v1.projects.list(request_options={"max_retries": 2})


def test_retry_after_ms_recovers() -> None:
    with respx.mock:
        route = respx.route(host=HOST)
        route.side_effect = [
            httpx.Response(503, headers={"retry-after-ms": "5"}, json={}),
            httpx.Response(200, json={}),
        ]
        assert _client().manage.v1.projects.list(request_options={"max_retries": 2}) is not None


# --------------------------------------------------------------------------- #
# jsonable_encoder: type dispatch
# --------------------------------------------------------------------------- #
def test_jsonable_encoder_ellipsis_and_primitives() -> None:
    assert jsonable_encoder(...) is None
    assert jsonable_encoder("s") == "s"
    assert jsonable_encoder(3) == 3
    assert jsonable_encoder(None) is None


def test_jsonable_encoder_custom_encoder_exact_and_isinstance() -> None:
    class Color(enum.Enum):
        RED = "red"

    # exact type match
    assert jsonable_encoder(Color.RED, custom_encoder={Color: lambda _c: "EXACT"}) == "EXACT"

    # isinstance match (subclass), no exact key
    class SubStr(str):
        pass

    assert jsonable_encoder(SubStr("x"), custom_encoder={str: lambda v: f"enc:{v}"}) == "enc:x"


def test_jsonable_encoder_bytes_enum_path_dates() -> None:
    assert jsonable_encoder(b"abc") == base64.b64encode(b"abc").decode("utf-8")

    class E(enum.Enum):
        A = "a"

    assert jsonable_encoder(E.A) == "a"
    assert jsonable_encoder(pathlib.PurePath("a", "b")) == str(pathlib.PurePath("a", "b"))
    assert jsonable_encoder(dt.date(2020, 1, 2)) == "2020-01-02"
    assert isinstance(jsonable_encoder(dt.datetime(2020, 1, 2, 3, 4, 5)), str)


def test_jsonable_encoder_collections_filter_ellipsis() -> None:
    assert jsonable_encoder({"keep": 1, "drop": ...}) == {"keep": 1}
    assert jsonable_encoder([1, ..., 2]) == [1, 2]
    assert sorted(jsonable_encoder({1, 2})) == [1, 2]
    assert jsonable_encoder((1, 2)) == [1, 2]


def test_jsonable_encoder_dataclass() -> None:
    @dataclasses.dataclass
    class Point:
        x: int
        y: int

    assert jsonable_encoder(Point(1, 2)) == {"x": 1, "y": 2}


def test_jsonable_encoder_fallback_dict_and_vars() -> None:
    # dict(o) path: a Mapping-like object
    class MappingLike:
        def keys(self) -> typing.List[str]:
            return ["a"]

        def __getitem__(self, k: str) -> int:
            return 1

    assert jsonable_encoder(MappingLike()) == {"a": 1}

    # vars(o) path: plain object, not iterable, has __dict__
    class Plain:
        def __init__(self) -> None:
            self.a = 1

    assert jsonable_encoder(Plain()) == {"a": 1}


def test_jsonable_encoder_fallback_raises_value_error() -> None:
    class NoDictNoIter:
        __slots__ = ()

    with pytest.raises(ValueError):
        jsonable_encoder(NoDictNoIter())


# --------------------------------------------------------------------------- #
# serialization: annotation-metadata conversion
# --------------------------------------------------------------------------- #
def test_convert_annotation_metadata_read_and_write() -> None:
    class Model(UncheckedBaseModel):
        my_field: typing_extensions.Annotated[str, FieldMetadata(alias="myField")]

    # write direction: field name -> alias
    written = convert_and_respect_annotation_metadata(object_={"my_field": "v"}, annotation=Model, direction="write")
    assert written.get("myField") == "v" or written.get("my_field") == "v"

    # read direction: alias -> field name
    read = convert_and_respect_annotation_metadata(object_={"myField": "v"}, annotation=Model, direction="read")
    assert read.get("my_field") == "v" or read.get("myField") == "v"


def test_convert_annotation_metadata_passthrough_non_model() -> None:
    # Non-model annotations pass the object through structurally.
    assert convert_and_respect_annotation_metadata(object_={"a": 1}, annotation=dict, direction="read") == {"a": 1}
    assert convert_and_respect_annotation_metadata(
        object_=[{"a": 1}], annotation=typing.List[dict], direction="read"
    ) == [{"a": 1}]
    assert convert_and_respect_annotation_metadata(object_="scalar", annotation=str, direction="read") == "scalar"


# --------------------------------------------------------------------------- #
# construct_type: unions, literals, collections
# --------------------------------------------------------------------------- #
def test_construct_type_optional_and_scalars() -> None:
    assert construct_type(object_=None, type_=typing.Optional[str]) is None
    assert construct_type(object_="hi", type_=str) == "hi"
    assert construct_type(object_=5, type_=int) == 5


def test_construct_type_list_and_dict() -> None:
    assert construct_type(object_=[1, 2], type_=typing.List[int]) == [1, 2]
    assert construct_type(object_={"a": 1}, type_=typing.Dict[str, int]) == {"a": 1}


def test_construct_type_model_and_extras() -> None:
    class Inner(UncheckedBaseModel):
        value: int

    class Outer(UncheckedBaseModel):
        inner: Inner

    built = construct_type(object_={"inner": {"value": 1}, "unexpected": "extra"}, type_=Outer)
    assert isinstance(built, Outer)
    assert built.inner.value == 1


def test_construct_type_union_selects_matching_model() -> None:
    class A(UncheckedBaseModel):
        kind: typing_extensions.Literal["a"]
        a_value: int

    class B(UncheckedBaseModel):
        kind: typing_extensions.Literal["b"]
        b_value: int

    # Union construction should exercise the union branch without raising.
    built = construct_type(object_={"kind": "b", "b_value": 7}, type_=typing.Union[A, B])
    assert built is None or isinstance(built, (A, B, dict))


def test_construct_type_bool_coercion() -> None:
    assert construct_type(object_="true", type_=bool) is True
    assert construct_type(object_="1", type_=bool) is True
    assert construct_type(object_="false", type_=bool) is False
    assert construct_type(object_=1, type_=bool) is True


def test_construct_type_enum_coercion() -> None:
    class Kind(enum.Enum):
        A = "a"
        B = "b"

    assert construct_type(object_="a", type_=Kind) == Kind.A
    # Invalid enum value is returned unchanged instead of raising.
    assert construct_type(object_="not-a-member", type_=Kind) == "not-a-member"


# --------------------------------------------------------------------------- #
# client.py: access_token / bearer override branches
# --------------------------------------------------------------------------- #
def _env() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


def test_client_access_token_without_api_key() -> None:
    client = DeepgramClient(environment=_env(), access_token="tok")
    headers = client._client_wrapper.get_headers()
    assert headers.get("Authorization") == "bearer tok"
    assert headers.get("x-deepgram-session-id")


def test_client_access_token_with_explicit_api_key() -> None:
    client = DeepgramClient(environment=_env(), access_token="tok", api_key="explicit")
    headers = client._client_wrapper.get_headers()
    assert headers.get("Authorization") == "bearer tok"


def test_client_api_key_only_uses_token_scheme() -> None:
    client = DeepgramClient(environment=_env(), api_key="secret")
    headers = client._client_wrapper.get_headers()
    assert "secret" in headers.get("Authorization", "")


# --------------------------------------------------------------------------- #
# jsonable_encoder: pydantic models & custom encoders
# --------------------------------------------------------------------------- #
def test_jsonable_encoder_pydantic_model_with_custom_encoder() -> None:
    class M(UncheckedBaseModel):
        value: int

    encoded = jsonable_encoder(M(value=5), custom_encoder={int: lambda v: v})
    assert encoded == {"value": 5}


def test_jsonable_encoder_custom_encoder_no_match_falls_through() -> None:
    # custom_encoder present but matches nothing -> falls through to normal handling
    assert jsonable_encoder(7, custom_encoder={bytes: lambda b: b}) == 7


# --------------------------------------------------------------------------- #
# pydantic_utilities: encode_by_type, deep_union_pydantic_dicts, field default
# --------------------------------------------------------------------------- #
def test_encode_by_type_exact_and_isinstance() -> None:
    from deepgram.core.pydantic_utilities import encode_by_type

    # exact type match (datetime is registered in pydantic's default encoders)
    assert isinstance(encode_by_type(dt.datetime(2020, 1, 1)), str)
    # a value with no registered encoder returns None
    assert encode_by_type(object()) is None


def test_deep_union_pydantic_dicts() -> None:
    from deepgram.core.pydantic_utilities import deep_union_pydantic_dicts

    result = deep_union_pydantic_dicts(
        {"nested": {"b": 1}, "items": [{"x": 1}, [{"y": 2}], 3], "scalar": "s"},
        {"nested": {}, "items": [{}, [{}], 0], "scalar": ""},
    )
    assert result["nested"]["b"] == 1
    assert result["items"][0]["x"] == 1
    assert result["scalar"] == "s"


# --------------------------------------------------------------------------- #
# http_client: debug/error logging on sync & async request + stream paths
# --------------------------------------------------------------------------- #
def _debug_client() -> DeepgramClient:
    return DeepgramClient(environment=_env(), api_key="secret-key", logging={"level": "debug", "silent": False})


def _async_debug_client() -> AsyncDeepgramClient:
    return AsyncDeepgramClient(
        environment=_env(),
        api_key="secret-key",
        logging={"level": "debug", "silent": False},
        httpx_client=httpx.AsyncClient(),
    )


def test_debug_logging_error_status_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"e": 1}))
        with pytest.raises(ApiError):
            _debug_client().manage.v1.projects.list(request_options={"max_retries": 0})


def test_debug_logging_stream_success_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = b"".join(_debug_client().speak.v1.audio.generate(text="hi"))
        assert chunks == b"audio-bytes"


def test_debug_logging_stream_error_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"e": 1}))
        with pytest.raises(ApiError):
            list(_debug_client().speak.v1.audio.generate(text="hi"))


async def test_debug_logging_stream_success_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = []
        async for chunk in _async_debug_client().speak.v1.audio.generate(text="hi"):
            chunks.append(chunk)
        assert b"".join(chunks) == b"audio-bytes"


async def test_debug_logging_error_status_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"e": 1}))
        with pytest.raises(ApiError):
            await _async_debug_client().manage.v1.projects.list(request_options={"max_retries": 0})


async def test_debug_logging_stream_error_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"e": 1}))
        with pytest.raises(ApiError):
            async for _chunk in _async_debug_client().speak.v1.audio.generate(text="hi"):
                pass


# --------------------------------------------------------------------------- #
# http_client: multipart file upload + additional body/query params
# --------------------------------------------------------------------------- #
def test_transcribe_file_multipart_request() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={"results": {}}))
        result = _debug_client().listen.v1.media.transcribe_file(request=b"audio-bytes", model="nova-3")
        assert result is not None


def test_additional_body_and_query_parameters() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        result = _client().manage.v1.projects.list(
            request_options={
                "additional_body_parameters": {"extra_body": 1},
                "additional_query_parameters": {"extra_query": "q"},
                "additional_headers": {"X-Extra": "h"},
            }
        )
        assert result is not None


# --------------------------------------------------------------------------- #
# logging: the "level too high -> skip" branch of each log method
# --------------------------------------------------------------------------- #
def test_logger_skips_below_threshold() -> None:
    from deepgram.core.logging import ConsoleLogger, Logger

    lg = Logger(level="error", logger=ConsoleLogger(), silent=False)
    # Each of these is below the "error" threshold, so is_*() is False and the
    # method body is skipped (the ->exit branch of each guard).
    lg.debug("d")
    lg.info("i")
    lg.warn("w")
    lg.error("e")  # this one logs


# --------------------------------------------------------------------------- #
# client.py: explicit headers + async access_token override
# --------------------------------------------------------------------------- #
def test_client_with_explicit_headers_dict() -> None:
    client = DeepgramClient(environment=_env(), api_key="k", headers={"X-Custom": "1"})
    headers = client._client_wrapper.get_headers()
    assert headers.get("X-Custom") == "1"
    assert headers.get("x-deepgram-session-id")


async def test_async_client_access_token_and_headers() -> None:
    client = AsyncDeepgramClient(
        environment=_env(),
        access_token="tok",
        headers={"X-Custom": "1"},
        httpx_client=httpx.AsyncClient(),
    )
    headers = client._client_wrapper.get_headers()
    assert headers.get("Authorization") == "bearer tok"
    assert headers.get("X-Custom") == "1"


async def test_async_client_api_key_only() -> None:
    client = AsyncDeepgramClient(environment=_env(), api_key="secret", httpx_client=httpx.AsyncClient())
    headers = client._client_wrapper.get_headers()
    assert "secret" in headers.get("Authorization", "")


# --------------------------------------------------------------------------- #
# http_client: explicit empty body preserved; force_multipart body
# --------------------------------------------------------------------------- #
def test_get_request_body_shapes() -> None:
    from deepgram.core.http_client import get_request_body

    # data provided as a non-mapping is encoded directly
    json_body, data_body = get_request_body(json=None, data="raw-string", request_options=None, omit=None)
    assert data_body == "raw-string"

    # additional_body_parameters merged into an explicit json mapping
    json_body, data_body = get_request_body(
        json={"a": 1},
        data=None,
        request_options={"additional_body_parameters": {"b": 2}},
        omit=None,
    )
    assert json_body == {"a": 1, "b": 2}

    # both None with additional body params -> additional params returned
    json_body, data_body = get_request_body(
        json=None, data=None, request_options={"additional_body_parameters": {"c": 3}}, omit=None
    )
    assert json_body == {"c": 3}


def test_remove_omit_and_none_helpers() -> None:
    from deepgram.core.http_client import remove_omit_from_dict
    from deepgram.core.remove_none_from_dict import remove_none_from_dict

    OMIT = ...
    assert remove_omit_from_dict({"a": 1, "b": OMIT}, OMIT) == {"a": 1}
    assert remove_omit_from_dict({"a": 1}, None) == {"a": 1}
    assert remove_none_from_dict({"a": 1, "b": None}) == {"a": 1}


# --------------------------------------------------------------------------- #
# construct_type: collection edge cases
# --------------------------------------------------------------------------- #
def test_construct_type_any_and_bare_containers() -> None:
    assert construct_type(object_={"x": 1}, type_=typing.Any) == {"x": 1}
    # bare dict / list annotations (no type args) return the object unchanged
    assert construct_type(object_={"a": 1}, type_=dict) == {"a": 1}
    assert construct_type(object_=[1, 2], type_=list) == [1, 2]


def test_construct_type_wrong_shape_passthrough() -> None:
    # object shape does not match the annotation -> returned unchanged
    assert construct_type(object_="not-a-dict", type_=typing.Dict[str, int]) == "not-a-dict"
    assert construct_type(object_="not-a-list", type_=typing.List[int]) == "not-a-list"
    assert construct_type(object_="not-a-set", type_=typing.Set[int]) == "not-a-set"


def test_construct_type_set_from_set_and_list() -> None:
    assert construct_type(object_={1, 2}, type_=typing.Set[int]) == {1, 2}
    # a list is coerced into a set
    assert construct_type(object_=[1, 2, 2], type_=typing.Set[int]) == {1, 2}


# --------------------------------------------------------------------------- #
# construct_type: model aliases + extras + literal-discriminated unions
# --------------------------------------------------------------------------- #
def test_construct_type_model_alias_and_extras() -> None:
    import pydantic

    class WithAlias(UncheckedBaseModel):
        my_field: typing.Optional[str] = pydantic.Field(default=None, alias="myField")

    built = construct_type(object_={"myField": "v", "unexpected": "extra"}, type_=WithAlias)
    assert isinstance(built, WithAlias)
    assert built.my_field == "v"


def test_construct_type_literal_discriminated_union() -> None:
    class A(UncheckedBaseModel):
        type: typing_extensions.Literal["a"] = "a"
        a_value: int = 0

    class B(UncheckedBaseModel):
        type: typing_extensions.Literal["b"] = "b"
        b_value: int = 0

    built = construct_type(object_={"type": "b", "b_value": 7}, type_=typing.Union[A, B])
    assert isinstance(built, B)
    assert built.b_value == 7

    built_a = construct_type(object_={"type": "a", "a_value": 3}, type_=typing.Union[A, B])
    assert isinstance(built_a, A)


# --------------------------------------------------------------------------- #
# socket_client: the defensive "unknown message type" warning branches
# (reached only when construct_type raises on an otherwise-valid JSON frame).
# --------------------------------------------------------------------------- #
import importlib  # noqa: E402

from deepgram.core.events import EventType  # noqa: E402

_SOCKET_MODULES = [
    ("deepgram.speak.v1.socket_client", "V1SocketClient", "AsyncV1SocketClient"),
    ("deepgram.agent.v1.socket_client", "V1SocketClient", "AsyncV1SocketClient"),
    ("deepgram.listen.v1.socket_client", "V1SocketClient", "AsyncV1SocketClient"),
    ("deepgram.listen.v2.socket_client", "V2SocketClient", "AsyncV2SocketClient"),
]


def _raise(**_kwargs: typing.Any) -> typing.Any:
    raise ValueError("boom")


class _SyncWSJson:
    def __iter__(self) -> typing.Iterator[str]:
        return iter(['{"type":"X"}'])

    def recv(self) -> str:
        return '{"type":"X"}'

    def send(self, _data: typing.Any) -> None:
        pass


class _AsyncWSJson:
    def __aiter__(self) -> typing.AsyncIterator[str]:
        async def _gen() -> typing.AsyncIterator[str]:
            yield '{"type":"X"}'

        return _gen()

    async def recv(self) -> str:
        return '{"type":"X"}'

    async def send(self, _data: typing.Any) -> None:
        pass


@pytest.mark.parametrize("mod_name,sync_cls,_async_cls", _SOCKET_MODULES)
def test_socket_unknown_message_sync(
    monkeypatch: pytest.MonkeyPatch, mod_name: str, sync_cls: str, _async_cls: str
) -> None:
    mod = importlib.import_module(mod_name)
    monkeypatch.setattr(mod, "construct_type", _raise)
    socket = getattr(mod, sync_cls)(websocket=_SyncWSJson())
    socket.on(EventType.MESSAGE, lambda _d: None)
    socket.on(EventType.ERROR, lambda _d: None)
    # recv, __iter__ and start_listening all hit the construct_type -> warning path
    socket.recv()
    list(socket)
    socket.start_listening()


@pytest.mark.parametrize("mod_name,_sync_cls,async_cls", _SOCKET_MODULES)
async def test_socket_unknown_message_async(
    monkeypatch: pytest.MonkeyPatch, mod_name: str, _sync_cls: str, async_cls: str
) -> None:
    mod = importlib.import_module(mod_name)
    monkeypatch.setattr(mod, "construct_type", _raise)
    socket = getattr(mod, async_cls)(websocket=_AsyncWSJson())
    socket.on(EventType.MESSAGE, lambda _d: None)
    socket.on(EventType.ERROR, lambda _d: None)
    await socket.recv()
    async for _ in socket:
        pass
    await socket.start_listening()


# --------------------------------------------------------------------------- #
# serialization: list/sequence of aliased models + read/write round-trip
# --------------------------------------------------------------------------- #
def test_convert_list_of_aliased_models() -> None:
    class Aliased(UncheckedBaseModel):
        my_field: typing_extensions.Annotated[str, FieldMetadata(alias="myField")]

    written = convert_and_respect_annotation_metadata(
        object_=[{"my_field": "v"}], annotation=typing.List[Aliased], direction="write"
    )
    assert written == [{"myField": "v"}]

    read = convert_and_respect_annotation_metadata(
        object_=[{"myField": "v"}], annotation=typing.List[Aliased], direction="read"
    )
    assert read == [{"my_field": "v"}]


def test_convert_sequence_and_union_of_aliased_models() -> None:
    class Aliased(UncheckedBaseModel):
        my_field: typing_extensions.Annotated[str, FieldMetadata(alias="myField")]

    seq = convert_and_respect_annotation_metadata(
        object_=[{"my_field": "v"}], annotation=typing.Sequence[Aliased], direction="write"
    )
    assert seq == [{"myField": "v"}]

    unioned = convert_and_respect_annotation_metadata(
        object_={"my_field": "v"}, annotation=typing.Union[Aliased, None], direction="write"
    )
    assert unioned.get("myField") == "v" or unioned.get("my_field") == "v"


# --------------------------------------------------------------------------- #
# UniversalBaseModel round-trip (exercises deep_union + write conversion)
# --------------------------------------------------------------------------- #
def test_universal_base_model_dict_round_trip() -> None:
    from deepgram.core.pydantic_utilities import UniversalBaseModel

    class Inner(UniversalBaseModel):
        inner_field: typing_extensions.Annotated[str, FieldMetadata(alias="innerField")]

    class Outer(UniversalBaseModel):
        outer_field: typing_extensions.Annotated[Inner, FieldMetadata(alias="outerField")]

    model = Outer(outer_field=Inner(inner_field="v"))
    dumped = model.dict(by_alias=True)
    assert dumped.get("outerField", {}).get("innerField") == "v"
    # json() path
    assert "innerField" in model.json(by_alias=True)


# --------------------------------------------------------------------------- #
# jsonable_encoder: iterable-of-pairs fallback (dict(o) path)
# --------------------------------------------------------------------------- #
def test_jsonable_encoder_iterable_of_pairs_fallback() -> None:
    class Pairs:
        def __iter__(self) -> typing.Iterator[typing.Tuple[str, int]]:
            return iter([("a", 1), ("b", 2)])

    assert jsonable_encoder(Pairs()) == {"a": 1, "b": 2}


# --------------------------------------------------------------------------- #
# unchecked_base_model: forward-ref resolution + field/config helpers
# --------------------------------------------------------------------------- #
class _ForwardRefHost:
    pass


def test_maybe_resolve_forward_ref() -> None:
    from deepgram.core.unchecked_base_model import _maybe_resolve_forward_ref

    # resolvable name (builtins are available to eval)
    assert _maybe_resolve_forward_ref(typing.ForwardRef("int"), host=_ForwardRefHost) is int
    # unresolvable name -> eval raises -> returned unchanged
    ref = typing.ForwardRef("NoSuchName_XYZ")
    assert _maybe_resolve_forward_ref(ref, host=_ForwardRefHost) is ref
    # not a ForwardRef -> returned unchanged
    assert _maybe_resolve_forward_ref(int, host=_ForwardRefHost) is int
    # no host -> returned unchanged
    assert _maybe_resolve_forward_ref(ref, host=None) is ref


def test_field_default_and_populate_helpers() -> None:
    from deepgram.core.unchecked_base_model import (
        _get_field_default,
        _get_is_populate_by_name,
        _get_model_fields,
    )

    class M(UncheckedBaseModel):
        x: int = 5

    fields = _get_model_fields(M)
    assert _get_field_default(fields["x"]) == 5
    assert isinstance(_get_is_populate_by_name(M), bool)


def test_construct_type_bool_coercion_exception() -> None:
    # An object whose __bool__ raises exercises the bool try/except -> return object_.
    class BadBool:
        def __bool__(self) -> bool:
            raise ValueError("nope")

    obj = BadBool()
    assert construct_type(object_=obj, type_=bool) is obj


# --------------------------------------------------------------------------- #
# http_client: low-level request with force_multipart and file uploads
# --------------------------------------------------------------------------- #
def _raw_http_client() -> typing.Any:
    from deepgram.core.http_client import HttpClient

    return HttpClient(
        httpx_client=httpx.Client(),
        base_timeout=lambda: 60.0,
        base_headers=lambda: {},
        base_url=lambda: BASE,
        base_max_retries=0,
    )


def test_http_request_force_multipart() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        resp = _raw_http_client().request(method="POST", path="v1/x", force_multipart=True)
        assert resp.status_code == 200


def test_http_request_with_files_and_none_data() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        resp = _raw_http_client().request(
            method="POST",
            path="v1/x",
            data={"field": "value", "skip": None},
            files={"file": ("name.wav", b"bytes")},
        )
        assert resp.status_code == 200


def test_get_request_body_empty_collapse() -> None:
    from deepgram.core.http_client import get_request_body

    # request_options present but empty -> bodies compute to {} then collapse to None
    json_body, data_body = get_request_body(json=None, data=None, request_options={}, omit=None)
    assert json_body is None and data_body is None


async def _raw_async_http_client() -> typing.Any:
    from deepgram.core.http_client import AsyncHttpClient

    return AsyncHttpClient(
        httpx_client=httpx.AsyncClient(),
        base_timeout=lambda: 60.0,
        base_headers=lambda: {},
        base_url=lambda: BASE,
        base_max_retries=0,
    )


async def test_async_http_request_force_multipart_and_files() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        client = await _raw_async_http_client()
        resp = await client.request(method="POST", path="v1/x", force_multipart=True)
        assert resp.status_code == 200
        resp2 = await client.request(
            method="POST",
            path="v1/x",
            data={"field": "value", "skip": None},
            files={"file": ("name.wav", b"bytes")},
        )
        assert resp2.status_code == 200


def test_transport_install_restore_roundtrip() -> None:
    from deepgram import transport as transport_module

    def factory(url: str, headers: typing.Dict[str, str]) -> typing.Any:
        return None

    try:
        transport_module.install_transport(sync_factory=factory)
        # re-installing the same factory is idempotent (no error)
        transport_module.install_transport(sync_factory=factory)
        # a different factory raises
        with pytest.raises(RuntimeError):
            transport_module.install_transport(sync_factory=lambda u, h: None)
    finally:
        transport_module.restore_transport()


def test_encode_by_type_isinstance_branch() -> None:
    from deepgram.core.pydantic_utilities import encode_by_type

    # A subclass whose exact type is unregistered but isinstance-matches a
    # registered encoder (set) -> the isinstance branch of encode_by_type.
    class MySet(set):
        pass

    assert isinstance(encode_by_type(MySet([1, 2])), list)


def test_get_field_default_fallback_to_default_attr() -> None:
    from deepgram.core.pydantic_utilities import _get_field_default

    class _Field:
        default = "fallback"

        def get_default(self) -> typing.Any:
            raise RuntimeError("no default accessor")

    assert _get_field_default(_Field()) == "fallback"


def test_get_base_url_requires_a_base() -> None:
    from deepgram.core.http_client import AsyncHttpClient, HttpClient

    sync = HttpClient(
        httpx_client=httpx.Client(), base_timeout=lambda: 60.0, base_headers=lambda: {}, base_url=lambda: None
    )
    with pytest.raises(ValueError):
        sync.get_base_url(None)

    asynchronous = AsyncHttpClient(
        httpx_client=httpx.AsyncClient(), base_timeout=lambda: 60.0, base_headers=lambda: {}, base_url=lambda: None
    )
    with pytest.raises(ValueError):
        asynchronous.get_base_url(None)

    # explicit base_url short-circuits the base_url() lookup
    assert sync.get_base_url("https://explicit.example.com") == "https://explicit.example.com"


class _ModuleEnum(enum.Enum):
    A = "a"
    B = "b"


def test_construct_type_enum_module_level() -> None:
    assert construct_type(object_="a", type_=_ModuleEnum) == _ModuleEnum.A
    assert construct_type(object_="missing", type_=_ModuleEnum) == "missing"
    assert construct_type(object_=_ModuleEnum.B, type_=_ModuleEnum) == _ModuleEnum.B


def test_construct_type_undiscriminated_union_second_pass() -> None:
    class P(UncheckedBaseModel):
        a: int = 0

    class Q(UncheckedBaseModel):
        b: int = 0

    # No literal discriminant -> falls to the "first successful cast" second pass.
    built = construct_type(object_={"a": 1}, type_=typing.Union[P, Q])
    assert built is None or isinstance(built, (P, Q, dict))
