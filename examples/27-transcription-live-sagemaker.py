"""
Example: Live Transcription via SageMaker (Listen V1)

This example shows how to use a custom transport to stream audio for real-time
transcription through a SageMaker endpoint running Deepgram, instead of the
Deepgram Cloud WebSocket API.

The SageMaker transport uses HTTP/2 bidirectional streaming under the hood,
but exposes the same SDK interface — just swap in a transport_factory.

**Async-only** — the SageMaker transport requires ``AsyncDeepgramClient``.
It cannot be used with the sync ``DeepgramClient``.

Requirements::

    pip install aws-sdk-sagemaker-runtime-http2 boto3

Environment:
    AWS credentials must be configured (via environment variables,
    ``~/.aws/credentials``, or an IAM role).
    Set ``SAGEMAKER_ENDPOINT_NAME`` and ``AWS_REGION`` in ``.env`` or your shell.
"""

import asyncio
import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)
from deepgram.transports.sagemaker import SageMakerTransportFactory

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT_NAME", "deepgram-nova-3")
SAGEMAKER_REGION = os.getenv("AWS_REGION", "us-west-2")

CHUNK_SIZE = 512_000  # 512 KB per chunk (optimal for streaming performance)
CHUNK_DELAY = 0.5  # seconds between chunks

# ---------------------------------------------------------------------------
# Create the client with SageMaker transport
# ---------------------------------------------------------------------------
factory = SageMakerTransportFactory(
    endpoint_name=SAGEMAKER_ENDPOINT,
    region=SAGEMAKER_REGION,
)

# SageMaker uses AWS credentials (not Deepgram API keys), so api_key is unused
client = AsyncDeepgramClient(api_key="unused", transport_factory=factory)


async def main() -> None:
    try:
        async with client.listen.v1.connect(model="nova-3") as connection:

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

            # Start listening in a background task so we can send audio concurrently
            listen_task = asyncio.create_task(connection.start_listening())

            # Wait for the connection to establish
            await asyncio.sleep(1)

            # Read and send audio in chunks
            audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()

            print(f"Sending {len(audio_data)} bytes in {CHUNK_SIZE}-byte chunks...")
            for i in range(0, len(audio_data), CHUNK_SIZE):
                chunk = audio_data[i : i + CHUNK_SIZE]
                await connection.send_media(chunk)
                print(f"Sent chunk {i // CHUNK_SIZE + 1} ({len(chunk)} bytes)")
                await asyncio.sleep(CHUNK_DELAY)

            # Signal end of audio
            await connection.send_finalize()
            print("Finished sending audio")

            # Wait for final responses
            await asyncio.sleep(5)

            # Cancel the listening task
            listen_task.cancel()

    except Exception as e:
        print(f"Error: {e}")


asyncio.run(main())
