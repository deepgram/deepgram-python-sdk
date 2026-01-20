"""
Example: Text-to-Speech Streaming with WebSocket

This example shows how to stream text-to-speech conversion using WebSocket.
In production, you would send text dynamically as it becomes available.
"""

from pathlib import Path
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v1.types import SpeakV1Close, SpeakV1Flush, SpeakV1Text

SpeakV1SocketClientResponse = Union[str, bytes]

client = DeepgramClient()

# Create output file path
output_path = Path("output.raw").resolve()

try:
    with open(output_path, "wb") as audio_file:
        with client.speak.v1.connect(model="aura-2-asteria-en", encoding="linear16", sample_rate=24000) as connection:

            def on_message(message: SpeakV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    print("Received audio data")
                    audio_file.write(message)
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    print(f"Received {msg_type} event")

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

            # For sync version: Send messages before starting to listen
            # Note: start_listening() blocks, so send all messages first
            # For better control with bidirectional communication, use the async version
            text_message = SpeakV1Text(text="Hello, this is a text to speech example.")
            connection.send_text(text_message)

            # Flush to ensure all text is processed
            flush_message = SpeakV1Flush(type="Flush")
            connection.send_flush(flush_message)

            # Close the connection when done
            close_message = SpeakV1Close(type="Close")
            connection.send_close(close_message)

            # Start listening - this blocks until the connection closes
            # All messages should be sent before calling this in sync mode
            connection.start_listening()

    print(f"Audio saved to {output_path}")

    # For async version:
    # import asyncio
    # from pathlib import Path
    # from deepgram import AsyncDeepgramClient
    # output_path = Path("output.raw").resolve()
    # async with client.speak.v1.connect(model="aura-2-asteria-en", encoding="linear16", sample_rate=24000) as connection:
    #     async def on_message(message):
    #         if isinstance(message, bytes):
    #             with open(output_path, "ab") as audio_file:
    #                 audio_file.write(message)
    #         else:
    #             msg_type = getattr(message, "type", "Unknown")
    #             print(f"Received {msg_type} event")
    #
    #     connection.on(EventType.MESSAGE, on_message)
    #
    #     listen_task = asyncio.create_task(connection.start_listening())
    #     await connection.send_text(SpeakV1Text(text="Hello, this is a text to speech example."))
    #     await connection.send_flush(SpeakV1Flush(type="Flush"))
    #     await connection.send_close(SpeakV1Close(type="Close"))
    #     await listen_task
    # print(f"Audio saved to {output_path}")

except Exception as e:
    print(f"Error: {e}")
