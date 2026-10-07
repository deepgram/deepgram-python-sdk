import json
from typing import Any, cast

from deepgram.core.unchecked_base_model import construct_type
from deepgram.listen import ListenV1Configure as ListenConfigure
from deepgram.listen.v1 import ListenV1Error as V1ListenError
from deepgram.listen.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.listen.v1.types import ListenV1Configure, ListenV1Error


class _FakeWebSocket:
    def __init__(self, response: dict | None = None) -> None:
        self.response = response
        self.sent: list[str] = []

    def recv(self) -> str:
        assert self.response is not None
        return json.dumps(self.response)

    def send(self, data: str) -> None:
        self.sent.append(data)


class _FakeAsyncWebSocket:
    def __init__(self, response: dict | None = None) -> None:
        self.response = response
        self.sent: list[str] = []

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


def test_listen_v1_configure_and_error_are_exported() -> None:
    assert ListenConfigure is ListenV1Configure
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
