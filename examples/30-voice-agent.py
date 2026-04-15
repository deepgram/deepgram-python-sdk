"""
Example: Voice Agent (Agent V1)

This example shows how to set up a voice agent that can listen, think, and speak.
It streams a pre-recorded audio file to simulate user speech.
"""

import os
import threading
import time
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

audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "audio.wav")

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
                    prompt="You are a helpful AI assistant. Keep your responses brief.",
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
                print(f"Received agent audio ({len(message)} bytes)")
            else:
                msg_type = getattr(message, "type", "Unknown")
                if msg_type == "ConversationText":
                    role = getattr(message, "role", "unknown")
                    content = getattr(message, "content", "")
                    print(f"[{role}] {content}")
                elif msg_type == "UserStartedSpeaking":
                    print(">> User started speaking")
                elif msg_type == "AgentThinking":
                    print(">> Agent thinking...")
                elif msg_type == "AgentStartedSpeaking":
                    print(">> Agent started speaking")
                elif msg_type == "AgentAudioDone":
                    print(">> Agent finished speaking")
                else:
                    print(f"Received {msg_type} event")

        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # Stream audio in a background thread
        def send_audio():
            with open(audio_path, "rb") as f:
                audio_data = f.read()

            chunk_size = 8192
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i : i + chunk_size]
                if chunk:
                    agent.send_media(chunk)
                time.sleep(0.01)

            print("Finished streaming audio, waiting for agent response...")
            time.sleep(15)

        sender = threading.Thread(target=send_audio, daemon=True)
        sender.start()

        # Start listening - blocks until connection closes
        agent.start_listening()

except Exception as e:
    print(f"Error: {e}")
