"""
Coverage for the websocket ``connect`` clients, their socket clients, and the
streaming TTS (``speak.v1.audio.generate``) endpoint.

These paths are not reachable through the HTTP request mock used by
``test_http_endpoints_coverage`` and are not exercised by the WireMock-based
wire tests, so they are driven here directly:

* ``connect`` is exercised by monkeypatching the ``websockets`` connect call so
  it yields a fake protocol. The same test then drives every method of the
  resulting socket client (send_*, recv, iteration, start_listening), which
  covers ``connect``, the high-level client wrapper, and ``socket_client`` in
  one shot.
* The InvalidWebSocketStatus -> ApiError mapping is covered by making the
  patched connect raise.
* The streaming TTS endpoint is covered with a mocked transport (respx).
"""

import typing

import httpx
import pytest
import respx
import websockets.sync.client as websockets_sync_client

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.events import EventType
from deepgram.core.websocket_compat import InvalidWebSocketStatus
from deepgram.environment import DeepgramClientEnvironment

HOST = "test.deepgram.local"
BASE = f"https://{HOST}"
WS_BASE = f"wss://{HOST}"


def _environment() -> DeepgramClientEnvironment:
    return DeepgramClientEnvironment(base=BASE, production=WS_BASE, agent=WS_BASE, agent_rest=BASE)


def _sync_client() -> DeepgramClient:
    return DeepgramClient(environment=_environment(), api_key="test_api_key")


def _async_client() -> AsyncDeepgramClient:
    return AsyncDeepgramClient(
        environment=_environment(), api_key="test_api_key", httpx_client=httpx.AsyncClient()
    )


def _resolve(client: typing.Any, dotted_path: str) -> typing.Any:
    obj = client
    for part in dotted_path.split("."):
        obj = getattr(obj, part)
    return obj


# A stand-in for the typed message models the send_* helpers expect. The socket
# client only calls ``.dict()`` on it; the float/list/nested values exercise the
# numeric-sanitizing branch in the agent socket client.
class _DummyModel:
    def dict(self) -> typing.Dict[str, typing.Any]:
        return {"type": "X", "sample_rate": 44100.0, "nested": {"v": 2.0}, "items": [1.0, "a"]}


# Messages fed to the iterators: a binary frame, a parseable JSON frame, and a
# non-JSON frame (skipped on iteration, surfaced as an ERROR by start_listening).
_ITER_MESSAGES = [b"\x00\x01", '{"type":"Welcome"}', "this is not json"]


class _FakeSyncWS:
    def __init__(self) -> None:
        self.sent: typing.List[typing.Any] = []
        self._recv_queue: typing.List[typing.Any] = [b"\x02", '{"type":"Welcome"}', '{"type":"Welcome"}']

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(_ITER_MESSAGES)

    def recv(self) -> typing.Any:
        return self._recv_queue.pop(0)

    def send(self, data: typing.Any) -> None:
        self.sent.append(data)


class _FakeAsyncWS:
    def __init__(self) -> None:
        self.sent: typing.List[typing.Any] = []
        self._recv_queue: typing.List[typing.Any] = [b"\x02", '{"type":"Welcome"}', '{"type":"Welcome"}']

    async def __aiter__(self) -> typing.AsyncIterator[typing.Any]:
        for message in _ITER_MESSAGES:
            yield message

    async def recv(self) -> typing.Any:
        return self._recv_queue.pop(0)

    async def send(self, data: typing.Any) -> None:
        self.sent.append(data)


class _FakeSyncConnectCM:
    def __init__(self, ws: _FakeSyncWS) -> None:
        self._ws = ws

    def __enter__(self) -> _FakeSyncWS:
        return self._ws

    def __exit__(self, *exc: typing.Any) -> bool:
        return False


class _FakeAsyncConnectCM:
    def __init__(self, ws: _FakeAsyncWS) -> None:
        self._ws = ws

    async def __aenter__(self) -> _FakeAsyncWS:
        return self._ws

    async def __aexit__(self, *exc: typing.Any) -> bool:
        return False


def _make_invalid_status(code: int) -> InvalidWebSocketStatus:
    exc = InvalidWebSocketStatus.__new__(InvalidWebSocketStatus)
    # Support both websockets layouts: legacy reads exc.status_code, newer reads
    # exc.response.status_code.
    exc.status_code = code  # type: ignore[attr-defined]
    exc.response = type("_Resp", (), {"status_code": code})()  # type: ignore[attr-defined]
    return exc


# (leaf client path, connect kwargs). The high-level ``connect`` reimplements the
# websocket logic inline (it does not call ``raw_client.connect``), so each
# endpoint is driven both through the high-level client and through
# ``with_raw_response`` to cover both modules.
WS_ENDPOINTS = [
    ("speak.v1", {}),
    ("agent.v1", {}),
    ("listen.v1", {"model": "nova-3"}),
    ("listen.v2", {"model": "flux-general-en"}),
]
_WS_IDS = [e[0] for e in WS_ENDPOINTS]


def _async_connect_modules(leaf: str) -> typing.List[str]:
    """The two modules that import ``websockets_client_connect`` for an endpoint."""
    return [f"deepgram.{leaf}.client", f"deepgram.{leaf}.raw_client"]


def _exercise_sync_socket(socket: typing.Any) -> None:
    socket.on(EventType.OPEN, lambda _data: None)
    socket.on(EventType.MESSAGE, lambda _data: None)
    socket.on(EventType.ERROR, lambda _data: None)
    socket.on(EventType.CLOSE, lambda _data: None)

    list(socket)  # __iter__: binary + parsed + skipped-non-json
    socket.start_listening()  # OPEN, MESSAGE(s), ERROR (non-json), CLOSE
    socket.recv()  # binary frame
    socket.recv()  # json frame

    for name in dir(socket):
        if not name.startswith("send_"):
            continue
        method = getattr(socket, name)
        try:
            method()  # send helpers with an optional/defaulted message
        except TypeError:
            method(_DummyModel())


async def _exercise_async_socket(socket: typing.Any) -> None:
    socket.on(EventType.OPEN, lambda _data: None)
    socket.on(EventType.MESSAGE, lambda _data: None)
    socket.on(EventType.ERROR, lambda _data: None)
    socket.on(EventType.CLOSE, lambda _data: None)

    async for _ in socket:  # __aiter__
        pass
    await socket.start_listening()
    await socket.recv()
    await socket.recv()

    for name in dir(socket):
        if not name.startswith("send_"):
            continue
        method = getattr(socket, name)
        try:
            await method()
        except TypeError:
            await method(_DummyModel())


@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
def test_connect_and_socket_client_sync(
    monkeypatch: pytest.MonkeyPatch, leaf: str, kwargs: typing.Dict[str, typing.Any]
) -> None:
    created: typing.List[_FakeSyncWS] = []

    def _connect(*_a: typing.Any, **_k: typing.Any) -> _FakeSyncConnectCM:
        ws = _FakeSyncWS()
        created.append(ws)
        return _FakeSyncConnectCM(ws)

    # Both client.py and raw_client.py reference the same websockets.sync.client
    # module, so a single global patch covers them.
    monkeypatch.setattr(websockets_sync_client, "connect", _connect)

    client = _sync_client()
    with _resolve(client, leaf).connect(**kwargs) as socket:  # high-level client.py
        _exercise_sync_socket(socket)
    with _resolve(client, leaf).with_raw_response.connect(**kwargs) as socket:  # raw_client.py
        _exercise_sync_socket(socket)
    # With authorization + request options, covering the auth-header, extra-header
    # and additional-query-parameter branches of connect.
    opts = {"additional_headers": {"X-Trace": "1"}, "additional_query_parameters": {"foo": "bar"}}
    with _resolve(client, leaf).connect(authorization="Token abc", request_options=opts, **kwargs):
        pass
    with _resolve(client, leaf).with_raw_response.connect(authorization="Token abc", request_options=opts, **kwargs):
        pass

    assert created and any(ws.sent for ws in created)  # send_* helpers reached the transport


@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
async def test_connect_and_socket_client_async(
    monkeypatch: pytest.MonkeyPatch, leaf: str, kwargs: typing.Dict[str, typing.Any]
) -> None:
    created: typing.List[_FakeAsyncWS] = []

    def _connect(*_a: typing.Any, **_k: typing.Any) -> _FakeAsyncConnectCM:
        ws = _FakeAsyncWS()
        created.append(ws)
        return _FakeAsyncConnectCM(ws)

    # The async connect is imported by name into both client.py and raw_client.py.
    for module in _async_connect_modules(leaf):
        monkeypatch.setattr(f"{module}.websockets_client_connect", _connect)

    client = _async_client()
    async with _resolve(client, leaf).connect(**kwargs) as socket:  # high-level client.py
        await _exercise_async_socket(socket)
    async with _resolve(client, leaf).with_raw_response.connect(**kwargs) as socket:  # raw_client.py
        await _exercise_async_socket(socket)
    opts = {"additional_headers": {"X-Trace": "1"}, "additional_query_parameters": {"foo": "bar"}}
    async with _resolve(client, leaf).connect(authorization="Token abc", request_options=opts, **kwargs):
        pass
    async with _resolve(client, leaf).with_raw_response.connect(
        authorization="Token abc", request_options=opts, **kwargs
    ):
        pass

    assert created and any(ws.sent for ws in created)


@pytest.mark.parametrize("status", [401, 500])
@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
def test_connect_invalid_status_raises_sync(
    monkeypatch: pytest.MonkeyPatch, leaf: str, kwargs: typing.Dict[str, typing.Any], status: int
) -> None:
    def _raise(*_a: typing.Any, **_k: typing.Any) -> typing.Any:
        raise _make_invalid_status(status)

    monkeypatch.setattr(websockets_sync_client, "connect", _raise)

    client = _sync_client()
    with pytest.raises(ApiError):
        with _resolve(client, leaf).connect(**kwargs):
            pass
    with pytest.raises(ApiError):
        with _resolve(client, leaf).with_raw_response.connect(**kwargs):
            pass


@pytest.mark.parametrize("status", [401, 500])
@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
async def test_connect_invalid_status_raises_async(
    monkeypatch: pytest.MonkeyPatch, leaf: str, kwargs: typing.Dict[str, typing.Any], status: int
) -> None:
    def _raise(*_a: typing.Any, **_k: typing.Any) -> typing.Any:
        raise _make_invalid_status(status)

    for module in _async_connect_modules(leaf):
        monkeypatch.setattr(f"{module}.websockets_client_connect", _raise)

    client = _async_client()
    with pytest.raises(ApiError):
        async with _resolve(client, leaf).connect(**kwargs):
            pass
    with pytest.raises(ApiError):
        async with _resolve(client, leaf).with_raw_response.connect(**kwargs):
            pass


def test_speak_audio_generate_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = list(_sync_client().speak.v1.audio.generate(text="hello"))
        assert b"".join(chunks) == b"audio-bytes"


def test_speak_audio_generate_with_request_options_sync() -> None:
    # chunk_size + timeout exercise the request_options branches in the stream path.
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = list(
            _sync_client().speak.v1.audio.generate(
                text="hello", request_options={"chunk_size": 4, "timeout_in_seconds": 5}
            )
        )
        assert b"".join(chunks) == b"audio-bytes"


async def test_speak_audio_generate_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = [chunk async for chunk in _async_client().speak.v1.audio.generate(text="hello")]
        assert b"".join(chunks) == b"audio-bytes"


async def test_speak_audio_generate_with_request_options_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(200, content=b"audio-bytes"))
        chunks = [
            chunk
            async for chunk in _async_client().speak.v1.audio.generate(
                text="hello", request_options={"chunk_size": 4, "timeout_in_seconds": 5}
            )
        ]
        assert b"".join(chunks) == b"audio-bytes"


def test_speak_audio_generate_error_sync() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"err": "bad"}))
        with pytest.raises(ApiError):
            list(_sync_client().speak.v1.audio.generate(text="hello"))


async def test_speak_audio_generate_error_async() -> None:
    with respx.mock:
        respx.route(host=HOST).mock(return_value=httpx.Response(400, json={"err": "bad"}))
        with pytest.raises(ApiError):
            [chunk async for chunk in _async_client().speak.v1.audio.generate(text="hello")]
