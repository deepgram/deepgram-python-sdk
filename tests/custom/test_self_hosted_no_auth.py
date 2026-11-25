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

import deepgram.agent.v1.client as agent_v1_client
import deepgram.agent.v1.raw_client as agent_v1_raw_client
import deepgram.listen.v1.client as listen_v1_client
import deepgram.listen.v1.raw_client as listen_v1_raw_client
import deepgram.listen.v2.client as listen_v2_client
import deepgram.listen.v2.raw_client as listen_v2_raw_client
import deepgram.speak.v1.client as speak_v1_client
import deepgram.speak.v1.raw_client as speak_v1_raw_client
import deepgram.speak.v2.client as speak_v2_client
import deepgram.speak.v2.raw_client as speak_v2_raw_client
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment
from deepgram.transport import restore_transport

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


class _CloseOnlyTransport:
    def close(self) -> None:
        pass


def _capturing_transport(seen: typing.List[httpx.Request]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={})

    return httpx.MockTransport(handler)


def _assert_no_authorization(headers: typing.Mapping[str, str]) -> None:
    assert all(key.lower() != "authorization" for key in headers)


def _connection_options(model: typing.Optional[str] = None) -> typing.Dict[str, typing.Any]:
    options: typing.Dict[str, typing.Any] = {
        "authorization": "Token connect-argument",
        "request_options": {"additional_headers": {"Authorization": "Token request-header"}},
    }
    if model is not None:
        options["model"] = model
    return options


_WEBSOCKET_CASES = [
    (
        "listen v1",
        listen_v1_client,
        listen_v1_raw_client,
        lambda client: client.listen.v1.connect(**_connection_options("nova-3")),
        lambda client: client.listen.v1.with_raw_response.connect(**_connection_options("nova-3")),
        "/v1/listen",
    ),
    (
        "listen v2",
        listen_v2_client,
        listen_v2_raw_client,
        lambda client: client.listen.v2.connect(**_connection_options("flux-general-en")),
        lambda client: client.listen.v2.with_raw_response.connect(**_connection_options("flux-general-en")),
        "/v2/listen",
    ),
    (
        "speak v1",
        speak_v1_client,
        speak_v1_raw_client,
        lambda client: client.speak.v1.connect(**_connection_options("aura-2-thalia-en")),
        lambda client: client.speak.v1.with_raw_response.connect(**_connection_options("aura-2-thalia-en")),
        "/v1/speak",
    ),
    (
        "speak v2",
        speak_v2_client,
        speak_v2_raw_client,
        lambda client: client.speak.v2.connect(**_connection_options("aura-2-thalia-en")),
        lambda client: client.speak.v2.with_raw_response.connect(**_connection_options("aura-2-thalia-en")),
        "/v2/speak",
    ),
    (
        "agent v1",
        agent_v1_client,
        agent_v1_raw_client,
        lambda client: client.agent.v1.connect(**_connection_options()),
        lambda client: client.agent.v1.with_raw_response.connect(**_connection_options()),
        "/v1/agent/converse",
    ),
]


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
        environment=LOCAL,
        auth=False,
        headers={"authorization": "Token client-header"},
        httpx_client=httpx.Client(transport=_capturing_transport(seen)),
    )
    client.manage.v1.models.list(request_options={"additional_headers": {"Authorization": "Token request-header"}})
    assert len(seen) == 1
    assert str(seen[0].url).startswith("http://127.0.0.1:8000/v1/models")
    _assert_no_authorization(seen[0].headers)


def test_auth_false_matches_origin_with_uppercase_scheme_and_default_port() -> None:
    # httpx keeps an explicit default port when the scheme is uppercase, so the hook
    # must normalize the request URL the same way it normalizes the environment.
    seen: typing.List[httpx.Request] = []
    environment = DeepgramClientEnvironment(
        base="HTTP://localhost:80",
        production="ws://localhost:80",
        agent="ws://localhost:80",
        agent_rest="HTTP://localhost:80",
    )
    client = DeepgramClient(
        environment=environment,
        auth=False,
        httpx_client=httpx.Client(
            headers={"Authorization": "Token httpx-client"}, transport=_capturing_transport(seen)
        ),
    )
    client.manage.v1.models.list(request_options={"additional_headers": {"Authorization": "Token request-header"}})
    assert len(seen) == 1
    _assert_no_authorization(seen[0].headers)


def test_auth_false_only_strips_authorization_from_its_own_httpx_requests() -> None:
    seen: typing.List[httpx.Request] = []
    httpx_client = httpx.Client(
        headers={"Authorization": "Token httpx-client"},
        auth=("username", "password"),
        transport=_capturing_transport(seen),
    )
    client = DeepgramClient(environment=LOCAL, auth=False, httpx_client=httpx_client)
    client.manage.v1.models.list()

    _assert_no_authorization(seen[0].headers)
    assert httpx_client.auth is not None

    httpx_client.get("http://127.0.0.1:8000/not-an-sdk-request")
    assert "authorization" in seen[1].headers


def test_auth_false_only_strips_authorization_from_its_own_httpx_streams() -> None:
    seen: typing.List[httpx.Request] = []
    httpx_client = httpx.Client(
        headers={"Authorization": "Token httpx-client"},
        auth=("username", "password"),
        transport=_capturing_transport(seen),
    )
    client = DeepgramClient(environment=LOCAL, auth=False, httpx_client=httpx_client)

    list(
        client.speak.v1.audio.generate(
            text="test",
            request_options={"additional_headers": {"authorization": "Token request-header"}},
        )
    )

    _assert_no_authorization(seen[0].headers)
    assert httpx_client.auth is not None


async def test_async_auth_false_sends_no_authorization_over_http() -> None:
    seen: typing.List[httpx.Request] = []
    client = AsyncDeepgramClient(
        environment=LOCAL,
        auth=False,
        headers={"authorization": "Token client-header"},
        httpx_client=httpx.AsyncClient(transport=_capturing_transport(seen)),
    )
    await client.manage.v1.models.list(
        request_options={"additional_headers": {"Authorization": "Token request-header"}}
    )
    assert len(seen) == 1
    _assert_no_authorization(seen[0].headers)


async def test_async_auth_false_only_strips_authorization_from_its_own_httpx_requests() -> None:
    seen: typing.List[httpx.Request] = []
    httpx_client = httpx.AsyncClient(
        headers={"Authorization": "Token httpx-client"},
        auth=("username", "password"),
        transport=_capturing_transport(seen),
    )
    client = AsyncDeepgramClient(environment=LOCAL, auth=False, httpx_client=httpx_client)
    await client.manage.v1.models.list()

    _assert_no_authorization(seen[0].headers)
    assert httpx_client.auth is not None

    await httpx_client.get("http://127.0.0.1:8000/not-an-sdk-request")
    assert "authorization" in seen[1].headers


async def test_async_auth_false_only_strips_authorization_from_its_own_httpx_streams() -> None:
    seen: typing.List[httpx.Request] = []
    httpx_client = httpx.AsyncClient(
        headers={"Authorization": "Token httpx-client"},
        auth=("username", "password"),
        transport=_capturing_transport(seen),
    )
    client = AsyncDeepgramClient(environment=LOCAL, auth=False, httpx_client=httpx_client)

    async for _ in client.speak.v1.audio.generate(
        text="test",
        request_options={"additional_headers": {"authorization": "Token request-header"}},
    ):
        pass

    _assert_no_authorization(seen[0].headers)
    assert httpx_client.auth is not None


@pytest.mark.parametrize(
    "_name,client_module,_raw_client_module,connect,_raw_connect,path",
    _WEBSOCKET_CASES,
)
def test_auth_false_sends_no_authorization_on_websocket_handshakes(
    _name: str,
    client_module: typing.Any,
    _raw_client_module: typing.Any,
    connect: typing.Callable[[DeepgramClient], typing.ContextManager[typing.Any]],
    _raw_connect: typing.Callable[[DeepgramClient], typing.ContextManager[typing.Any]],
    path: str,
) -> None:
    capture = _CaptureConnect()
    with patch.object(client_module.websockets_sync_client, "connect", capture):
        with connect(DeepgramClient(environment=LOCAL, auth=False, headers={"authorization": "Token client-header"})):
            pass
    assert capture.url is not None and capture.url.startswith(f"ws://127.0.0.1:8000{path}")
    _assert_no_authorization(capture.headers)
    assert "x-deepgram-session-id" in capture.headers


@pytest.mark.parametrize(
    "_name,_client_module,raw_client_module,_connect,raw_connect,_path",
    _WEBSOCKET_CASES,
)
async def test_async_auth_false_sends_no_authorization_on_websocket_handshakes(
    _name: str,
    _client_module: typing.Any,
    raw_client_module: typing.Any,
    _connect: typing.Callable[[AsyncDeepgramClient], typing.AsyncContextManager[typing.Any]],
    raw_connect: typing.Callable[[AsyncDeepgramClient], typing.AsyncContextManager[typing.Any]],
    _path: str,
) -> None:
    capture = _CaptureConnect()
    with patch.object(raw_client_module, "websockets_client_connect", capture):
        async with raw_connect(
            AsyncDeepgramClient(environment=LOCAL, auth=False, headers={"authorization": "Token client-header"})
        ):
            pass
    _assert_no_authorization(capture.headers)


def test_auth_false_sends_no_authorization_to_a_custom_websocket_transport() -> None:
    captured: typing.Dict[str, str] = {}

    def factory(_url: str, headers: typing.Dict[str, str]) -> _CloseOnlyTransport:
        captured.update(headers)
        return _CloseOnlyTransport()

    try:
        with DeepgramClient(
            environment=LOCAL,
            auth=False,
            headers={"authorization": "Token client-header"},
            transport_factory=factory,
        ).listen.v2.connect(
            model="flux-general-en",
            authorization="Token connect-argument",
            request_options={"additional_headers": {"Authorization": "Token request-header"}},
        ):
            pass
    finally:
        restore_transport()

    _assert_no_authorization(captured)


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


def test_a_base_without_a_scheme_gets_the_hint() -> None:
    # An easy mistake with a local server: "127.0.0.1:8000" parses with no host, and a base with
    # no host can never be Deepgram's.
    schemeless = DeepgramClientEnvironment(
        base="127.0.0.1:8000",
        production="127.0.0.1:8000",
        agent="127.0.0.1:8000",
        agent_rest="127.0.0.1:8000",
    )
    body = _missing_key_body(environment=schemeless)
    assert body.startswith(MISSING_KEY)
    assert "auth=False" in body
