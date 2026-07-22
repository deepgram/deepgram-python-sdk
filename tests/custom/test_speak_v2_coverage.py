"""
Coverage for the Speak V2 (Flux TTS) client surface that the existing dedicated
tests leave untouched:

  * ``audio/client.py`` + ``audio/raw_client.py`` — the batch (REST) ``generate``
    endpoint. It is a *streaming* POST (``httpx_client.stream``), so it is not in
    the table-driven ``test_http_endpoints_coverage.py`` sweep and previously sat
    at 0%. Exercised here against a mocked transport (respx): the 2xx streaming
    success path plus the 400 (BadRequestError) and generic (ApiError) error
    branches, for both the sync and async clients.
  * ``client.py`` ``connect`` — the header plumbing (``authorization`` +
    ``additional_headers``), the ``audio`` lazy-init property, and the
    ``InvalidWebSocketStatus`` -> ``ApiError`` handshake-failure branches (401
    credentials message vs. the generic fallback), sync and async.
  * ``socket_client.py`` — the plain-iteration protocol (``__iter__`` /
    ``__aiter__``), the async send/recv paths, and the binary-frame passthrough
    in ``start_listening``, none of which the send/parse-focused
    ``test_speak_v2_socket.py`` drives.

No network / WireMock: HTTP is mocked with respx and the websocket entrypoints
are replaced with in-process shims / fakes.

Hand-written and frozen in ``.fernignore`` — Fern only generates HTTP WireMock
wire tests, so a regen would not reproduce this coverage.
"""

import json
from unittest.mock import patch

import httpx
import pytest
import respx

import deepgram.speak.v2.client as speak_v2_client
import deepgram.speak.v2.raw_client as speak_v2_raw_client
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.events import EventType
from deepgram.environment import DeepgramClientEnvironment
from deepgram.speak.v2.audio.client import AsyncAudioClient, AudioClient
from deepgram.speak.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.speak.v2.types.speak_v2flushed import SpeakV2Flushed
from deepgram.speak.v2.types.speak_v2speak import SpeakV2Speak

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=BASE, agent=BASE, agent_rest=BASE)


def _sync_client() -> DeepgramClient:
    return DeepgramClient(environment=_environment(), api_key="test_api_key")


def _async_client() -> AsyncDeepgramClient:
    # Force a plain httpx.AsyncClient transport; the default aiohttp-backed
    # transport cannot be intercepted by respx.
    return AsyncDeepgramClient(environment=_environment(), api_key="test_api_key", httpx_client=httpx.AsyncClient())


# --------------------------------------------------------------------------- #
# audio/client.py + audio/raw_client.py — batch REST generate (streaming POST)
# --------------------------------------------------------------------------- #


class TestAudioGenerateSuccess:
    def test_sync_streams_audio_bytes(self) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
            chunks = b"".join(
                _sync_client().speak.v2.audio.generate(model="flux-alexis-en", text="hello", tag=["a", "b"])
            )
        assert chunks == b"audio-bytes"

    async def test_async_streams_audio_bytes(self) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
            chunks = b""
            async for chunk in _async_client().speak.v2.audio.generate(model="flux-alexis-en", text="hello"):
                chunks += chunk
        assert chunks == b"audio-bytes"

    def test_with_raw_response_accessor(self) -> None:
        assert isinstance(
            _sync_client().speak.v2.audio.with_raw_response,
            type(AudioClient(client_wrapper=_sync_client()._client_wrapper).with_raw_response),
        )

    async def test_async_with_raw_response_accessor(self) -> None:
        client = _async_client()
        raw = client.speak.v2.audio.with_raw_response
        assert isinstance(raw, type(AsyncAudioClient(client_wrapper=client._client_wrapper).with_raw_response))


class TestAudioGenerateErrors:
    @pytest.mark.parametrize("status", [400, 403])
    def test_sync_error_statuses_raise_api_error(self, status: int) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(status, json={"error": "boom"}))
            with pytest.raises(ApiError):
                list(_sync_client().speak.v2.audio.generate(model="m", text="t"))

    @pytest.mark.parametrize("status", [400, 403])
    async def test_async_error_statuses_raise_api_error(self, status: int) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(status, json={"error": "boom"}))
            with pytest.raises(ApiError):
                async for _ in _async_client().speak.v2.audio.generate(model="m", text="t"):
                    pass

    def test_sync_non_json_error_body_raises_api_error(self) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(403, content=b"not json"))
            with pytest.raises(ApiError):
                list(_sync_client().speak.v2.audio.generate(model="m", text="t"))

    async def test_async_non_json_error_body_raises_api_error(self) -> None:
        with respx.mock:
            respx.route(host=HOST).mock(return_value=httpx.Response(403, content=b"not json"))
            with pytest.raises(ApiError):
                async for _ in _async_client().speak.v2.audio.generate(model="m", text="t"):
                    pass


# --------------------------------------------------------------------------- #
# client.py — connect() header plumbing, audio property, handshake failures
# --------------------------------------------------------------------------- #


class _CaptureConnect:
    """Records the URL/kwargs it is called with; usable as sync + async CM."""

    def __init__(self) -> None:
        self.url = None
        self.kwargs = None

    def __call__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs
        return self

    def __enter__(self):
        return object()

    def __exit__(self, *exc):
        return False

    async def __aenter__(self):
        return object()

    async def __aexit__(self, *exc):
        return False


class _RaisingConnect:
    """Raises a supplied ``InvalidWebSocketStatus`` instance when called, to drive
    the handshake-failure branch of ``connect``."""

    def __init__(self, exc):
        self._exc = exc

    def __call__(self, url, **kwargs):
        raise self._exc


def _invalid_status_exc():
    # Build an InvalidWebSocketStatus without invoking its version-specific
    # constructor; connect() reads the code via get_status_code, which we patch.
    return speak_v2_client.InvalidWebSocketStatus.__new__(speak_v2_client.InvalidWebSocketStatus)


class TestConnectHeaders:
    def test_sync_connect_forwards_authorization_and_additional_headers(self) -> None:
        capture = _CaptureConnect()
        with patch.object(speak_v2_client.websockets_sync_client, "connect", capture):
            with DeepgramClient(api_key="test_api_key").speak.v2.connect(
                model="flux-alexis-en",
                authorization="Token override",
                request_options={"additional_headers": {"X-Custom": "1"}},
            ):
                pass
        headers = capture.kwargs["additional_headers"]
        assert headers["Authorization"] == "Token override"
        assert headers["X-Custom"] == "1"

    async def test_async_connect_forwards_authorization_and_additional_headers(self) -> None:
        capture = _CaptureConnect()
        with patch.object(speak_v2_client, "websockets_client_connect", capture):
            async with AsyncDeepgramClient(api_key="test_api_key").speak.v2.connect(
                model="flux-alexis-en",
                authorization="Bearer tok",
                request_options={"additional_headers": {"X-Custom": "2"}},
            ):
                pass
        headers = capture.kwargs["extra_headers"]
        assert headers["Authorization"] == "Bearer tok"
        assert headers["X-Custom"] == "2"


class TestConnectHandshakeFailure:
    @pytest.mark.parametrize("status,needle", [(401, "invalid credentials"), (503, "Unexpected error")])
    def test_sync_invalid_status_maps_to_api_error(self, status: int, needle: str) -> None:
        raising = _RaisingConnect(_invalid_status_exc())
        with (
            patch.object(speak_v2_client.websockets_sync_client, "connect", raising),
            patch.object(speak_v2_client, "get_status_code", lambda exc: status),
        ):
            with pytest.raises(ApiError) as excinfo:
                with DeepgramClient(api_key="test_api_key").speak.v2.connect(model="flux-alexis-en"):
                    pass
        assert excinfo.value.status_code == status
        assert needle in str(excinfo.value.body)

    @pytest.mark.parametrize("status,needle", [(401, "invalid credentials"), (503, "Unexpected error")])
    async def test_async_invalid_status_maps_to_api_error(self, status: int, needle: str) -> None:
        raising = _RaisingConnect(_invalid_status_exc())
        with (
            patch.object(speak_v2_client, "websockets_client_connect", raising),
            patch.object(speak_v2_client, "get_status_code", lambda exc: status),
        ):
            with pytest.raises(ApiError) as excinfo:
                async with AsyncDeepgramClient(api_key="test_api_key").speak.v2.connect(model="flux-alexis-en"):
                    pass
        assert excinfo.value.status_code == status
        assert needle in str(excinfo.value.body)


class TestV2ClientAccessors:
    def test_sync_audio_property_is_cached(self) -> None:
        v2 = _sync_client().speak.v2
        first = v2.audio
        assert isinstance(first, AudioClient)
        assert v2.audio is first  # second access hits the cached branch

    def test_async_audio_property_is_cached(self) -> None:
        v2 = _async_client().speak.v2
        first = v2.audio
        assert isinstance(first, AsyncAudioClient)
        assert v2.audio is first

    def test_with_raw_response_accessors(self) -> None:
        assert _sync_client().speak.v2.with_raw_response is not None
        assert _async_client().speak.v2.with_raw_response is not None


# --------------------------------------------------------------------------- #
# raw_client.py — RawV2Client.connect / AsyncRawV2Client.connect (the
# ``with_raw_response.connect`` variant), a near-duplicate of the public connect.
# --------------------------------------------------------------------------- #


class TestRawConnect:
    def test_sync_raw_connect_forwards_headers(self) -> None:
        capture = _CaptureConnect()
        with patch.object(speak_v2_raw_client.websockets_sync_client, "connect", capture):
            with _sync_client().speak.v2.with_raw_response.connect(
                model="flux-alexis-en",
                authorization="Token override",
                request_options={"additional_headers": {"X-Custom": "1"}},
            ):
                pass
        headers = capture.kwargs["additional_headers"]
        assert headers["Authorization"] == "Token override"
        assert headers["X-Custom"] == "1"

    async def test_async_raw_connect_forwards_headers(self) -> None:
        capture = _CaptureConnect()
        with patch.object(speak_v2_raw_client, "websockets_client_connect", capture):
            async with _async_client().speak.v2.with_raw_response.connect(
                model="flux-alexis-en",
                authorization="Bearer tok",
                request_options={"additional_headers": {"X-Custom": "2"}},
            ):
                pass
        headers = capture.kwargs["extra_headers"]
        assert headers["Authorization"] == "Bearer tok"
        assert headers["X-Custom"] == "2"

    @pytest.mark.parametrize("status,needle", [(401, "invalid credentials"), (503, "Unexpected error")])
    def test_sync_raw_connect_handshake_failure(self, status: int, needle: str) -> None:
        raising = _RaisingConnect(
            speak_v2_raw_client.InvalidWebSocketStatus.__new__(speak_v2_raw_client.InvalidWebSocketStatus)
        )
        with (
            patch.object(speak_v2_raw_client.websockets_sync_client, "connect", raising),
            patch.object(speak_v2_raw_client, "get_status_code", lambda exc: status),
        ):
            with pytest.raises(ApiError) as excinfo:
                with _sync_client().speak.v2.with_raw_response.connect(model="flux-alexis-en"):
                    pass
        assert excinfo.value.status_code == status
        assert needle in str(excinfo.value.body)

    @pytest.mark.parametrize("status,needle", [(401, "invalid credentials"), (503, "Unexpected error")])
    async def test_async_raw_connect_handshake_failure(self, status: int, needle: str) -> None:
        raising = _RaisingConnect(
            speak_v2_raw_client.InvalidWebSocketStatus.__new__(speak_v2_raw_client.InvalidWebSocketStatus)
        )
        with (
            patch.object(speak_v2_raw_client, "websockets_client_connect", raising),
            patch.object(speak_v2_raw_client, "get_status_code", lambda exc: status),
        ):
            with pytest.raises(ApiError) as excinfo:
                async with _async_client().speak.v2.with_raw_response.connect(model="flux-alexis-en"):
                    pass
        assert excinfo.value.status_code == status
        assert needle in str(excinfo.value.body)


# --------------------------------------------------------------------------- #
# socket_client.py — iteration protocol, async send/recv, binary passthrough
# --------------------------------------------------------------------------- #


class _FakeWebSocket:
    def __init__(self, incoming=None):
        self.sent = []
        self._incoming = list(incoming or [])

    def send(self, data):
        self.sent.append(data)

    def recv(self):
        return self._incoming.pop(0)

    def __iter__(self):
        yield from self._incoming


class _FakeAsyncWebSocket:
    def __init__(self, incoming=None):
        self.sent = []
        self._incoming = list(incoming or [])

    async def send(self, data):
        self.sent.append(data)

    async def recv(self):
        return self._incoming.pop(0)

    def __aiter__(self):
        incoming = self._incoming

        async def _gen():
            for message in incoming:
                yield message

        return _gen()


class TestSyncIterationProtocol:
    def test_iter_parses_json_skips_unparseable_and_passes_bytes(self) -> None:
        ws = _FakeWebSocket(
            incoming=[
                b"\x00audio",
                json.dumps({"type": "Flushed", "speech_id": "s-1"}),
                "not-json{",  # json.loads raises -> caught and skipped, not yielded
            ]
        )
        out = list(V2SocketClient(websocket=ws))
        assert out[0] == b"\x00audio"
        assert isinstance(out[1], SpeakV2Flushed)
        # The unparseable frame is dropped by the except/continue branch.
        assert len(out) == 2

    def test_start_listening_emits_binary_frame(self) -> None:
        ws = _FakeWebSocket(incoming=[b"\x01\x02"])
        client = V2SocketClient(websocket=ws)
        messages = []
        client.on(EventType.MESSAGE, messages.append)
        client.start_listening()
        assert messages == [b"\x01\x02"]

    def test_send_non_dict_passthrough(self) -> None:
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws)._send("raw-string")  # non-dict -> no json.dumps
        assert ws.sent == ["raw-string"]


class TestAsyncIterationAndSend:
    async def test_aiter_parses_json_skips_unparseable_and_passes_bytes(self) -> None:
        ws = _FakeAsyncWebSocket(
            incoming=[
                b"\x00audio",
                json.dumps({"type": "Flushed", "speech_id": "s-1"}),
                "not-json{",  # json.loads raises -> caught and skipped
            ]
        )
        out = [message async for message in AsyncV2SocketClient(websocket=ws)]
        assert out[0] == b"\x00audio"
        assert isinstance(out[1], SpeakV2Flushed)
        assert len(out) == 2

    async def test_start_listening_emits_binary_frame(self) -> None:
        ws = _FakeAsyncWebSocket(incoming=[b"\x03\x04"])
        client = AsyncV2SocketClient(websocket=ws)
        messages = []
        client.on(EventType.MESSAGE, messages.append)
        await client.start_listening()
        assert messages == [b"\x03\x04"]

    async def test_send_speak_flush_close_serialize(self) -> None:
        ws = _FakeAsyncWebSocket()
        client = AsyncV2SocketClient(websocket=ws)
        await client.send_speak(SpeakV2Speak(text="hi"))
        await client.send_flush()
        await client.send_close()
        types = [json.loads(p)["type"] for p in ws.sent]
        assert types == ["Speak", "Flush", "Close"]
        assert json.loads(ws.sent[0])["text"] == "hi"

    async def test_recv_binary_passthrough_and_non_dict_send(self) -> None:
        ws = _FakeAsyncWebSocket(incoming=[b"binary-frame"])
        client = AsyncV2SocketClient(websocket=ws)
        assert await client.recv() == b"binary-frame"
        await client._send("raw-string")  # non-dict -> no json.dumps
        assert ws.sent == ["raw-string"]

    async def test_start_listening_surfaces_malformed_frame_as_error(self) -> None:
        # A malformed (non-JSON) text frame makes json.loads raise inside the
        # loop; the broad except surfaces it as an ERROR event, then CLOSE.
        ws = _FakeAsyncWebSocket(incoming=["not-json{"])
        client = AsyncV2SocketClient(websocket=ws)
        events = []
        client.on(EventType.ERROR, lambda exc: events.append(("error", exc)))
        client.on(EventType.CLOSE, lambda _: events.append(("close", None)))
        await client.start_listening()
        assert events[0][0] == "error"
        assert events[-1] == ("close", None)


class TestSocketConstructTypeGuard:
    """The inner ``try/except`` around ``construct_type`` is the forward-compat
    safety net: if parsing a *well-formed* JSON frame ever raises, ``recv`` must
    return the raw payload and the listen loops must skip the frame rather than
    crash. ``construct_type`` is lenient in practice, so the guard is driven by
    forcing it to raise."""

    def _boom(self, *args, **kwargs):
        raise ValueError("construct blew up")

    def test_sync_recv_returns_raw_on_construct_error(self) -> None:
        ws = _FakeWebSocket(incoming=[json.dumps({"type": "Flushed", "speech_id": "s-1"})])
        with patch("deepgram.speak.v2.socket_client.construct_type", self._boom):
            assert V2SocketClient(websocket=ws).recv() == {"type": "Flushed", "speech_id": "s-1"}

    async def test_async_recv_returns_raw_on_construct_error(self) -> None:
        ws = _FakeAsyncWebSocket(incoming=[json.dumps({"type": "Flushed", "speech_id": "s-1"})])
        with patch("deepgram.speak.v2.socket_client.construct_type", self._boom):
            assert await AsyncV2SocketClient(websocket=ws).recv() == {"type": "Flushed", "speech_id": "s-1"}

    def test_sync_start_listening_skips_on_construct_error(self) -> None:
        ws = _FakeWebSocket(incoming=[json.dumps({"type": "Flushed", "speech_id": "s-1"})])
        client = V2SocketClient(websocket=ws)
        messages, errors = [], []
        client.on(EventType.MESSAGE, messages.append)
        client.on(EventType.ERROR, errors.append)
        with patch("deepgram.speak.v2.socket_client.construct_type", self._boom):
            client.start_listening()
        assert messages == []  # frame skipped, no crash
        assert errors == []

    async def test_async_start_listening_skips_on_construct_error(self) -> None:
        ws = _FakeAsyncWebSocket(incoming=[json.dumps({"type": "Flushed", "speech_id": "s-1"})])
        client = AsyncV2SocketClient(websocket=ws)
        messages, errors = [], []
        client.on(EventType.MESSAGE, messages.append)
        client.on(EventType.ERROR, errors.append)
        with patch("deepgram.speak.v2.socket_client.construct_type", self._boom):
            await client.start_listening()
        assert messages == []
        assert errors == []
