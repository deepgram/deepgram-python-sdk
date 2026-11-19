"""
``auth=False`` for self-hosted and local Deepgram servers that don't require authentication.

Pins that:

  * the client constructs without an API key (and ignores ``DEEPGRAM_API_KEY``),
  * no ``Authorization`` header is sent on HTTP requests or WebSocket handshakes,
  * ``auth=False`` can't be combined with a credential, and only ``False`` is accepted,
  * the missing-key error suggests ``auth=False`` when the environment isn't a Deepgram host,
    and stays unchanged for Deepgram's hosted API,
  * a key passed for a self-hosted environment is still sent.

Hand-written and frozen in ``.fernignore``.
"""

import typing
from unittest.mock import patch

import httpx
import pytest

import deepgram.listen.v2.client as listen_v2_client
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment

LOCAL = DeepgramClientEnvironment(
    base="http://127.0.0.1:8000",
    production="ws://127.0.0.1:8000",
    agent="ws://127.0.0.1:8000",
    agent_rest="http://127.0.0.1:8000",
)
MISSING_KEY = "The client must be instantiated by either passing in api_key or setting DEEPGRAM_API_KEY"


@pytest.fixture(autouse=True)
def no_env_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEEPGRAM_API_KEY", raising=False)


class _CaptureConnect:
    """Stands in for ``websockets(.sync).connect`` and records the handshake headers."""

    def __init__(self) -> None:
        self.url: typing.Optional[str] = None
        self.headers: typing.Dict[str, str] = {}

    def __call__(self, url: str, **kwargs: typing.Any) -> "_CaptureConnect":
        self.url = url
        self.headers = dict(kwargs.get("additional_headers") or kwargs.get("extra_headers") or {})
        return self

    def __enter__(self) -> object:
        return object()

    def __exit__(self, *exc: typing.Any) -> bool:
        return False

    async def __aenter__(self) -> object:
        return object()

    async def __aexit__(self, *exc: typing.Any) -> bool:
        return False


def _capturing_transport(seen: typing.List[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    return httpx.MockTransport(handler)


# --------------------------------------------------------------------------- construction


def test_auth_false_constructs_without_a_key() -> None:
    DeepgramClient(environment=LOCAL, auth=False)
    AsyncDeepgramClient(environment=LOCAL, auth=False)


def test_auth_false_ignores_the_environment_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPGRAM_API_KEY", "from-env")
    client = DeepgramClient(environment=LOCAL, auth=False)
    assert "Authorization" not in client._client_wrapper.get_headers()


@pytest.mark.parametrize("credential", [{"api_key": "key"}, {"access_token": "token"}])
def test_auth_false_rejects_a_credential(credential: typing.Dict[str, str]) -> None:
    with pytest.raises(ValueError, match="auth=False cannot be combined"):
        DeepgramClient(environment=LOCAL, auth=False, **credential)
    with pytest.raises(ValueError, match="auth=False cannot be combined"):
        AsyncDeepgramClient(environment=LOCAL, auth=False, **credential)


@pytest.mark.parametrize("value", [True, "none", 0])
def test_auth_accepts_only_false(value: typing.Any) -> None:
    with pytest.raises(ValueError, match="auth only accepts False"):
        DeepgramClient(environment=LOCAL, auth=value, api_key="key")


# --------------------------------------------------------------------------- headers on the wire


def test_auth_false_sends_no_authorization_over_http() -> None:
    seen: typing.List[httpx.Request] = []
    client = DeepgramClient(
        environment=LOCAL, auth=False, httpx_client=httpx.Client(transport=_capturing_transport(seen))
    )
    client.manage.v1.models.list()
    assert len(seen) == 1
    assert str(seen[0].url).startswith("http://127.0.0.1:8000/v1/models")
    assert "authorization" not in seen[0].headers


async def test_async_auth_false_sends_no_authorization_over_http() -> None:
    seen: typing.List[httpx.Request] = []
    client = AsyncDeepgramClient(
        environment=LOCAL, auth=False, httpx_client=httpx.AsyncClient(transport=_capturing_transport(seen))
    )
    await client.manage.v1.models.list()
    assert len(seen) == 1
    assert "authorization" not in seen[0].headers


def test_auth_false_sends_no_authorization_on_websocket_handshake() -> None:
    capture = _CaptureConnect()
    with patch.object(listen_v2_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(environment=LOCAL, auth=False).listen.v2.connect(model="flux-general-en"):
            pass
    assert capture.url is not None and capture.url.startswith("ws://127.0.0.1:8000/v2/listen")
    assert "Authorization" not in capture.headers
    assert "x-deepgram-session-id" in capture.headers


async def test_async_auth_false_sends_no_authorization_on_websocket_handshake() -> None:
    capture = _CaptureConnect()
    with patch.object(listen_v2_client, "websockets_client_connect", capture):
        async with AsyncDeepgramClient(environment=LOCAL, auth=False).listen.v2.connect(model="flux-general-en"):
            pass
    assert "Authorization" not in capture.headers


def test_a_key_is_still_sent_to_a_self_hosted_server() -> None:
    seen: typing.List[httpx.Request] = []
    client = DeepgramClient(
        environment=LOCAL, api_key="local-key", httpx_client=httpx.Client(transport=_capturing_transport(seen))
    )
    client.manage.v1.models.list()
    assert seen[0].headers["authorization"] == "Token local-key"


# --------------------------------------------------------------------------- missing-key error


def _missing_key_body(**kwargs: typing.Any) -> str:
    with pytest.raises(ApiError) as caught:
        DeepgramClient(**kwargs)
    return str(caught.value.body)


def test_missing_key_error_suggests_auth_false_for_a_self_hosted_environment() -> None:
    body = _missing_key_body(environment=LOCAL)
    assert body.startswith(MISSING_KEY)
    assert "auth=False" in body


def test_explicit_none_key_also_gets_the_hint_for_a_self_hosted_environment() -> None:
    assert "auth=False" in _missing_key_body(environment=LOCAL, api_key=None)


def test_async_missing_key_error_suggests_auth_false() -> None:
    with pytest.raises(ApiError) as caught:
        AsyncDeepgramClient(environment=LOCAL)
    assert "auth=False" in str(caught.value.body)


def test_missing_key_error_is_unchanged_for_the_hosted_api() -> None:
    assert _missing_key_body() == MISSING_KEY


def test_missing_key_error_is_unchanged_for_a_regional_deepgram_host() -> None:
    eu = DeepgramClientEnvironment(
        base="https://api.eu.deepgram.com",
        production="wss://api.eu.deepgram.com",
        agent="wss://agent.deepgram.com",
        agent_rest="https://agent.deepgram.com",
    )
    assert _missing_key_body(environment=eu) == MISSING_KEY


def test_a_look_alike_host_is_not_treated_as_deepgram() -> None:
    lookalike = DeepgramClientEnvironment(
        base="https://notdeepgram.com",
        production="wss://notdeepgram.com",
        agent="wss://notdeepgram.com",
        agent_rest="https://notdeepgram.com",
    )
    assert "auth=False" in _missing_key_body(environment=lookalike)
