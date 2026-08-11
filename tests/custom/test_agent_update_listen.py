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
from deepgram.agent.v1.types.agent_v1update_listen_listen_provider import (
    AgentV1UpdateListenListenProvider_V1,
    AgentV1UpdateListenListenProvider_V2,
)
from deepgram.core.unchecked_base_model import construct_type
from deepgram.types.deepgram_listen_provider_v1 import DeepgramListenProviderV1
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
        # The legacy (unversioned) provider must be coerced to the v2 member of
        # the AgentV1UpdateListenListenProvider union added in the 2026-07-31
        # regen -- that coercion is the frozen patch on
        # agent_v1update_listen_listen.py.
        assert sent["listen"]["provider"]["version"] == "v2"

    def test_legacy_v1_provider_is_coerced_to_v1_member(self):
        ws = _FakeWebSocket()
        message = AgentV1UpdateListen(
            listen=AgentV1UpdateListenListen(provider=DeepgramListenProviderV1(model="nova-3"))
        )
        V1SocketClient(websocket=ws).send_update_listen(message)

        provider = _sent_json(ws)["listen"]["provider"]
        assert provider["version"] == "v1"
        assert provider["model"] == "nova-3"

    def test_legacy_dict_provider_is_coerced(self):
        ws = _FakeWebSocket()
        message = AgentV1UpdateListen(
            listen=AgentV1UpdateListenListen(provider={"type": "deepgram", "model": "flux-general-en"})
        )
        V1SocketClient(websocket=ws).send_update_listen(message)

        provider = _sent_json(ws)["listen"]["provider"]
        assert provider["version"] == "v2"
        assert provider["model"] == "flux-general-en"

    def test_native_union_v2_provider_round_trips(self):
        # The generator-native form must keep working alongside the legacy shim.
        ws = _FakeWebSocket()
        message = AgentV1UpdateListen(
            listen=AgentV1UpdateListenListen(
                provider=AgentV1UpdateListenListenProvider_V2(
                    model="flux-general-en", language_hints=["en"], eot_threshold=0.8
                )
            )
        )
        V1SocketClient(websocket=ws).send_update_listen(message)

        provider = _sent_json(ws)["listen"]["provider"]
        assert provider["version"] == "v2"
        assert provider["model"] == "flux-general-en"
        assert provider["language_hints"] == ["en"]
        assert provider["eot_threshold"] == 0.8

    def test_native_union_v1_provider_round_trips(self):
        ws = _FakeWebSocket()
        message = AgentV1UpdateListen(
            listen=AgentV1UpdateListenListen(
                provider=AgentV1UpdateListenListenProvider_V1(model="nova-3", smart_format=True)
            )
        )
        V1SocketClient(websocket=ws).send_update_listen(message)

        provider = _sent_json(ws)["listen"]["provider"]
        assert provider["version"] == "v1"
        assert provider["model"] == "nova-3"
        assert provider["smart_format"] is True


class TestListenUpdatedResponse:
    def test_resolves_from_response_union(self):
        obj = construct_type(type_=V1SocketClientResponse, object_={"type": "ListenUpdated"})
        assert isinstance(obj, AgentV1ListenUpdated)
        assert obj.type == "ListenUpdated"
