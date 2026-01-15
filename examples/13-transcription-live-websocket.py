"""
Example: Live Transcription with WebSocket (Listen V1)

This example demonstrates how to use WebSocket for real-time audio transcription.
In production, you would stream audio from a microphone or other live source.
This example uses an audio file to demonstrate the streaming pattern.
"""

import os
import threading
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

# Chunk size in bytes (e.g., 8KB chunks for efficient streaming)
CHUNK_SIZE = 8192

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

        # Start listening in a background thread
        threading.Thread(target=connection.start_listening, daemon=True).start()

        # Stream audio file
        # In production, replace this with audio from microphone or other live source
        audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")

        with open(audio_path, "rb") as audio_file:
            print(f"Streaming audio from {audio_path}")

            while True:
                chunk = audio_file.read(CHUNK_SIZE)
                if not chunk:
                    break

                connection.send_listen_v_1_media(chunk)

        print("Finished sending audio")

    # For async version:
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
    #     # Start listening
    #     listen_task = asyncio.create_task(connection.start_listening())
    #
    #     # Stream audio
    #     with open(audio_path, "rb") as audio_file:
    #         while chunk := audio_file.read(CHUNK_SIZE):
    #             await connection.send_listen_v_1_media(chunk)
    #
    #     await listen_task

except Exception as e:
    print(f"Error: {e}")
