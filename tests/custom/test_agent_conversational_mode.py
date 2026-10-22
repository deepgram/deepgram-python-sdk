import json
from typing import Any, cast

import pytest

from deepgram.agent.v1.socket_client import AsyncV1SocketClient, V1SocketClient
from deepgram.agent.v1.types import (
    AgentV1ConversationText,
    AgentV1FrustrationDetected,
    AgentV1InjectDynamicAgentMessage,
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentContext,
    AgentV1SettingsAgentContextContext,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
    AgentV1ThinkConversationalUpdated,
)
from deepgram.types import (
    DeepgramThinkConversationalProviderV1,
    ThinkConversationalSettingsV1,
    ThinkSettingsV1,
    ThinkSettingsV1FunctionsItem,
)
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi


class _FakeWebSocket:
    def __init__(self, responses: list[dict[str, Any]] | None = None) -> None:
        self._responses = responses or []
        self.sent: list[str] = []

    def recv(self) -> str:
        return json.dumps(self._responses.pop(0))

    def send(self, data: str) -> None:
        self.sent.append(data)


class _FakeAsyncWebSocket:
    def __init__(self, responses: list[dict[str, Any]] | None = None) -> None:
        self._responses = responses or []
        self.sent: list[str] = []

    async def recv(self) -> str:
        return json.dumps(self._responses.pop(0))

    async def send(self, data: str) -> None:
        self.sent.append(data)


def _settings(*, legacy: bool) -> AgentV1Settings:
    think = ThinkSettingsV1(
        provider=ThinkSettingsV1Provider_OpenAi(model="gpt-4o-mini"),
        functions=[
            ThinkSettingsV1FunctionsItem(
                name="lookup_order",
                parameters={"type": "object", "properties": {"order_id": {"type": "string"}}},
                defer_until_eot=True,
                initial_agent_filler=True,
                agent_filler_max_count=2,
                agent_filler_interval_ms=1500,
            )
        ],
    )
    think_conversational = ThinkConversationalSettingsV1(
        provider=DeepgramThinkConversationalProviderV1(
            agent_backchannel_sensitivity=0.35,
            presence_check_max_count=2,
            presence_check_interval_ms=5000,
            frustration_max_count=3,
            restricted_terms=["competitor name"],
        )
    )
    context = AgentV1SettingsAgentContextContext(messages=[])
    agent: AgentV1SettingsAgent | AgentV1SettingsAgentContext
    if legacy:
        agent = AgentV1SettingsAgent(
            context=AgentV1SettingsAgentContext(messages=[]),
            think=think,
            think_conversational=think_conversational,
        )
    else:
        agent = AgentV1SettingsAgentContext(
            context=context,
            think=think,
            think_conversational=think_conversational,
        )
    return AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
        agent=agent,
    )


def _assert_settings_payload(payload: dict[str, Any]) -> None:
    assert payload["type"] == "Settings"
    provider = payload["agent"]["think_conversational"]["provider"]
    assert provider == {
        "type": "deepgram",
        "version": "v1",
        "agent_backchannel_sensitivity": 0.35,
        "presence_check_max_count": 2,
        "presence_check_interval_ms": 5000,
        "frustration_max_count": 3,
        "restricted_terms": ["competitor name"],
    }

    function = payload["agent"]["think"]["functions"][0]
    assert function["defer_until_eot"] is True
    assert function["initial_agent_filler"] is True
    assert function["agent_filler_max_count"] == 2
    assert function["agent_filler_interval_ms"] == 1500


def test_sync_settings_serializes_conversational_mode_and_legacy_settings_shape() -> None:
    legacy_settings = _settings(legacy=True)
    canonical_settings = _settings(legacy=False)
    websocket = _FakeWebSocket()

    V1SocketClient(websocket=cast(Any, websocket)).send_settings(legacy_settings)

    payload = json.loads(websocket.sent[0])
    assert legacy_settings.dict() == canonical_settings.dict()
    _assert_settings_payload(payload)


async def test_async_settings_serializes_conversational_mode() -> None:
    websocket = _FakeAsyncWebSocket()

    await AsyncV1SocketClient(websocket=cast(Any, websocket)).send_settings(_settings(legacy=False))

    _assert_settings_payload(json.loads(websocket.sent[0]))


@pytest.mark.parametrize("behavior", [None, "default", "queue", "interrupt"])
def test_sync_dynamic_agent_message_serializes_default_and_behavior_payloads(behavior: str | None) -> None:
    websocket = _FakeWebSocket()

    V1SocketClient(websocket=cast(Any, websocket)).send_inject_dynamic_agent_message(
        AgentV1InjectDynamicAgentMessage(behavior=behavior)
    )

    assert json.loads(websocket.sent[0]) == {
        "type": "InjectAgentMessage",
        "is_dynamic": True,
        "behavior": behavior,
    }


@pytest.mark.parametrize("behavior", [None, "default", "queue", "interrupt"])
async def test_async_dynamic_agent_message_serializes_default_and_behavior_payloads(behavior: str | None) -> None:
    websocket = _FakeAsyncWebSocket()

    await AsyncV1SocketClient(websocket=cast(Any, websocket)).send_inject_dynamic_agent_message(
        AgentV1InjectDynamicAgentMessage(behavior=behavior)
    )

    assert json.loads(websocket.sent[0]) == {
        "type": "InjectAgentMessage",
        "is_dynamic": True,
        "behavior": behavior,
    }


def _response_frames() -> list[dict[str, Any]]:
    return [
        {"type": "ThinkConversationalUpdated"},
        {"type": "FrustrationDetected", "count": 3, "escalated": True},
        {"type": "ConversationText", "role": "assistant", "content": "One moment.", "conversational_behavior": "filler"},
    ]


def _assert_conversational_responses(responses: list[Any]) -> None:
    updated, frustration, conversation_text = responses
    assert isinstance(updated, AgentV1ThinkConversationalUpdated)
    assert isinstance(frustration, AgentV1FrustrationDetected)
    assert frustration.count == 3
    assert frustration.escalated is True
    assert isinstance(conversation_text, AgentV1ConversationText)
    assert conversation_text.conversational_behavior == "filler"


def test_sync_conversational_mode_response_frames_parse_from_socket() -> None:
    client = V1SocketClient(websocket=cast(Any, _FakeWebSocket(_response_frames())))

    _assert_conversational_responses([client.recv(), client.recv(), client.recv()])


async def test_async_conversational_mode_response_frames_parse_from_socket() -> None:
    client = AsyncV1SocketClient(websocket=cast(Any, _FakeAsyncWebSocket(_response_frames())))

    _assert_conversational_responses([await client.recv(), await client.recv(), await client.recv()])
