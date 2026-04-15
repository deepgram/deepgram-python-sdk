"""
Example: Live Transcription with WebSocket (Listen V1)

This example shows how to stream audio for real-time transcription using WebSocket.
It streams a pre-recorded audio file in chunks to simulate a live microphone feed.
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
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

client = DeepgramClient()

# Audio chunking: simulate real-time streaming by sending 1-second chunks
sample_rate = 44100  # Hz (matches fixtures/audio.wav)
chunk_size = sample_rate * 2  # 2 bytes per sample (linear16 PCM mono)
chunk_delay = 1.0  # seconds between chunks

audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "audio.wav")

try:
    with client.listen.v1.connect(model="nova-3") as connection:

        def on_message(message: ListenV1SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            if isinstance(message, ListenV1Results):
                if message.channel and message.channel.alternatives:
                    transcript = message.channel.alternatives[0].transcript
                    if transcript:
                        print(f"Transcript: {transcript}")
            else:
                print(f"Received {msg_type} event")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # Start listening in a background thread so we can send audio concurrently
        threading.Thread(target=connection.start_listening, daemon=True).start()

        # Stream audio file in chunks to simulate live microphone input
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i : i + chunk_size]
            if chunk:
                connection.send_media(chunk)
                time.sleep(chunk_delay)

        # Wait for final transcription results
        time.sleep(2)

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.listen.v1.connect(model="nova-3") as connection:
    #     # ... same event handlers ...
    #     await connection.start_listening()

except Exception as e:
    print(f"Error: {e}")
