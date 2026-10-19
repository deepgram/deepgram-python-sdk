import json
from typing import Any, cast

from deepgram.core.events import EventType
from deepgram.core.unchecked_base_model import construct_type
from deepgram.listen import (
    ListenV1Configure as ListenConfigure,
)
from deepgram.listen import (
    ListenV1ConfigureFailure as V1ListenConfigureFailure,
)
from deepgram.listen import (
    ListenV1ConfigureSuccess as V1ListenConfigureSuccess,
)
from deepgram.listen.v1 import ListenV1Error as V1ListenError
from deepgram.listen.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.listen.v1.types import (
    ListenV1Configure,
    ListenV1ConfigureFailure,
    ListenV1ConfigureSuccess,
    ListenV1Error,
)


class _FakeWebSocket:
    def __init__(self, response: dict | None = None, messages: list[dict] | None = None) -> None:
        self.response = response
        self.messages = messages or []
        self.sent: list[str] = []

    def __iter__(self):
        return iter(json.dumps(message) for message in self.messages)

    def recv(self) -> str:
        assert self.response is not None
        return json.dumps(self.response)

    def send(self, data: str) -> None:
        self.sent.append(data)


class _FakeAsyncWebSocket:
    def __init__(self, response: dict | None = None, messages: list[dict] | None = None) -> None:
        self.response = response
        self.messages = messages or []
        self.sent: list[str] = []

    def __aiter__(self):
        return self

    async def __anext__(self) -> str:
        if not self.messages:
            raise StopAsyncIteration
        return json.dumps(self.messages.pop(0))

    async def recv(self) -> str:
        assert self.response is not None
        return json.dumps(self.response)

    async def send(self, data: str) -> None:
        self.sent.append(data)


def _error_payload() -> dict:
    return {
        "type": "Error",
        "variant": "InvalidConfigureMessage",
        "description": "Keyterms require a Nova-3 model.",
        "code": "KeytermsNotSupported",
    }


def _configure_success_payload() -> dict:
    return {
        "type": "ConfigureSuccess",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "keyterms": ["Deepgram", "customer service"],
    }


def _configure_failure_payload() -> dict:
    return {
        "type": "ConfigureFailure",
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "code": "CONFIGURE_KEYTERM_LIMIT_EXCEEDED",
        "description": "The keyterms exceed the 500-token keyterm limit.",
    }


def test_listen_v1_configure_and_error_are_exported() -> None:
    assert ListenConfigure is ListenV1Configure
    assert V1ListenConfigureSuccess is ListenV1ConfigureSuccess
    assert V1ListenConfigureFailure is ListenV1ConfigureFailure
    assert V1ListenError is ListenV1Error


def test_sync_configure_serializes_empty_keyterms_and_features() -> None:
    websocket = _FakeWebSocket()

    V1SocketClient(websocket=cast(Any, websocket)).send_configure(
        ListenV1Configure(keyterms=[], features={"numerals": True})
    )

    assert json.loads(websocket.sent[0]) == {"type": "Configure", "keyterms": [], "features": {"numerals": True}}


async def test_async_configure_serializes_empty_keyterms_and_features() -> None:
    websocket = _FakeAsyncWebSocket()

    await AsyncV1SocketClient(websocket=cast(Any, websocket)).send_configure(
        ListenV1Configure(keyterms=[], features={"numerals": True})
    )

    assert json.loads(websocket.sent[0]) == {"type": "Configure", "keyterms": [], "features": {"numerals": True}}


def test_sync_listen_v1_error_parses_from_socket_union_and_recv() -> None:
    parsed = construct_type(type_=cast(Any, V1SocketClientResponse), object_=_error_payload())
    assert isinstance(parsed, ListenV1Error)
    assert parsed.code == "KeytermsNotSupported"

    received = V1SocketClient(websocket=cast(Any, _FakeWebSocket(_error_payload()))).recv()
    assert isinstance(received, ListenV1Error)
    assert received.description == "Keyterms require a Nova-3 model."


async def test_async_listen_v1_error_parses_from_recv() -> None:
    received = await AsyncV1SocketClient(websocket=cast(Any, _FakeAsyncWebSocket(_error_payload()))).recv()

    assert isinstance(received, ListenV1Error)
    assert received.variant == "InvalidConfigureMessage"


def test_sync_listen_v1_configure_responses_parse_from_socket_union_and_recv() -> None:
    success = construct_type(type_=cast(Any, V1SocketClientResponse), object_=_configure_success_payload())
    assert isinstance(success, ListenV1ConfigureSuccess)
    assert success.keyterms == ["Deepgram", "customer service"]

    failure = V1SocketClient(websocket=cast(Any, _FakeWebSocket(_configure_failure_payload()))).recv()
    assert isinstance(failure, ListenV1ConfigureFailure)
    assert failure.code == "CONFIGURE_KEYTERM_LIMIT_EXCEEDED"


async def test_async_listen_v1_configure_responses_parse_from_socket_union_and_recv() -> None:
    success = await AsyncV1SocketClient(websocket=cast(Any, _FakeAsyncWebSocket(_configure_success_payload()))).recv()
    assert isinstance(success, ListenV1ConfigureSuccess)
    assert success.request_id == "550e8400-e29b-41d4-a716-446655440000"

    failure = await AsyncV1SocketClient(websocket=cast(Any, _FakeAsyncWebSocket(_configure_failure_payload()))).recv()
    assert isinstance(failure, ListenV1ConfigureFailure)
    assert failure.description == "The keyterms exceed the 500-token keyterm limit."


def test_sync_start_listening_emits_configure_responses() -> None:
    websocket = _FakeWebSocket(messages=[_configure_success_payload(), _configure_failure_payload()])
    client = V1SocketClient(websocket=cast(Any, websocket))
    received: list[V1SocketClientResponse] = []
    client.on(EventType.MESSAGE, received.append)

    client.start_listening()

    assert isinstance(received[0], ListenV1ConfigureSuccess)
    assert isinstance(received[1], ListenV1ConfigureFailure)


async def test_async_start_listening_emits_configure_responses() -> None:
    websocket = _FakeAsyncWebSocket(messages=[_configure_success_payload(), _configure_failure_payload()])
    client = AsyncV1SocketClient(websocket=cast(Any, websocket))
    received: list[V1SocketClientResponse] = []
    client.on(EventType.MESSAGE, received.append)

    await client.start_listening()

    assert isinstance(received[0], ListenV1ConfigureSuccess)
    assert isinstance(received[1], ListenV1ConfigureFailure)
