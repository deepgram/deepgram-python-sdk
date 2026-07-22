"""
Coverage for the Voice Agent mid-session listen-reconfigure surface added in the
2026-07-08 regen:

  * ``send_update_listen(AgentV1UpdateListen(...))`` — client-sent control message
    that serializes to ``{"type": "UpdateListen", "listen": {"provider": {...}}}``.
  * ``AgentV1ListenUpdated`` — the server acknowledgement, which must resolve out
    of the agent socket response union via its ``type`` discriminant.

Driven with a fake websocket / construct_type — no network.
"""

import json

from deepgram.agent.v1.socket_client import V1SocketClient, V1SocketClientResponse
from deepgram.agent.v1.types.agent_v1listen_updated import AgentV1ListenUpdated
from deepgram.agent.v1.types.agent_v1update_listen import AgentV1UpdateListen
from deepgram.agent.v1.types.agent_v1update_listen_listen import AgentV1UpdateListenListen
from deepgram.core.unchecked_base_model import construct_type
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2


class _FakeWebSocket:
    def __init__(self):
        self.sent = []

    def send(self, data):
        self.sent.append(data)


def _sent_json(ws):
    assert len(ws.sent) == 1
    payload = ws.sent[0]
    return json.loads(payload) if isinstance(payload, str) else payload


class TestSendUpdateListen:
    def test_serializes_provider_on_the_wire(self):
        ws = _FakeWebSocket()
        message = AgentV1UpdateListen(
            listen=AgentV1UpdateListenListen(provider=DeepgramListenProviderV2(model="flux-general-en"))
        )
        V1SocketClient(websocket=ws).send_update_listen(message)

        sent = _sent_json(ws)
        assert sent["type"] == "UpdateListen"
        assert sent["listen"]["provider"]["type"] == "deepgram"
        assert sent["listen"]["provider"]["model"] == "flux-general-en"


class TestListenUpdatedResponse:
    def test_resolves_from_response_union(self):
        obj = construct_type(type_=V1SocketClientResponse, object_={"type": "ListenUpdated"})
        assert isinstance(obj, AgentV1ListenUpdated)
        assert obj.type == "ListenUpdated"
