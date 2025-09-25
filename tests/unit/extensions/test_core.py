import asyncio
import json
import time
from typing import Any, Iterator, List, Optional

import httpx
import pytest
import websockets

from deepgram.core.events import EventEmitterMixin, EventType
from deepgram.core.http_client import HttpClient as GeneratedHttpClient
from deepgram.extensions.core.binary_message_mixin import BinaryMessageMixin
from deepgram.extensions.core.instrumented_http import (
    HttpEvents,
    InstrumentedAsyncHttpClient,
    InstrumentedHttpClient,
)
from deepgram.extensions.core.instrumented_socket_client import (
    _InstrumentedAsyncBase,
    _InstrumentedSyncBase,
)
from deepgram.extensions.core.socket_instrumentation import install_socket_instrumentation
from deepgram.extensions.core.socket_send_mixins import (
    AgentSocketSendMixinAsync,
    AgentSocketSendMixinSync,
    ListenSocketSendMixinAsync,
    ListenSocketSendMixinSync,
    SpeakSocketSendMixinAsync,
    SpeakSocketSendMixinSync,
)
from deepgram.extensions.types.sockets import (
    AgentSocketClientResponse,
    ListenSocketClientResponse,
    SpeakSocketClientResponse,
    SpeakV1MetadataEvent,
    SpeakV1TextMessage,
)


class _FakeWebSocketSync:
    def __init__(self, messages: List[Any], *, raise_after: Optional[BaseException] = None) -> None:
        self._messages = list(messages)
        self._send_data: List[Any] = []
        self._raise_after = raise_after

    def __iter__(self) -> Iterator[Any]:
        for idx, m in enumerate(self._messages):
            yield m
            if self._raise_after is not None and idx == len(self._messages) - 1:
                raise self._raise_after

    def recv(self) -> Any:
        if not self._messages:
            raise StopIteration()
        return self._messages.pop(0)

    def send(self, data: Any) -> None:
        self._send_data.append(data)


class _FakeWebSocketAsync:
    def __init__(self, messages: List[Any], *, raise_after: Optional[BaseException] = None) -> None:
        self._messages = list(messages)
        self._send_data: List[Any] = []
        self._raise_after = raise_after
        self._iter_index = 0

    def __aiter__(self):
        self._iter_index = 0
        return self

    async def __anext__(self):
        if self._iter_index >= len(self._messages):
            raise StopAsyncIteration
        value = self._messages[self._iter_index]
        self._iter_index += 1
        # Raise after yielding the last message if configured
        if self._raise_after is not None and self._iter_index == len(self._messages):
            # Give consumer a tick to process current value before raising on next iteration
            exc = self._raise_after
            self._raise_after = None
            return value
        return value

    async def recv(self) -> Any:
        if not self._messages:
            raise StopAsyncIteration
        return self._messages.pop(0)

    async def send(self, data: Any) -> None:
        self._send_data.append(data)


class _EventsCollector(HttpEvents):
    def __init__(self) -> None:
        self.requests: List[tuple[str, str]] = []
        self.responses: List[tuple[str, str, int]] = []
        self.errors: List[tuple[str, str, BaseException]] = []

    def on_http_request(self, *, method: str, url: str, headers: dict | None) -> None:
        self.requests.append((method, url))

    def on_http_response(self, *, method: str, url: str, status_code: int, duration_ms: float, headers: dict | None) -> None:
        self.responses.append((method, url, status_code))

    def on_http_error(self, *, method: str, url: str, error: BaseException, duration_ms: float) -> None:
        self.errors.append((method, url, error))


def _base_http_client(transport: httpx.BaseTransport) -> GeneratedHttpClient:
    return GeneratedHttpClient(
        httpx_client=httpx.Client(transport=transport),
        base_timeout=lambda: 5.0,
        base_headers=lambda: {"x-test": "1"},
        base_url=lambda: "https://example.com",
    )


def test_binary_message_mixin_processing_and_send_sync():
    class Dummy(BinaryMessageMixin, EventEmitterMixin):
        pass

    dummy = Dummy()
    # JSON path with concrete model
    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="m",
        model_version="v",
        model_uuid="u",
    )
    raw_json = json.dumps(meta.dict())
    parsed, is_bin = dummy._process_message(raw_json, SpeakSocketClientResponse)
    assert not is_bin
    assert isinstance(parsed, SpeakV1MetadataEvent)

    # Binary path
    payload = b"abc"
    parsed_b, is_bin_b = dummy._process_message(payload, SpeakSocketClientResponse)
    assert is_bin_b and parsed_b == payload

    # Send helpers
    ws = _FakeWebSocketSync([])
    dummy._send_binary_or_json(ws, payload)
    dummy._send_binary_or_json(ws, {"foo": "bar"})
    dummy._send_binary_or_json(ws, "str")
    assert ws._send_data[0] == payload
    assert ws._send_data[1] == json.dumps({"foo": "bar"})
    assert ws._send_data[2] == "str"


def test_binary_message_mixin_invalid_json_raises():
    class Dummy(BinaryMessageMixin):
        pass

    with pytest.raises(json.JSONDecodeError):
        Dummy()._handle_json_message("not-json", SpeakSocketClientResponse)


def test_instrumented_http_calls_events_success_and_error():
    # Success transport
    def ok_handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("https://example.com/test")
        return httpx.Response(200, json={"ok": True})

    base = _base_http_client(httpx.MockTransport(ok_handler))
    collector = _EventsCollector()
    client = InstrumentedHttpClient(delegate=base, events=collector)
    resp = client.request(path="test", method="GET")
    assert resp.status_code == 200
    assert collector.requests and collector.responses and not collector.errors

    # Error transport
    def err_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom")

    base_err = _base_http_client(httpx.MockTransport(err_handler))
    collector_err = _EventsCollector()
    client_err = InstrumentedHttpClient(delegate=base_err, events=collector_err)
    with pytest.raises(httpx.ConnectError):
        client_err.request(path="test", method="GET")
    assert collector_err.errors and collector_err.requests


@pytest.mark.asyncio
async def test_instrumented_async_http_calls_events_success():
    def ok_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(204)

    base = GeneratedHttpClient(
        httpx_client=httpx.Client(transport=httpx.MockTransport(ok_handler)),
        base_timeout=lambda: 5.0,
        base_headers=lambda: {},
        base_url=lambda: "https://example.com",
    )
    async_base = type("AsyncDelegate", (), {"httpx_client": httpx.AsyncClient(transport=httpx.MockTransport(ok_handler)), "base_timeout": lambda: 5.0, "base_headers": lambda: {}, "base_url": lambda: "https://example.com"})
    # Build a real async delegate using the generated AsyncHttpClient for correctness
    async_delegate = InstrumentedAsyncHttpClient.__mro__[1](  # GeneratedAsyncHttpClient class
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(ok_handler)),
        base_timeout=lambda: 5.0,
        base_headers=lambda: {},
        base_url=lambda: "https://example.com",
    )
    collector = _EventsCollector()
    client = InstrumentedAsyncHttpClient(delegate=async_delegate, events=collector)
    resp = await client.request(path="ping", method="GET")
    assert resp.status_code == 204
    assert collector.requests and collector.responses


def test_instrumented_sync_socket_events_and_iteration():
    class TestClient(_InstrumentedSyncBase):
        _response_type = SpeakSocketClientResponse

    # Include a JSON message and a binary message
    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="m",
        model_version="v",
        model_uuid="u",
    )
    ws = _FakeWebSocketSync([json.dumps(meta.dict()), b"bytes"])  # type: ignore[arg-type]
    client = TestClient(websocket=ws, events=None)

    messages: list[Any] = []
    opens: list[Any] = []
    closes: list[Any] = []
    client.on(EventType.MESSAGE, lambda m: messages.append(m))
    client.on(EventType.OPEN, lambda m: opens.append(m))
    client.on(EventType.CLOSE, lambda m: closes.append(m))

    client.start_listening()
    assert len(opens) == 1 and len(closes) == 1
    assert any(isinstance(m, SpeakV1MetadataEvent) for m in messages)
    assert any(isinstance(m, (bytes, bytearray)) for m in messages)

    # Send model uses dict(exclude_unset=True, exclude_none=True)
    txt = SpeakV1TextMessage(type="Speak", text="hello")
    client._send_model(txt)
    assert json.loads(ws._send_data[-1]) == txt.dict(exclude_unset=True, exclude_none=True)


@pytest.mark.asyncio
async def test_instrumented_async_socket_events_and_iteration():
    class TestClient(_InstrumentedAsyncBase):
        _response_type = SpeakSocketClientResponse

    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="m",
        model_version="v",
        model_uuid="u",
    )
    ws = _FakeWebSocketAsync([json.dumps(meta.dict()), b"bytes"])  # type: ignore[arg-type]
    client = TestClient(websocket=ws, events=None)

    messages: list[Any] = []
    opens: list[Any] = []
    closes: list[Any] = []

    client.on(EventType.MESSAGE, lambda m: messages.append(m))
    client.on(EventType.OPEN, lambda m: opens.append(m))
    client.on(EventType.CLOSE, lambda m: closes.append(m))

    await client.start_listening()
    assert len(opens) == 1 and len(closes) == 1
    assert any(isinstance(m, SpeakV1MetadataEvent) for m in messages)
    assert any(isinstance(m, (bytes, bytearray)) for m in messages)

    # Send helpers
    await client._send({"a": 1})
    await client._send(b"bin")
    assert isinstance(ws._send_data[0], str) and isinstance(ws._send_data[1], (bytes, bytearray))


def test_instrumented_socket_emits_error_on_exception():
    class TestClient(_InstrumentedSyncBase):
        _response_type = SpeakSocketClientResponse

    meta = SpeakV1MetadataEvent(
        type="Metadata",
        request_id="r1",
        model_name="m",
        model_version="v",
        model_uuid="u",
    )
    ws = _FakeWebSocketSync([json.dumps(meta.dict())], raise_after=websockets.WebSocketException("err"))  # type: ignore[arg-type]
    client = TestClient(websocket=ws, events=None)
    errors: list[Any] = []
    client.on(EventType.ERROR, lambda e: errors.append(e))
    client.start_listening()
    assert errors and isinstance(errors[0], websockets.WebSocketException)

    # ConnectionClosedOK should not emit error
    ws_ok = _FakeWebSocketSync([json.dumps(meta.dict())], raise_after=websockets.exceptions.ConnectionClosedOK(None, None))  # type: ignore[arg-type]
    client_ok = TestClient(websocket=ws_ok, events=None)
    errs: list[Any] = []
    client_ok.on(EventType.ERROR, lambda e: errs.append(e))
    client_ok.start_listening()
    assert not errs


def test_socket_send_mixins_invoke_send_model_sync_and_async():
    # Sync
    class DummySender(AgentSocketSendMixinSync, ListenSocketSendMixinSync, SpeakSocketSendMixinSync):
        def __init__(self) -> None:
            self.sent: list[Any] = []

        def _send_model(self, data: Any) -> None:  # type: ignore[override]
            self.sent.append(data)

    d = DummySender()
    d.send_text(SpeakV1TextMessage(type="Speak", text="hi"))
    assert d.sent and d.sent[0].dict()["text"] == "hi"

    # Async
    class DummySenderAsync(AgentSocketSendMixinAsync, ListenSocketSendMixinAsync, SpeakSocketSendMixinAsync):
        def __init__(self) -> None:
            self.sent: list[Any] = []

        async def _send_model(self, data: Any) -> None:  # type: ignore[override]
            self.sent.append(data)

    async def _run() -> None:
        d2 = DummySenderAsync()
        await d2.send_text(SpeakV1TextMessage(type="Speak", text="yo"))
        assert d2.sent and d2.sent[0].dict()["text"] == "yo"

    asyncio.get_event_loop().run_until_complete(_run())


def test_socket_instrumentation_monkey_patches_clients_and_mros():
    # Install once; should not raise
    install_socket_instrumentation(base_package="deepgram", events=None)

    from deepgram.speak.client import AsyncSpeakSocketClient, SpeakSocketClient

    # Classes should have _response_type set to union alias and include mixins in MRO
    assert getattr(SpeakSocketClient, "_response_type", None) is SpeakSocketClientResponse
    assert any(c.__name__ == "_InstrumentedSyncBase" for c in SpeakSocketClient.__mro__)
    assert any(c.__name__ == "SpeakSocketSendMixinSync" for c in SpeakSocketClient.__mro__)

    # Instantiate and exercise send method
    ws = _FakeWebSocketSync([])
    client = SpeakSocketClient(websocket=ws)
    msg = SpeakV1TextMessage(type="Speak", text="hello")
    client.send_text(msg)  # type: ignore[attr-defined]
    assert json.loads(ws._send_data[-1])["text"] == "hello"


