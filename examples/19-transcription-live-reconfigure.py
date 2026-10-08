"""
Example: Reconfigure a Live Transcription Stream (Listen V1)

This streams a short local WAV fixture, then updates the active Nova-3 stream
without reconnecting. ``keyterms`` replaces the full keyterm list (an empty list
clears it), while ``features`` supports only the ``numerals`` formatting feature.
"""

import os
import threading
import time
from pathlib import Path
from typing import Union

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Configure,
    ListenV1Error,
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[
    ListenV1Error,
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
]

client = DeepgramClient(api_key=os.environ.get("DEEPGRAM_API_KEY"))
audio_path = Path(__file__).parent / "fixtures" / "audio.wav"
final_result_received = threading.Event()


def on_message(message: ListenV1SocketClientResponse) -> None:
    if isinstance(message, ListenV1Results):
        transcript = message.channel.alternatives[0].transcript if message.channel.alternatives else ""
        if transcript:
            label = "Final" if message.is_final else "Interim"
            print(f"{label}: {transcript}")
        if message.is_final:
            final_result_received.set()
    elif isinstance(message, ListenV1Error):
        print(f"Configure error ({message.variant}/{message.code}): {message.description}")
    elif isinstance(message, ListenV1Metadata):
        print("Stream completed")


try:
    with client.listen.v1.connect(
        model="nova-3", encoding="linear16", sample_rate=44100, interim_results=True
    ) as connection:
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.ERROR, lambda error: print(f"Connection error: {type(error).__name__}"))
        threading.Thread(target=connection.start_listening, daemon=True).start()

        with audio_path.open("rb") as audio_file:
            audio_file.read(44)  # Skip the WAV header; the stream expects linear16 PCM.
            audio = audio_file.read(44100 * 2 * 3)

        chunk_size = 44100 // 10 * 2  # 100 ms of 16-bit mono PCM.
        reconfigure_after_bytes = 44100 * 2 * 3 // 2  # Reconfigure after 1.5 seconds of audio.
        configured = False
        for offset in range(0, len(audio), chunk_size):
            connection.send_media(audio[offset : offset + chunk_size])
            time.sleep(0.1)
            if not configured and offset + chunk_size >= reconfigure_after_bytes:
                connection.send_configure(ListenV1Configure(keyterms=["Deepgram"], features={"numerals": True}))
                configured = True

        connection.send_finalize()
        if not final_result_received.wait(10):
            raise TimeoutError("The stream did not produce final results within 10 seconds")
        connection.send_close_stream()
except Exception as error:
    print(f"Error: {type(error).__name__}")
    raise SystemExit(1)
