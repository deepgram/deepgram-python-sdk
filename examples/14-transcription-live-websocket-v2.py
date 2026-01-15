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

# Chunk size in bytes (e.g., 8KB chunks for efficient streaming)
CHUNK_SIZE = 8192

client = DeepgramClient()

try:
    # Listen V2 requires specific audio format: 16kHz linear16 PCM
    with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="16000"
    ) as connection:

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

        # Start listening in a background thread
        threading.Thread(target=connection.start_listening, daemon=True).start()

        # Stream audio file
        # In production, replace this with audio from microphone or other live source
        # IMPORTANT: Audio must be 16kHz linear16 PCM for Listen V2
        audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")
        
        with open(audio_path, "rb") as audio_file:
            print(f"Streaming audio from {audio_path}")
            
            while True:
                chunk = audio_file.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                connection.send_listen_v_2_media(chunk)
        
        print("Finished sending audio")

    # For async version:
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
    #     # Start listening
    #     listen_task = asyncio.create_task(connection.start_listening())
    #     
    #     # Stream audio
    #     with open(audio_path, "rb") as audio_file:
    #         while chunk := audio_file.read(CHUNK_SIZE):
    #             await connection.send_listen_v_2_media(chunk)
    #     
    #     await listen_task

except Exception as e:
    print(f"Error: {e}")
