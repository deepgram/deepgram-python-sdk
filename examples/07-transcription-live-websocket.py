"""
Example: Live Transcription with WebSocket (Listen V1)

This example shows how to stream audio for real-time transcription using WebSocket.
It reads an audio file, chunks it, and sends it as if it were microphone audio.
"""

import os
import threading
import time
import wave
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

# Audio file properties (from ffprobe: sample_rate=44100 Hz, mono, PCM s16le)
SAMPLE_RATE = 44100  # Hz
CHANNELS = 1  # mono
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes per sample

# Calculate chunk size for 100ms of audio (to simulate real-time streaming)
CHUNK_DURATION_MS = 100  # milliseconds
CHUNK_SIZE = int(SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS * (CHUNK_DURATION_MS / 1000.0))
CHUNK_DELAY = CHUNK_DURATION_MS / 1000.0  # Delay in seconds

client = DeepgramClient()

try:
    with client.listen.v1.connect(model="nova-3") as connection:

        def on_message(message: ListenV1SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

            # Extract transcription from Results events
            if isinstance(message, ListenV1Results):
                if message.channel and message.channel.alternatives:
                    transcript = message.channel.alternatives[0].transcript
                    if transcript:
                        print(f"Transcript: {transcript}")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # Start listening in a background thread (it blocks until connection closes)
        threading.Thread(target=connection.start_listening, daemon=True).start()

        # Wait a moment for connection to establish
        time.sleep(0.5)

        # Load audio file and extract raw PCM data
        audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")
        print(f"Loading audio file: {audio_path}")

        with wave.open(audio_path, "rb") as wav_file:
            # Read all audio frames as raw PCM data
            audio_data = wav_file.readframes(wav_file.getnframes())

        print(f"Audio loaded: {len(audio_data)} bytes")
        print(f"Sending audio in {CHUNK_DURATION_MS}ms chunks...")

        # Send audio in chunks with delays to simulate microphone input
        chunk_count = 0
        for i in range(0, len(audio_data), CHUNK_SIZE):
            chunk = audio_data[i : i + CHUNK_SIZE]
            if chunk:
                connection.send_listen_v_1_media(chunk)
                chunk_count += 1
                time.sleep(CHUNK_DELAY)

        print(f"Finished sending {chunk_count} chunks")
        print("Waiting for final transcription...")
        time.sleep(2)

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.listen.v1.connect(model="nova-3") as connection:
    #     # ... same event handlers ...
    #     await connection.start_listening()

except Exception as e:
    print(f"Error: {e}")
