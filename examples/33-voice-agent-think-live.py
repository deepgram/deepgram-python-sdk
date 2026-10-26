"""
Example: Voice Agent with Think Live (Agent V1)

This deterministic text-only example configures normal Think alongside Think Live,
then injects a user message and queues a Think Live-generated dynamic message after
SettingsApplied. It does not write or play audio. Frustration detection and filler
responses are model- and timing-dependent, so they may not appear on every run.
"""

import threading
import time

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1InjectDynamicAgentMessage,
    AgentV1InjectUserMessage,
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V1,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
    AgentV1UpdateThinkLive,
)
from deepgram.core.events import EventType
from deepgram.types.deepgram_think_live_provider_v1 import DeepgramThinkLiveProviderV1
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_live_settings_v1 import ThinkLiveSettingsV1
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

USER_MESSAGE = "Please tell me one short fact about the first all-female spacewalk."

load_dotenv()
client = DeepgramClient()


def think_live_settings() -> ThinkLiveSettingsV1:
    return ThinkLiveSettingsV1(
        provider=DeepgramThinkLiveProviderV1(
            agent_backchannel_sensitivity=0.4,
            presence_check_max_count=1,
            presence_check_interval_ms=5000,
            frustration_max_count=1,
        )
    )


try:
    with client.agent.v1.connect() as agent:
        settings_applied = threading.Event()
        think_live_updated = threading.Event()
        assistant_response = threading.Event()

        settings = AgentV1Settings(
            audio=AgentV1SettingsAudio(
                input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)
            ),
            agent=AgentV1SettingsAgent(
                listen=AgentV1SettingsAgentListen(
                    provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3")
                ),
                think=ThinkSettingsV1(
                    provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini"),
                    prompt="You are helpful and concise.",
                ),
                think_live=think_live_settings(),
                speak=SpeakSettingsV1(
                    provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
                ),
            ),
        )

        def on_message(message: object) -> None:
            if isinstance(message, bytes):
                print(f"Received agent audio ({len(message)} bytes; not saved)")
                return

            msg_type = getattr(message, "type", "Unknown")
            if msg_type == "SettingsApplied":
                print("Received SettingsApplied event")
                settings_applied.set()
            elif msg_type == "ThinkLiveUpdated":
                print("Received ThinkLiveUpdated event")
                think_live_updated.set()
            elif msg_type == "FrustrationDetected":
                print(
                    "Received FrustrationDetected event "
                    f"(count={getattr(message, 'count', 'unknown')}, "
                    f"escalated={getattr(message, 'escalated', 'unknown')})"
                )
            elif msg_type == "ConversationText":
                role = getattr(message, "role", "unknown")
                print(f"[{role}] {getattr(message, 'content', '')}")
                conversational_behavior = getattr(message, "conversational_behavior", None)
                if conversational_behavior is not None:
                    print(f"  conversational_behavior: {conversational_behavior}")
                if role == "assistant" and conversational_behavior in (None, "default"):
                    assistant_response.set()
            elif msg_type == "Error":
                print("Agent reported an error")
            else:
                print(f"Received {msg_type} event")

        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda _: print("Connection error"))

        listener = threading.Thread(target=agent.start_listening, daemon=True)
        listener.start()

        agent.send_settings(settings)
        if not settings_applied.wait(10):
            raise TimeoutError("Timed out waiting for settings to apply")

        # This update demonstrates the ThinkLiveUpdated event without changing behavior.
        agent.send_update_think_live(AgentV1UpdateThinkLive(think_live=think_live_settings()))
        if not think_live_updated.wait(10):
            raise TimeoutError("Timed out waiting for Think Live update to apply")

        agent.send_inject_user_message(AgentV1InjectUserMessage(content=USER_MESSAGE))
        agent.send_inject_dynamic_agent_message(AgentV1InjectDynamicAgentMessage(behavior="queue"))

        if not assistant_response.wait(30):
            raise TimeoutError("Timed out waiting for an assistant response")

        # Bound the final callbacks without writing any audio data to disk.
        time.sleep(1)

except Exception as error:
    print(f"Voice Agent example stopped: {type(error).__name__}")
