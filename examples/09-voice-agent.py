"""
Example: Voice Agent (Agent V1)

This example shows how to set up a voice agent that can listen, think, and speak.
"""

from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.agent.v1.types import (
    AgentV1Agent,
    AgentV1AudioConfig,
    AgentV1AudioInput,
    AgentV1DeepgramSpeakProvider,
    AgentV1Listen,
    AgentV1ListenProvider,
    AgentV1OpenAiThinkProvider,
    AgentV1Settings,
    AgentV1SpeakProviderConfig,
    AgentV1Think,
)

AgentV1SocketClientResponse = Union[str, bytes]

client = DeepgramClient()

try:
    with client.agent.v1.connect() as agent:
        # Configure the agent settings
        settings = AgentV1Settings(
            audio=AgentV1AudioConfig(
                input=AgentV1AudioInput(
                    encoding="linear16",
                    sample_rate=44100,
                )
            ),
            agent=AgentV1Agent(
                listen=AgentV1Listen(
                    provider=AgentV1ListenProvider(
                        type="deepgram",
                        model="nova-3",
                        smart_format=True,
                    )
                ),
                think=AgentV1Think(
                    provider=AgentV1OpenAiThinkProvider(
                        type="open_ai",
                        model="gpt-4o-mini",
                        temperature=0.7,
                    ),
                    prompt='You are a helpful AI assistant.',
                ),
                speak=AgentV1SpeakProviderConfig(
                    provider=AgentV1DeepgramSpeakProvider(
                        type="deepgram",
                        model="aura-2-asteria-en",
                    )
                ),
            ),
        )

        print("Sending agent settings...")
        agent.send_agent_v_1_settings(settings)

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
        #     agent.send_agent_v_1_media(audio_data)
        
        agent.start_listening()
        
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.agent.v1.connect() as agent:
    #     # ... same configuration ...
    #     await agent.send_agent_v_1_settings(settings)
    #     await agent.start_listening()
    
except Exception as e:
    print(f"Error: {e}")

