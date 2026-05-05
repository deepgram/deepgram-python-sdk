"""
Example: Voice Agent (Agent V1)

This example shows how to set up a voice agent that can listen, think, and speak.
To keep the example deterministic, it injects a user message after the settings are
applied and then prints the agent's text and audio responses.
"""

import threading
import time
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1InjectUserMessage,
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
USER_MESSAGE = "What does the first all-female spacewalk symbolize?"

client = DeepgramClient()

try:
    with client.agent.v1.connect() as agent:
        settings_applied_event = threading.Event()
        assistant_response_event = threading.Event()

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

        def on_message(message: AgentV1SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print(f"Received agent audio ({len(message)} bytes)")
            else:
                msg_type = getattr(message, "type", "Unknown")
                if msg_type == "SettingsApplied":
                    print("Received SettingsApplied event")
                    settings_applied_event.set()
                elif msg_type == "ConversationText":
                    role = getattr(message, "role", "unknown")
                    content = getattr(message, "content", "")
                    print(f"[{role}] {content}")
                    if role == "assistant":
                        assistant_response_event.set()
                elif msg_type == "UserStartedSpeaking":
                    print(">> User started speaking")
                elif msg_type == "AgentThinking":
                    print(">> Agent thinking...")
                elif msg_type == "AgentStartedSpeaking":
                    print(">> Agent started speaking")
                elif msg_type == "AgentAudioDone":
                    print(">> Agent finished speaking")
                elif msg_type == "Error":
                    print(
                        f">> Agent error: {getattr(message, 'code', 'unknown')} - "
                        f"{getattr(message, 'description', 'unknown error')}"
                    )
                else:
                    print(f"Received {msg_type} event")

        agent.on(EventType.OPEN, lambda _: print("Connection opened"))
        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.CLOSE, lambda _: print("Connection closed"))
        agent.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        listener = threading.Thread(target=agent.start_listening, daemon=True)
        listener.start()

        print("Sending agent settings...")
        agent.send_settings(settings)

        if not settings_applied_event.wait(10):
            raise TimeoutError("Timed out waiting for agent settings to apply")

        print(f"Sending injected user message: {USER_MESSAGE}")
        agent.send_inject_user_message(AgentV1InjectUserMessage(content=USER_MESSAGE))

        if not assistant_response_event.wait(30):
            raise TimeoutError("Timed out waiting for the agent to respond")

        # Give the final audio callbacks a moment to flush before exiting the context.
        time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
