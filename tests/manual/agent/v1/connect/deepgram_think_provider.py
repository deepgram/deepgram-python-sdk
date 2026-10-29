"""Manual live integration test for the Deepgram Think provider.

Set DEEPGRAM_API_KEY before running this script. It passes only after the
Voice Agent service accepts the settings and emits SettingsApplied.
"""

import threading

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V1,
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
settings_applied = threading.Event()
errors: list[object] = []

settings = AgentV1Settings(
    audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
    mip_opt_out=True,
    agent=AgentV1SettingsAgent(
        listen=AgentV1SettingsAgentListen(
            provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3")
        ),
        think=ThinkSettingsV1(
            provider=ThinkSettingsV1Provider_Deepgram(
                type="deepgram",
                model="phonellm-mini-alpha-2-fp8",
                temperature=0.2,
                reasoning_mode="none",
                voice_prompt_opt_out=True,
            ),
            prompt="Reply with one sentence.",
        ),
        speak=SpeakSettingsV1(
            provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
        ),
    ),
)

with client.agent.v1.connect() as agent:
    def on_message(message: object) -> None:
        message_type = getattr(message, "type", "Unknown")
        if message_type == "SettingsApplied":
            settings_applied.set()
        elif message_type == "Error":
            errors.append(message)

    agent.on(EventType.MESSAGE, on_message)
    threading.Thread(target=agent.start_listening, daemon=True).start()
    agent.send_settings(settings)

    if not settings_applied.wait(10):
        raise AssertionError(f"Deepgram Think settings were not accepted: {errors!r}")
