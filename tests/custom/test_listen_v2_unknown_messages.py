"""Regression tests for forward-compatible Listen V2 response parsing."""

import json

from deepgram.core.events import EventType
from deepgram.listen.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.listen.v2.types.listen_v2warning import ListenV2Warning

UNKNOWN_RESPONSE = {
    "type": "FutureMessage",
    "request_id": "req-123",
    "sequence_id": 4,
    "details": {"reason": "new server feature", "values": [1, 2]},
}

WARNING_RESPONSE = {
    "type": "Warning",
    "request_id": "req-123",
    "sequence_id": 5,
    "code": "FORCE_END_TURN_NO_ACTIVE_TURN",
    "description": "There is no active turn.",
}


class _SyncWebSocket:
    def __init__(self, messages):
        self.messages = list(messages)

    def __iter__(self):
        return iter(self.messages)

    def recv(self):
        return self.messages.pop(0)


class _AsyncWebSocket:
    def __init__(self, messages):
        self.messages = list(messages)

    async def __aiter__(self):
        for message in self.messages:
            yield message

    async def recv(self):
        return self.messages.pop(0)


def test_sync_iterator_returns_unknown_response_as_raw_json():
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert list(client) == [UNKNOWN_RESPONSE]


async def test_async_iterator_returns_unknown_response_as_raw_json():
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert [message async for message in client] == [UNKNOWN_RESPONSE]


def test_sync_listener_emits_unknown_response_as_raw_json():
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))
    received = []
    client.on(EventType.MESSAGE, received.append)

    client.start_listening()

    assert received == [UNKNOWN_RESPONSE]


async def test_async_listener_emits_unknown_response_as_raw_json():
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))
    received = []
    client.on(EventType.MESSAGE, received.append)

    await client.start_listening()

    assert received == [UNKNOWN_RESPONSE]


def test_sync_recv_returns_unknown_response_as_raw_json_without_logging_payload(caplog):
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert client.recv() == UNKNOWN_RESPONSE
    assert "unrecognized Listen V2 response" in caplog.text
    assert "new server feature" not in caplog.text


async def test_async_recv_returns_unknown_response_as_raw_json():
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert await client.recv() == UNKNOWN_RESPONSE


def test_sync_recv_keeps_known_warning_typed():
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(WARNING_RESPONSE)]))

    response = client.recv()

    assert isinstance(response, ListenV2Warning)
    assert response.code == WARNING_RESPONSE["code"]


async def test_async_recv_keeps_known_warning_typed():
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(WARNING_RESPONSE)]))

    response = await client.recv()

    assert isinstance(response, ListenV2Warning)
    assert response.code == WARNING_RESPONSE["code"]


def test_sync_iterator_passes_through_binary_frame():
    frame = b"audio-frame"
    client = V2SocketClient(websocket=_SyncWebSocket([frame]))

    assert list(client) == [frame]


async def test_async_iterator_passes_through_binary_frame():
    frame = b"audio-frame"
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([frame]))

    assert [message async for message in client] == [frame]


def test_sync_iterator_keeps_skipping_decoder_exceptions(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert list(client) == []


async def test_async_iterator_keeps_skipping_decoder_exceptions(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert [message async for message in client] == []


def test_sync_listener_keeps_skipping_decoder_exceptions(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)
    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))
    received = []
    errors = []
    client.on(EventType.MESSAGE, received.append)
    client.on(EventType.ERROR, errors.append)

    client.start_listening()

    assert received == []
    assert errors == []


async def test_async_listener_keeps_skipping_decoder_exceptions(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))
    received = []
    errors = []
    client.on(EventType.MESSAGE, received.append)
    client.on(EventType.ERROR, errors.append)

    await client.start_listening()

    assert received == []
    assert errors == []


def test_sync_recv_keeps_returning_raw_json_when_decoder_raises(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)

    client = V2SocketClient(websocket=_SyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert client.recv() == UNKNOWN_RESPONSE


async def test_async_recv_keeps_returning_raw_json_when_decoder_raises(monkeypatch):
    import deepgram.listen.v2.socket_client as socket_client_module

    def fail_decoder(**kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(socket_client_module, "construct_type", fail_decoder)
    client = AsyncV2SocketClient(websocket=_AsyncWebSocket([json.dumps(UNKNOWN_RESPONSE)]))

    assert await client.recv() == UNKNOWN_RESPONSE
