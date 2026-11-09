"""Regression coverage for generated WebSocket unknown-message fallbacks."""

import json

import pytest

from deepgram.agent.v1.socket_client import V1SocketClient as AgentV1SocketClient
from deepgram.listen.v1.socket_client import V1SocketClient as ListenV1SocketClient
from deepgram.listen.v2.socket_client import V2SocketClient as ListenV2SocketClient
from deepgram.speak.v1.socket_client import V1SocketClient as SpeakV1SocketClient
from deepgram.speak.v2.socket_client import V2SocketClient as SpeakV2SocketClient

_UNKNOWN_MESSAGE = {"type": "BrandNewServerEvent", "brand_new_field": 123}


class _FakeWebSocket:
    def recv(self):
        return json.dumps(_UNKNOWN_MESSAGE)


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
