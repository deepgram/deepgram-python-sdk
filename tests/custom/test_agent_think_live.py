import json
from typing import Any, cast

import pytest

from deepgram import DeepgramThinkProvider
from deepgram.agent.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.agent.v1.types.agent_v1conversation_text import AgentV1ConversationText
from deepgram.agent.v1.types.agent_v1frustration_detected import AgentV1FrustrationDetected
from deepgram.agent.v1.types.agent_v1inject_dynamic_agent_message import AgentV1InjectDynamicAgentMessage
from deepgram.agent.v1.types.agent_v1settings import AgentV1Settings
from deepgram.agent.v1.types.agent_v1settings_agent import AgentV1SettingsAgent
from deepgram.agent.v1.types.agent_v1settings_applied import AgentV1SettingsApplied
from deepgram.agent.v1.types.agent_v1settings_audio import AgentV1SettingsAudio
from deepgram.agent.v1.types.agent_v1settings_audio_input import AgentV1SettingsAudioInput
from deepgram.agent.v1.types.agent_v1think_live_updated import AgentV1ThinkLiveUpdated
from deepgram.agent.v1.types.agent_v1update_think_live import AgentV1UpdateThinkLive
from deepgram.core.unchecked_base_model import construct_type
from deepgram.types.deepgram_think_live_provider_v1 import DeepgramThinkLiveProviderV1
from deepgram.types.think_live_settings_v1 import ThinkLiveSettingsV1
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1functions_item import ThinkSettingsV1FunctionsItem
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_Deepgram, ThinkSettingsV1Provider_OpenAi


class _FakeWebSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []

    def send(self, data: str) -> None:
        self.sent.append(data)


class _FakeAsyncWebSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []

    async def send(self, data: str) -> None:
        self.sent.append(data)


def _think_live_settings() -> ThinkLiveSettingsV1:
    return ThinkLiveSettingsV1(
        provider=DeepgramThinkLiveProviderV1(
            agent_backchannel_sensitivity=0.4,
            presence_check_max_count=3,
            presence_check_interval_ms=5000,
            frustration_max_count=2,
            restricted_terms=["forbidden phrase"],
        )
    )


def _settings_with_think_live() -> AgentV1Settings:
    return AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
        agent=AgentV1SettingsAgent(
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini"),
                functions=[
                    ThinkSettingsV1FunctionsItem(
                        name="lookup_order",
                        defer_until_eot=True,
                        initial_agent_filler=True,
                        agent_filler_max_count=2,
                        agent_filler_interval_ms=3000,
                    )
                ]
            ),
            think_live=_think_live_settings(),
            messages=[{"type": "History", "role": "user", "content": "Hello"}],
        ),
    )


def _settings_with_deepgram_think() -> AgentV1Settings:
    return AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
        agent=AgentV1SettingsAgent(
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_Deepgram(
                    type="deepgram",
                    version="v1",
                    model="phonellm-mini-alpha-2-fp8",
                    temperature=0.2,
                    reasoning_mode="none",
                )
            )
        ),
    )


def _sent_json(websocket: _FakeWebSocket | _FakeAsyncWebSocket) -> dict[str, Any]:
    assert len(websocket.sent) == 1
    return json.loads(websocket.sent[0])


def test_sync_think_live_settings_and_update_serialize() -> None:
    settings_websocket = _FakeWebSocket()
    V1SocketClient(websocket=cast(Any, settings_websocket)).send_settings(_settings_with_think_live())

    settings = _sent_json(settings_websocket)
    assert settings["agent"]["think_live"]["provider"] == {
        "type": "deepgram",
        "version": "v1",
        "agent_backchannel_sensitivity": 0.4,
        "presence_check_max_count": 3,
        "presence_check_interval_ms": 5000,
        "frustration_max_count": 2,
        "restricted_terms": ["forbidden phrase"],
    }
    assert settings["agent"]["think"]["functions"] == [
        {
            "name": "lookup_order",
            "defer_until_eot": True,
            "initial_agent_filler": True,
            "agent_filler_max_count": 2,
            "agent_filler_interval_ms": 3000,
        }
    ]
    assert settings["agent"]["context"]["messages"][0]["content"] == "Hello"

    update_websocket = _FakeWebSocket()
    V1SocketClient(websocket=cast(Any, update_websocket)).send_update_think_live(
        AgentV1UpdateThinkLive(think_live=_think_live_settings())
    )
    assert _sent_json(update_websocket) == {
        "type": "UpdateThink_Live",
        "think_live": {
            "provider": {
                "type": "deepgram",
                "version": "v1",
                "agent_backchannel_sensitivity": 0.4,
                "presence_check_max_count": 3,
                "presence_check_interval_ms": 5000,
                "frustration_max_count": 2,
                "restricted_terms": ["forbidden phrase"],
            }
        },
    }


async def test_async_think_live_settings_and_update_serialize() -> None:
    settings_websocket = _FakeAsyncWebSocket()
    client = AsyncV1SocketClient(websocket=cast(Any, settings_websocket))
    await client.send_settings(_settings_with_think_live())

    settings = _sent_json(settings_websocket)
    assert settings["agent"]["think_live"]["provider"] == {
        "type": "deepgram",
        "version": "v1",
        "agent_backchannel_sensitivity": 0.4,
        "presence_check_max_count": 3,
        "presence_check_interval_ms": 5000,
        "frustration_max_count": 2,
        "restricted_terms": ["forbidden phrase"],
    }
    assert settings["agent"]["think"]["functions"] == [
        {
            "name": "lookup_order",
            "defer_until_eot": True,
            "initial_agent_filler": True,
            "agent_filler_max_count": 2,
            "agent_filler_interval_ms": 3000,
        }
    ]

    update_websocket = _FakeAsyncWebSocket()
    await AsyncV1SocketClient(websocket=cast(Any, update_websocket)).send_update_think_live(
        AgentV1UpdateThinkLive(think_live=_think_live_settings())
    )
    assert _sent_json(update_websocket) == {
        "type": "UpdateThink_Live",
        "think_live": {
            "provider": {
                "type": "deepgram",
                "version": "v1",
                "agent_backchannel_sensitivity": 0.4,
                "presence_check_max_count": 3,
                "presence_check_interval_ms": 5000,
                "frustration_max_count": 2,
                "restricted_terms": ["forbidden phrase"],
            }
        },
    }


def test_sync_deepgram_think_settings_serialize() -> None:
    websocket = _FakeWebSocket()
    V1SocketClient(websocket=cast(Any, websocket)).send_settings(_settings_with_deepgram_think())

    assert _sent_json(websocket)["agent"]["think"]["provider"] == {
        "type": "deepgram",
        "version": "v1",
        "model": "phonellm-mini-alpha-2-fp8",
        "temperature": 0.2,
        "reasoning_mode": "none",
    }


async def test_async_deepgram_think_settings_serialize() -> None:
    websocket = _FakeAsyncWebSocket()
    await AsyncV1SocketClient(websocket=cast(Any, websocket)).send_settings(_settings_with_deepgram_think())

    assert _sent_json(websocket)["agent"]["think"]["provider"] == {
        "type": "deepgram",
        "version": "v1",
        "model": "phonellm-mini-alpha-2-fp8",
        "temperature": 0.2,
        "reasoning_mode": "none",
    }


def test_deepgram_think_provider_uses_the_deepgram_union_variant() -> None:
    settings = construct_type(
        type_=ThinkSettingsV1,
        object_={
            "provider": {
                "type": "deepgram",
                "model": "think-fast",
                "temperature": 1.0,
                "voice_prompt_opt_out": True,
            }
        },
    )

    assert isinstance(settings.provider, ThinkSettingsV1Provider_Deepgram)
    assert settings.provider.model == "think-fast"
    assert settings.provider.temperature == 1.0
    assert settings.provider.voice_prompt_opt_out is True


def test_direct_deepgram_think_provider_serializes() -> None:
    provider = DeepgramThinkProvider(
        model="think-fast",
        version="v1",
        temperature=0.2,
        reasoning_mode="minimal",
        voice_prompt_opt_out=True,
    )

    assert json.loads(provider.json()) == {
        "type": "deepgram",
        "model": "think-fast",
        "version": "v1",
        "temperature": 0.2,
        "reasoning_mode": "minimal",
        "voice_prompt_opt_out": True,
    }


@pytest.mark.parametrize("behavior", [None, "default", "queue", "interrupt"])
def test_sync_dynamic_injection_behaviors_serialize(behavior: str | None) -> None:
    websocket = _FakeWebSocket()
    message = AgentV1InjectDynamicAgentMessage() if behavior is None else AgentV1InjectDynamicAgentMessage(behavior=behavior)
    V1SocketClient(websocket=cast(Any, websocket)).send_inject_dynamic_agent_message(message)

    expected = {"type": "InjectAgentMessage", "is_dynamic": True}
    if behavior is not None:
        expected["behavior"] = behavior
    assert _sent_json(websocket) == expected


@pytest.mark.parametrize("behavior", [None, "default", "queue", "interrupt"])
async def test_async_dynamic_injection_behaviors_serialize(behavior: str | None) -> None:
    websocket = _FakeAsyncWebSocket()
    message = AgentV1InjectDynamicAgentMessage() if behavior is None else AgentV1InjectDynamicAgentMessage(behavior=behavior)
    await AsyncV1SocketClient(websocket=cast(Any, websocket)).send_inject_dynamic_agent_message(message)

    expected = {"type": "InjectAgentMessage", "is_dynamic": True}
    if behavior is not None:
        expected["behavior"] = behavior
    assert _sent_json(websocket) == expected


@pytest.mark.parametrize(
    ("payload", "expected_type"),
    [
        ({"type": "SettingsApplied"}, AgentV1SettingsApplied),
        ({"type": "ThinkLiveUpdated"}, AgentV1ThinkLiveUpdated),
        ({"type": "FrustrationDetected", "count": 2, "escalated": True}, AgentV1FrustrationDetected),
    ],
)
def test_think_live_response_events_parse(payload: dict[str, Any], expected_type: type[Any]) -> None:
    parsed = construct_type(type_=cast(Any, V1SocketClientResponse), object_=payload)

    assert isinstance(parsed, expected_type)
    if isinstance(parsed, AgentV1FrustrationDetected):
        assert parsed.count == 2
        assert parsed.escalated is True


@pytest.mark.parametrize("behavior", ["default", "backchannel", "presence_check", "filler"])
def test_conversation_text_conversational_behaviors_parse(behavior: str) -> None:
    parsed = construct_type(
        type_=cast(Any, V1SocketClientResponse),
        object_={
            "type": "ConversationText",
            "role": "assistant",
            "content": "I am still here.",
            "conversational_behavior": behavior,
        },
    )

    assert isinstance(parsed, AgentV1ConversationText)
    assert parsed.conversational_behavior == behavior


def test_conversation_text_without_behavior_defaults_for_legacy_responses() -> None:
    parsed = construct_type(
        type_=cast(Any, V1SocketClientResponse),
        object_={"type": "ConversationText", "role": "assistant", "content": "I am still here."},
    )

    assert isinstance(parsed, AgentV1ConversationText)
    assert parsed.conversational_behavior == "default"
    assert parsed.dict()["conversational_behavior"] == "default"


def test_legacy_messages_and_think_live_coexist_without_unwrapping() -> None:
    agent = AgentV1SettingsAgent(
        messages=[{"type": "History", "role": "assistant", "content": "Welcome"}],
        think_live=_think_live_settings(),
    )

    serialized = agent.dict()
    assert serialized["context"]["messages"][0]["content"] == "Welcome"
    assert serialized["think_live"]["provider"]["type"] == "deepgram"
