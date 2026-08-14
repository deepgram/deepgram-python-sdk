"""
Data-driven coverage for the auto-generated REST endpoint clients.

Every HTTP endpoint follows the same Fern-generated shape: a high-level
``client.py`` method delegates to a ``raw_client.py`` method that calls
``httpx_client.request(...)`` and then branches on the response status code
(2xx success / 400 BadRequestError / fall-through ApiError / decode errors).

Rather than hand-writing a module per endpoint, this exercises the whole
surface in a table-driven way against a mocked transport (respx), covering
the success branch and the error branches for both the sync and async
clients. Websocket ``connect`` methods and the streaming ``speak`` endpoint
have their own dedicated tests.
"""

import typing

import httpx
import pytest
import respx

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


def _sync_client() -> DeepgramClient:
    return DeepgramClient(environment=_environment(), api_key="test_api_key")


def _async_client() -> AsyncDeepgramClient:
    # Force a plain httpx.AsyncClient transport. By default the async client
    # auto-detects and uses an aiohttp-backed transport, which respx cannot
    # intercept (the requests would hit the real network).
    return AsyncDeepgramClient(
        environment=_environment(), api_key="test_api_key", httpx_client=httpx.AsyncClient()
    )


def _resolve(client: typing.Any, dotted_path: str) -> typing.Any:
    """Walk ``a.b.c`` attribute chain from the client to the bound endpoint method."""
    obj = client
    for part in dotted_path.split("."):
        obj = getattr(obj, part)
    return obj


# (dotted method path, kwargs). All path params are positional-or-keyword in the
# generated code, so they can be supplied by name. Request bodies use the minimal
# shape the generated method requires.
ENDPOINTS: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]] = [
    ("agent.v1.settings.think.models.list", {}),
    ("auth.v1.tokens.grant", {}),
    ("listen.v1.media.transcribe_file", {"request": b"\x00\x00"}),
    ("listen.v1.media.transcribe_url", {"url": "https://example.com/a.wav"}),
    ("manage.v1.models.get", {"model_id": "m"}),
    ("manage.v1.models.list", {}),
    ("manage.v1.projects.billing.balances.get", {"project_id": "p", "balance_id": "b"}),
    ("manage.v1.projects.billing.balances.list", {"project_id": "p"}),
    ("manage.v1.projects.billing.breakdown.list", {"project_id": "p"}),
    ("manage.v1.projects.billing.fields.list", {"project_id": "p"}),
    ("manage.v1.projects.billing.purchases.list", {"project_id": "p"}),
    ("manage.v1.projects.delete", {"project_id": "p"}),
    ("manage.v1.projects.get", {"project_id": "p"}),
    ("manage.v1.projects.keys.create", {"project_id": "p", "request": {}}),
    ("manage.v1.projects.keys.delete", {"project_id": "p", "key_id": "k"}),
    ("manage.v1.projects.keys.get", {"project_id": "p", "key_id": "k"}),
    ("manage.v1.projects.keys.list", {"project_id": "p"}),
    ("manage.v1.projects.leave", {"project_id": "p"}),
    ("manage.v1.projects.list", {}),
    ("manage.v1.projects.members.delete", {"project_id": "p", "member_id": "m"}),
    ("manage.v1.projects.members.invites.create", {"project_id": "p", "email": "e@x.com", "scope": "member"}),
    ("manage.v1.projects.members.invites.delete", {"project_id": "p", "email": "e@x.com"}),
    ("manage.v1.projects.members.invites.list", {"project_id": "p"}),
    ("manage.v1.projects.members.list", {"project_id": "p"}),
    ("manage.v1.projects.members.scopes.list", {"project_id": "p", "member_id": "m"}),
    ("manage.v1.projects.members.scopes.update", {"project_id": "p", "member_id": "m", "scope": "member"}),
    ("manage.v1.projects.models.get", {"project_id": "p", "model_id": "m"}),
    ("manage.v1.projects.models.list", {"project_id": "p"}),
    ("manage.v1.projects.requests.get", {"project_id": "p", "request_id": "r"}),
    ("manage.v1.projects.requests.list", {"project_id": "p"}),
    ("manage.v1.projects.update", {"project_id": "p", "name": "new-name"}),
    ("manage.v1.projects.usage.breakdown.get", {"project_id": "p"}),
    ("manage.v1.projects.usage.fields.list", {"project_id": "p"}),
    ("manage.v1.projects.usage.get", {"project_id": "p"}),
    ("read.v1.text.analyze", {"request": {"url": "https://example.com/a.txt"}}),
    ("self_hosted.v1.distribution_credentials.create", {"project_id": "p"}),
    ("self_hosted.v1.distribution_credentials.delete", {"project_id": "p", "distribution_credentials_id": "d"}),
    ("self_hosted.v1.distribution_credentials.get", {"project_id": "p", "distribution_credentials_id": "d"}),
    ("self_hosted.v1.distribution_credentials.list", {"project_id": "p"}),
    ("voice_agent.configurations.create", {"project_id": "p", "config": "cfg"}),
    ("voice_agent.configurations.delete", {"project_id": "p", "agent_id": "a"}),
    ("voice_agent.configurations.get", {"project_id": "p", "agent_id": "a"}),
    ("voice_agent.configurations.list", {"project_id": "p"}),
    ("voice_agent.configurations.update", {"project_id": "p", "agent_id": "a", "metadata": {"k": "v"}}),
    ("voice_agent.variables.create", {"project_id": "p", "key": "k", "value": "v"}),
    ("voice_agent.variables.delete", {"project_id": "p", "variable_id": "v"}),
    ("voice_agent.variables.get", {"project_id": "p", "variable_id": "v"}),
    ("voice_agent.variables.list", {"project_id": "p"}),
    ("voice_agent.variables.update", {"project_id": "p", "variable_id": "v", "value": "v"}),
]

_ENDPOINT_IDS = [path for path, _ in ENDPOINTS]


@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
def test_endpoint_success_sync(path: str, kwargs: typing.Dict[str, typing.Any]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        result = _resolve(_sync_client(), path)(**kwargs)
        assert result is not None


@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
async def test_endpoint_success_async(path: str, kwargs: typing.Dict[str, typing.Any]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        result = await _resolve(_async_client(), path)(**kwargs)
        assert result is not None


# 400 hits the dedicated BadRequestError branch; 403 falls through to the
# generic ApiError branch. Both are non-retryable (the client retries only on
# >=500 / 429 / 408 / 409), so the suite stays fast and deterministic.
_ERROR_STATUSES = [400, 403]


@pytest.mark.parametrize("status", _ERROR_STATUSES)
@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
def test_endpoint_error_sync(path: str, kwargs: typing.Dict[str, typing.Any], status: int) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(status, json={"error": "boom"}))
        with pytest.raises(ApiError):
            _resolve(_sync_client(), path)(**kwargs)


@pytest.mark.parametrize("status", _ERROR_STATUSES)
@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
async def test_endpoint_error_async(path: str, kwargs: typing.Dict[str, typing.Any], status: int) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(status, json={"error": "boom"}))
        with pytest.raises(ApiError):
            await _resolve(_async_client(), path)(**kwargs)


# A non-JSON error body exercises the ``except JSONDecodeError -> ApiError``
# branch present in every raw_client method.
@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
def test_endpoint_non_json_error_body_sync(path: str, kwargs: typing.Dict[str, typing.Any]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(403, content=b"not json"))
        with pytest.raises(ApiError):
            _resolve(_sync_client(), path)(**kwargs)


@pytest.mark.parametrize("path,kwargs", ENDPOINTS, ids=_ENDPOINT_IDS)
async def test_endpoint_non_json_error_body_async(path: str, kwargs: typing.Dict[str, typing.Any]) -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(403, content=b"not json"))
        with pytest.raises(ApiError):
            await _resolve(_async_client(), path)(**kwargs)


def test_with_raw_response_returns_http_response_sync() -> None:
    """The ``with_raw_response`` accessor returns the raw HttpResponse wrapper."""
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, json={}))
        raw = _sync_client().manage.v1.projects.with_raw_response.list()
        assert raw.data is not None


def _walk_subclients(obj: typing.Any, depth: int = 0, seen: typing.Optional[set] = None) -> int:
    """Touch every nested sub-client property to cover their lazy-init accessors."""
    seen = seen if seen is not None else set()
    if id(obj) in seen or depth > 8:
        return 0
    seen.add(id(obj))
    count = 0
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            attr = getattr(obj, name)
        except Exception:
            continue
        module = getattr(type(attr), "__module__", "") or ""
        if module.startswith("deepgram") and not callable(attr):
            count += 1
            count += _walk_subclients(attr, depth + 1, seen)
    return count


def test_subclient_accessors_are_reachable_sync() -> None:
    client = _sync_client()
    # Access twice so both the lazy-construct and cached branches run.
    assert _walk_subclients(client) > 0
    assert _walk_subclients(client) > 0


def test_subclient_accessors_are_reachable_async() -> None:
    client = _async_client()
    assert _walk_subclients(client) > 0
    assert _walk_subclients(client) > 0
