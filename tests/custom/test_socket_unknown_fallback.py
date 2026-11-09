"""Regression coverage for generated WebSocket unknown-message fallbacks."""

import json

import pytest

from deepgram.agent.v1.socket_client import V1SocketClient as AgentV1SocketClient
from deepgram.listen.v1.socket_client import AsyncV1SocketClient as AsyncListenV1SocketClient
from deepgram.listen.v1.socket_client import V1SocketClient as ListenV1SocketClient
from deepgram.listen.v2.socket_client import AsyncV2SocketClient
from deepgram.listen.v2.socket_client import V2SocketClient as ListenV2SocketClient
from deepgram.speak.v1.socket_client import V1SocketClient as SpeakV1SocketClient
from deepgram.speak.v2.socket_client import V2SocketClient as SpeakV2SocketClient

_UNKNOWN_MESSAGE = {"type": "BrandNewServerEvent", "brand_new_field": 123}


class _FakeWebSocket:
    def __init__(self, message=_UNKNOWN_MESSAGE):
        self._message = json.dumps(message) if isinstance(message, dict) else message

    def recv(self):
        return self._message

    def __iter__(self):
        return iter([self._message])


class _FakeAsyncWebSocket:
    def __init__(self, message):
        self._message = message

    async def recv(self):
        return self._message

    def __aiter__(self):
        async def _messages():
            yield self._message

        return _messages()


@pytest.mark.parametrize(
    "socket_client",
    [
        AgentV1SocketClient,
        ListenV1SocketClient,
        ListenV2SocketClient,
        pytest.param(
            SpeakV1SocketClient,
            marks=pytest.mark.xfail(
                strict=True,
                reason="Fern incorrectly coerces unknown Speak V1 frames into SpeakV1Flushed; see fern-api/fern#18824.",
            ),
        ),
        SpeakV2SocketClient,
    ],
)
def test_recv_returns_unknown_server_message_as_dict(socket_client):
    message = socket_client(websocket=_FakeWebSocket()).recv()

    assert isinstance(message, dict)
    assert message == _UNKNOWN_MESSAGE


@pytest.mark.parametrize("socket_client", [ListenV1SocketClient, ListenV2SocketClient])
def test_listen_iteration_returns_binary_frames(socket_client):
    audio = b"audio-frame"

    assert list(socket_client(websocket=_FakeWebSocket(audio))) == [audio]


@pytest.mark.parametrize("socket_client", [AsyncListenV1SocketClient, AsyncV2SocketClient])
async def test_async_listen_iteration_returns_binary_frames(socket_client):
    audio = b"audio-frame"

    assert [message async for message in socket_client(websocket=_FakeAsyncWebSocket(audio))] == [audio]
