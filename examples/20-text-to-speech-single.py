"""
Example: Text-to-Speech Single Request

This example shows how to convert text to speech in a single request.
The generate() method returns an Iterator[bytes] that streams audio chunks
as they arrive from the API, allowing you to process audio incrementally.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Sending text-to-speech request...")
    # generate() returns an Iterator[bytes] that streams chunks as they arrive
    # This allows processing audio incrementally without waiting for the full response
    audio_chunks = client.speak.v1.audio.generate(
        text="Hello, this is a sample text to speech conversion.",
        model="aura-2-asteria-en",
        # Optional: Control chunk size for streaming
        # request_options={"chunk_size": 8192}  # 8KB chunks
    )

    # Process chunks as they arrive (streaming)
    output_path = Path("output.mp3").resolve()
    chunk_count = 0
    with open(output_path, "wb") as audio_file:
        for chunk in audio_chunks:
            audio_file.write(chunk)
            chunk_count += 1
            # In production, you could process chunks immediately (e.g., play audio)

    print(f"Audio saved to {output_path} ({chunk_count} chunks received)")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # async for chunk in await client.speak.v1.audio.generate(
    #     text="Hello, this is a sample text to speech conversion.",
    #     model="aura-2-asteria-en",
    # ):
    #     # Process chunks as they arrive
    #     audio_file.write(chunk)

    # With access token:
    # client = DeepgramClient(access_token="your-access-token")

except Exception as e:
    print(f"Error: {e}")
