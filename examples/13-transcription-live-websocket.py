"""
Example: Live Transcription with WebSocket (Listen V1)

This example demonstrates how to use WebSocket for real-time audio transcription.
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
from deepgram.listen.v1.types import (
    ListenV1Finalize,
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

# Audio streaming configuration
CHUNK_SIZE = 8192  # Bytes to send at a time
SAMPLE_RATE = 44100  # Hz (typical for WAV files)
SAMPLE_WIDTH = 2  # 16-bit audio = 2 bytes per sample
CHANNELS = 1  # Mono audio

# Calculate delay between chunks to simulate real-time streaming
# This makes the audio stream at its natural playback rate
CHUNK_DELAY = CHUNK_SIZE / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

client = DeepgramClient()

try:
    with client.listen.v1.connect(model="nova-3") as connection:

        def on_message(message: ListenV1SocketClientResponse) -> None:
            # Extract transcription from Results events
            if isinstance(message, ListenV1Results):
                if message.channel and message.channel.alternatives:
                    transcript = message.channel.alternatives[0].transcript
                    if transcript:
                        print(f"Transcript: {transcript}")

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

            connection.send_finalize(ListenV1Finalize(type="Finalize"))

        # Start sending audio in a background thread
        threading.Thread(target=send_audio, daemon=True).start()

        # Start listening - this blocks until the connection closes or times out
        # The connection will stay open until the server closes it or it times out
        connection.start_listening()

    # For async version:
    # import asyncio
    # from deepgram import AsyncDeepgramClient
    #
    # async with client.listen.v1.connect(model="nova-3") as connection:
    #     async def on_message(message):
    #         if isinstance(message, ListenV1Results):
    #             if message.channel and message.channel.alternatives:
    #                 transcript = message.channel.alternatives[0].transcript
    #                 if transcript:
    #                     print(f"Transcript: {transcript}")
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
    #         await connection.send_finalize(ListenV1Finalize(type="Finalize"))
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
