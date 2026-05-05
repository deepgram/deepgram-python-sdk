#!/usr/bin/env python3
"""
Example: TextBuilder with Streaming TTS (WebSocket)

This example demonstrates using TextBuilder with streaming text-to-speech
over WebSocket for real-time audio generation.

The streaming API path shown here focuses on pronunciation controls. Inline
pause tokens are omitted because the WebSocket endpoint may reject them with
DATA-0002 policy violations.
"""

import os
import threading
from typing import Union

from deepgram import DeepgramClient
from deepgram.helpers import TextBuilder
from deepgram.core.events import EventType
from deepgram.speak.v1.types import SpeakV1Text

SpeakV1SocketClientResponse = Union[str, bytes]


def example_streaming_with_textbuilder():
    """Stream TTS audio using TextBuilder for pronunciation control"""
    print("Example: Streaming TTS with TextBuilder")
    print("-" * 50)

    # Build text with pronunciations and pauses
    text = (
        TextBuilder()
        .text("Take ")
        .pronunciation("azathioprine", "ˌæzəˈθaɪəpriːn")
        .text(" twice daily with ")
        .pronunciation("dupilumab", "duːˈpɪljuːmæb")
        .text(" injections.")
        .text(" Do not exceed prescribed dosage.")
        .build()
    )

    print(f"Generated text: {text}\n")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        print("ℹ Set DEEPGRAM_API_KEY to stream audio")
        return

    client = DeepgramClient(api_key=api_key)

    try:
        with client.speak.v1.connect(
            model="aura-2-asteria-en", encoding="linear16", sample_rate=24000
        ) as connection:
            closed_event = threading.Event()

            def on_message(message: SpeakV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    print(f"Received {len(message)} bytes of audio data")
                    # Write audio to file
                    with open("streaming_output.raw", "ab") as audio_file:
                        audio_file.write(message)
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    print(f"Received {msg_type} event")
                    if msg_type == "Flushed":
                        connection.send_close()

            connection.on(EventType.OPEN, lambda _: print("✓ Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, lambda _: (print("✓ Connection closed"), closed_event.set()))
            connection.on(EventType.ERROR, lambda error: print(f"✗ Error: {error}"))

            # Send the TextBuilder-generated text
            connection.send_text(SpeakV1Text(text=text))

            # Flush to ensure all text is processed
            connection.send_flush()

            listener = threading.Thread(target=connection.start_listening, daemon=True)
            listener.start()
            closed_event.wait(30)

        print("\n✓ Audio saved to streaming_output.raw")
        print("  Convert to WAV: ffmpeg -f s16le -ar 24000 -ac 1 -i streaming_output.raw output.wav")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_multiple_messages():
    """Stream multiple TextBuilder messages sequentially"""
    print("\n\nExample: Multiple Messages with Streaming")
    print("-" * 50)

    # Build multiple text segments
    intro = TextBuilder().text("Welcome to your medication guide.").build()

    instruction1 = (
        TextBuilder()
        .text("First, take ")
        .pronunciation("methotrexate", "mɛθəˈtrɛkseɪt")
        .text(" on Mondays.")
        .build()
    )

    instruction2 = (
        TextBuilder()
        .text("Then, inject ")
        .pronunciation("adalimumab", "ˌædəˈljuːməb")
        .text(" on Fridays.")
        .build()
    )

    closing = TextBuilder().text("Contact your doctor with any questions.").build()

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        print("ℹ Set DEEPGRAM_API_KEY to stream audio")
        return

    client = DeepgramClient(api_key=api_key)

    try:
        with client.speak.v1.connect(
            model="aura-2-asteria-en", encoding="linear16", sample_rate=24000
        ) as connection:

            audio_chunks = []
            closed_event = threading.Event()

            def on_message(message: SpeakV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    audio_chunks.append(message)
                    print(f"Received {len(message)} bytes")
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    if msg_type == "Flushed":
                        connection.send_close()

            connection.on(EventType.OPEN, lambda _: print("✓ Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, lambda _: (print("✓ Connection closed"), closed_event.set()))

            # Send multiple messages
            for i, text in enumerate([intro, instruction1, instruction2, closing], 1):
                print(f"Sending message {i}: {text[:50]}...")
                connection.send_text(SpeakV1Text(text=text))

            connection.send_flush()

            listener = threading.Thread(target=connection.start_listening, daemon=True)
            listener.start()
            closed_event.wait(30)

        # Save all audio
        with open("streaming_multi.raw", "wb") as f:
            for chunk in audio_chunks:
                f.write(chunk)

        print(f"\n✓ Saved {len(audio_chunks)} audio chunks to streaming_multi.raw")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all streaming examples"""
    if os.path.exists("streaming_output.raw"):
        os.remove("streaming_output.raw")
    if os.path.exists("streaming_multi.raw"):
        os.remove("streaming_multi.raw")

    example_streaming_with_textbuilder()
    example_multiple_messages()

    print("\n" + "=" * 50)
    print("All streaming examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
