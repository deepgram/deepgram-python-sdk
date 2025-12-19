import asyncio
import os

from dotenv import load_dotenv

print("Starting async listen v2 connect example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)
from typing import Union

ListenV2SocketClientResponse = Union[ListenV2Connected, ListenV2TurnInfo, ListenV2FatalError]

print("Initializing AsyncDeepgramClient")
client = AsyncDeepgramClient()
print("AsyncDeepgramClient initialized")

# Audio file properties (from ffprobe: sample_rate=44100 Hz, bit_rate=705600 bps)
# Note: v2 connection uses sample_rate=16000, but we use file's actual sample_rate for chunking
audio_sample_rate = 44100  # Hz (from audio file)
audio_bit_rate = 705600  # bps (from audio file)
print(f"Audio file properties - Sample rate: {audio_sample_rate} Hz, Bit rate: {audio_bit_rate} bps")

# Calculate chunk size for 100ms of audio (linear16 PCM: 2 bytes per sample)
# Assuming mono audio: bytes_per_second = sample_rate * 2
chunk_duration_ms = 1000  # 1s chunks
chunk_size = int(audio_sample_rate * 2 * (chunk_duration_ms / 1000.0))
chunk_delay = chunk_duration_ms / 1000.0  # Delay in seconds
print(f"Chunk size: {chunk_size} bytes ({chunk_duration_ms}ms), Delay: {chunk_delay}s per chunk")

# Get audio file path
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(script_dir, "..", "..", "..", "fixtures", "audio.wav")


async def main() -> None:
    try:
        model = "flux-general-en"
        encoding = "linear16"
        sample_rate = "16000"
        print(f"Establishing async connection - Model: {model}, Encoding: {encoding}, Sample Rate: {sample_rate}")
        async with client.listen.v2.connect(model=model, encoding=encoding, sample_rate=sample_rate) as connection:
            print("Connection context entered")

            def on_message(message: ListenV2SocketClientResponse) -> None:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")
                # For transcription events, extract full transcription; otherwise show full event body
                if msg_type == "Results" or (hasattr(message, "type") and str(message.type) == "Results"):
                    # Extract transcription from Results event
                    if hasattr(message, "channel") and message.channel:
                        channel = message.channel
                        if hasattr(channel, "alternatives") and channel.alternatives:
                            alt = channel.alternatives[0]
                            if hasattr(alt, "transcript") and alt.transcript:
                                print(f"Full transcription: {alt.transcript}")
                            else:
                                print(f"Event body: {message}")
                        else:
                            print(f"Event body: {message}")
                    else:
                        print(f"Event body: {message}")
                else:
                    print(f"Event body: {message}")

            print("Registering event handlers")
            connection.on(EventType.OPEN, lambda _: print("Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
            connection.on(EventType.ERROR, lambda error: print(f"Connection error: {error}"))
            print("Event handlers registered")

            # EXAMPLE ONLY: Start listening task and cancel after brief demo
            # In production, you would typically await connection.start_listening() directly
            # which runs until the connection closes or is interrupted
            print("Starting listening task")
            listen_task = asyncio.create_task(connection.start_listening())

            # Load and send audio file in chunks
            print(f"Loading audio file: {audio_path}")
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
            print(f"Audio file loaded, total size: {len(audio_data)} bytes")

            # Send audio in chunks with delays to simulate microphone input
            print("Sending audio chunks...")
            chunk_count = 0
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i : i + chunk_size]
                if chunk:
                    await connection.send_listen_v_2_media(chunk)
                    chunk_count += 1
                    print(f"Sent chunk {chunk_count} ({len(chunk)} bytes)")
                    await asyncio.sleep(chunk_delay)

            print(f"Finished sending {chunk_count} chunks")
            print("Waiting 2 seconds for final transcription...")
            await asyncio.sleep(2)
            print("Cancelling listening task")
            listen_task.cancel()
            print("Exiting connection context")
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        # Log request headers if available
        if hasattr(e, "request_headers"):
            print(f"Request headers: {e.request_headers}")
        elif hasattr(e, "request") and hasattr(e.request, "headers"):
            print(f"Request headers: {e.request.headers}")
        # Log response headers if available
        if hasattr(e, "headers"):
            print(f"Response headers: {e.headers}")
        # Log status code if available
        if hasattr(e, "status_code"):
            print(f"Status code: {e.status_code}")
        # Log body if available
        if hasattr(e, "body"):
            print(f"Response body: {e.body}")
        print(f"Caught: {e}")


print("Running async main function")
asyncio.run(main())
print("Script completed")
