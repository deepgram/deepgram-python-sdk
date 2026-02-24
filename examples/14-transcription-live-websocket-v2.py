"""
Example: Live Transcription with WebSocket V2 (Listen V2)

This example shows how to use Listen V2 for advanced conversational speech recognition
with contextual turn detection.
"""

import os
import threading
import time
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2CloseStream,
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)

ListenV2SocketClientResponse = Union[ListenV2Connected, ListenV2TurnInfo, ListenV2FatalError]

client = DeepgramClient(api_key=os.environ.get("DEEPGRAM_API_KEY"))

try:
    with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="16000",
    ) as connection:

        def on_message(message: ListenV2SocketClientResponse) -> None:
            msg_type = getattr(message, "type", type(message).__name__)
            print(f"Received {msg_type} event ({type(message).__name__})")

            # Extract transcription from TurnInfo events
            if isinstance(message, ListenV2TurnInfo):
                print(f"  transcript: {message.transcript}")
                print(f"  event: {message.event}")
                print(f"  turn_index: {message.turn_index}")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Error: {type(error).__name__}: {error}"))

        # Send audio in a background thread so start_listening can process responses
        def send_audio():
            audio_path = Path(__file__).parent / "fixtures" / "audio.wav"
            with open(audio_path, "rb") as f:
                audio = f.read()

            # Send in chunks
            chunk_size = 4096
            for i in range(0, len(audio), chunk_size):
                connection.send_media(audio[i : i + chunk_size])
                time.sleep(0.01)  # pace the sending

            # Signal end of audio
            time.sleep(2)
            connection.send_close_stream(ListenV2CloseStream(type="CloseStream"))

        sender = threading.Thread(target=send_audio, daemon=True)
        sender.start()

        # This blocks until the connection closes
        connection.start_listening()

except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
