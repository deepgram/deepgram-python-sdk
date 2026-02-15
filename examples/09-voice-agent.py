"""
Example: Voice Agent (Agent V1)

This example shows how to set up a voice agent that can listen, think, and speak.
"""

from typing import Union

from dotenv import load_dotenv

load_dotenv()

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
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

AgentV1SocketClientResponse = Union[str, bytes]

client = DeepgramClient()

try:
    with client.agent.v1.connect() as agent:
        # Configure the agent settings
        settings = AgentV1Settings(
            audio=AgentV1SettingsAudio(
                input=AgentV1SettingsAudioInput(
                    encoding="linear16",
                    sample_rate=24000,
                )
            ),
            agent=AgentV1SettingsAgent(
                listen=AgentV1SettingsAgentListen(
                    provider=AgentV1SettingsAgentListenProvider_V1(
                        type="deepgram",
                        model="nova-3",
                    )
                ),
                think=ThinkSettingsV1(
                    provider=ThinkSettingsV1Provider_OpenAi(
                        type="open_ai",
                        model="gpt-4o-mini",
                        temperature=0.7,
                    ),
                    prompt="You are a helpful AI assistant.",
                ),
                speak=SpeakSettingsV1(
                    provider=SpeakSettingsV1Provider_Deepgram(
                        type="deepgram",
                        model="aura-2-asteria-en",
                    )
                ),
            ),
        )

        print("Sending agent settings...")
        agent.send_settings(settings)

        def on_message(message: AgentV1SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print("Received audio data")
                # In production, you would play this audio or write it to a file
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")

        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # Start listening - this blocks until the connection closes
        # In production, you would send audio from your microphone or audio source:
        # with open("audio.wav", "rb") as audio_file:
        #     audio_data = audio_file.read()
        #     agent.send_media(audio_data)

        agent.start_listening()

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.agent.v1.connect() as agent:
    #     # ... same configuration ...
    #     await agent.send_settings(settings)
    #     await agent.start_listening()

except Exception as e:
    print(f"Error: {e}")
