"""
Example: Voice Agent (Agent V1)

This example shows how to set up a voice agent that can listen, think, and speak.
This example simulates a two-way conversation by sending user messages and receiving
agent responses with audio output.
"""

import threading
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1InjectUserMessage,
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider,
    AgentV1SettingsAgentSpeakOneItem,
    AgentV1SettingsAgentSpeakOneItemProvider_Deepgram,
    AgentV1SettingsAgentThink,
    AgentV1SettingsAgentThinkProvider_Anthropic,
    AgentV1SettingsAudio,
)
from deepgram.core.events import EventType

AgentV1SocketClientResponse = Union[str, bytes]

client = DeepgramClient()

# Create output file path for audio data
output_path = Path("output.raw").resolve()

try:
    with open(output_path, "wb") as audio_file:
        with client.agent.v1.connect() as agent:
            # Step 1: Connect (already done by entering context manager)

            # Step 2: Register all listeners first
            welcome_received = threading.Event()
            settings_applied = threading.Event()

            def on_message(message: AgentV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    # Step 7: Save binary message data to output file
                    print("Received audio data")
                    audio_file.write(message)
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    print(f"Received {msg_type} event")
                    # Print event details for debugging
                    if hasattr(message, "__dict__"):
                        print(f"  Event details: {message.__dict__}")

                    # Step 3: Wait for Welcome event
                    if msg_type == "Welcome":
                        print("Welcome event received")
                        welcome_received.set()

                    # Step 5: Wait for SettingsApplied event
                    if msg_type == "SettingsApplied":
                        print("Settings applied event received")
                        settings_applied.set()

            def on_open(_) -> None:
                print("Connection opened")

            def on_close(_) -> None:
                print("Connection closed")

            def on_error(error) -> None:
                print(f"Error: {error}")

            # Register event handlers
            agent.on(EventType.OPEN, on_open)
            agent.on(EventType.MESSAGE, on_message)
            agent.on(EventType.CLOSE, on_close)
            agent.on(EventType.ERROR, on_error)

            # Start listening in a background thread so we can wait for events
            def listen():
                agent.start_listening()

            listen_thread = threading.Thread(target=listen, daemon=True)
            listen_thread.start()

            # Step 3: Wait for Welcome event
            print("Waiting for Welcome event...")
            welcome_received.wait(timeout=10)
            if not welcome_received.is_set():
                raise TimeoutError("Did not receive Welcome event")

            # Step 4: Send settings
            print("Sending agent settings...")
            settings = AgentV1Settings(
                # Audio input defaults to encoding=linear16 and sample_rate=24000 if omitted
                audio=AgentV1SettingsAudio(),
                agent=AgentV1SettingsAgent(
                    listen=AgentV1SettingsAgentListen(
                        provider={
                            "version": "v1",
                            "type": "deepgram",
                            "model": "nova-3",
                            "smart_format": True,
                        }
                    ),
                    think=AgentV1SettingsAgentThink(
                        provider=AgentV1SettingsAgentThinkProvider_Anthropic(
                            type="anthropic",
                            model="claude-sonnet-4-20250514",
                            temperature=0.7,
                        ),
                        prompt="You are a helpful AI assistant.",
                    ),
                    speak=[
                        AgentV1SettingsAgentSpeakOneItem(
                            provider=AgentV1SettingsAgentSpeakOneItemProvider_Deepgram(
                                type="deepgram",
                                model="aura-2-asteria-en",
                            )
                        )
                    ],
                ),
            )
            agent.send_settings(settings)

            # Step 5: Wait for SettingsApplied event
            print("Waiting for SettingsApplied event...")
            settings_applied.wait(timeout=10)
            if not settings_applied.is_set():
                raise TimeoutError("Did not receive SettingsApplied event")

            # --- Now ready to be an agent ---
            print("Agent is ready!")

            # Step 6: Insert user message
            print("Sending user message...")
            user_message = AgentV1InjectUserMessage(content="Hello! Can you tell me a fun fact about space?")
            agent.send_inject_user_message(user_message)

            # Wait for the connection to close (or timeout after reasonable time)
            listen_thread.join(timeout=30)

    print(f"Audio saved to {output_path}")

    # For async version:
    # import asyncio
    # from deepgram import AsyncDeepgramClient
    # async with client.agent.v1.connect() as agent:
    #     # Register handlers
    #     welcome_received = asyncio.Event()
    #     settings_applied = asyncio.Event()
    #
    #     async def on_message(message):
    #         if isinstance(message, bytes):
    #             audio_file.write(message)
    #         elif getattr(message, "type", None) == "Welcome":
    #             welcome_received.set()
    #         elif getattr(message, "type", None) == "SettingsApplied":
    #             settings_applied.set()
    #
    #     agent.on(EventType.MESSAGE, on_message)
    #
    #     listen_task = asyncio.create_task(agent.start_listening())
    #     await welcome_received.wait()
    #     await agent.send_settings(settings)
    #     await settings_applied.wait()
    #     await agent.send_inject_user_message(user_message)
    #     await listen_task

except Exception as e:
    import traceback

    print(f"Error: {e}")
    traceback.print_exc()
