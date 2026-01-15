"""
Example: Live Transcription with WebSocket V2 (Listen V2)

This example demonstrates how to use Listen V2 for advanced conversational speech
recognition with contextual turn detection.

Note: Listen V2 requires 16kHz linear16 PCM audio format.
In production, you would stream audio from a microphone or other live source.
This example uses an audio file to demonstrate the streaming pattern.
"""

import os
import threading
import time
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)

ListenV2SocketClientResponse = Union[ListenV2Connected, ListenV2TurnInfo, ListenV2FatalError]

# Audio streaming configuration
# IMPORTANT: Listen V2 requires 16kHz linear16 PCM audio
CHUNK_SIZE = 8192  # Bytes to send at a time
SAMPLE_RATE = 16000  # Hz (required for Listen V2)
SAMPLE_WIDTH = 2  # 16-bit audio = 2 bytes per sample
CHANNELS = 1  # Mono audio

# Calculate delay between chunks to simulate real-time streaming
# This makes the audio stream at its natural playback rate
CHUNK_DELAY = CHUNK_SIZE / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

client = DeepgramClient()

try:
    # Listen V2 requires specific audio format: 16kHz linear16 PCM
    with client.listen.v2.connect(model="flux-general-en", encoding="linear16", sample_rate="16000") as connection:

        def on_message(message: ListenV2SocketClientResponse) -> None:
            # Handle TurnInfo events containing transcription and turn metadata
            if isinstance(message, ListenV2TurnInfo):
                print(f"Turn {message.turn_index}: {message.transcript}")
                print(f"  Event: {message.event}")

        def on_open(_) -> None:
            print("Connection opened")

        def on_close(_) -> None:
            print("Connection closed")

        def on_error(error) -> None:
            print(f"Error: {error}")

        # Register event handlers
        connection.on(EventType.OPEN, on_open)
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, on_close)
        connection.on(EventType.ERROR, on_error)

        # Define a function to send audio in a background thread
        def send_audio():
            # IMPORTANT: Audio must be 16kHz linear16 PCM for Listen V2
            audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")
            
            with open(audio_path, "rb") as audio_file:
                print(f"Streaming audio from {audio_path}")

                while True:
                    chunk = audio_file.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    connection.send_media(chunk)

                    # Simulate real-time streaming by adding delay between chunks
                    time.sleep(CHUNK_DELAY)

            print("Finished sending audio")

        # Start sending audio in a background thread
        threading.Thread(target=send_audio, daemon=True).start()

        # Start listening - this blocks until the connection closes or times out
        # The connection will stay open until the server closes it or it times out
        connection.start_listening()

    # For async version:
    # import asyncio
    # from deepgram import AsyncDeepgramClient
    #
    # async with client.listen.v2.connect(
    #     model="flux-general-en",
    #     encoding="linear16",
    #     sample_rate="16000"
    # ) as connection:
    #     async def on_message(message):
    #         if isinstance(message, ListenV2TurnInfo):
    #             print(f"Turn {message.turn_index}: {message.transcript}")
    #
    #     connection.on(EventType.MESSAGE, on_message)
    #
    #     # Define coroutine to send audio
    #     async def send_audio():
    #         audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")
    #         with open(audio_path, "rb") as audio_file:
    #             while chunk := audio_file.read(CHUNK_SIZE):
    #                 await connection.send_media(chunk)
    #                 # Simulate real-time streaming
    #                 await asyncio.sleep(CHUNK_DELAY)
    #         print("Finished sending audio")
    #
    #     # Start both tasks
    #     listen_task = asyncio.create_task(connection.start_listening())
    #     send_task = asyncio.create_task(send_audio())
    #
    #     # Wait for send to complete
    #     await send_task
    #
    #     # Continue listening until connection closes or times out
    #     await listen_task

except Exception as e:
    print(f"Error: {e}")
