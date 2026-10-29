"""Configure a Voice Agent with a Deepgram-hosted Think model."""

import threading

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V2,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
)
from deepgram.core.events import EventType
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_Deepgram

load_dotenv()
client = DeepgramClient()

settings = AgentV1Settings(
    audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
    # think-fast requires Model Improvement Program participation.
    # With mip_opt_out=True, use phonellm-mini-alpha-2-fp8 or the service returns INVALID_SETTINGS.
    mip_opt_out=True,
    agent=AgentV1SettingsAgent(
        listen=AgentV1SettingsAgentListen(
            provider=AgentV1SettingsAgentListenProvider_V2(type="deepgram", model="flux-general-en")
        ),
        think=ThinkSettingsV1(
            provider=ThinkSettingsV1Provider_Deepgram(
                type="deepgram",
                model="phonellm-mini-alpha-2-fp8",
                temperature=0.2,
                reasoning_mode="none",
            ),
            prompt="You are helpful and concise.",
        ),
        speak=SpeakSettingsV1(
            provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
        ),
    ),
)

with client.agent.v1.connect() as agent:
    settings_applied = threading.Event()

    def on_message(message: object) -> None:
        message_type = getattr(message, "type", "Unknown")
        print(f"Received {message_type}")
        if message_type == "SettingsApplied":
            settings_applied.set()

    agent.on(EventType.MESSAGE, on_message)
    threading.Thread(target=agent.start_listening, daemon=True).start()
    agent.send_settings(settings)

    if not settings_applied.wait(10):
        raise TimeoutError("Timed out waiting for Deepgram Think settings to apply")
