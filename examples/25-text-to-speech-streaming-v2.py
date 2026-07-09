"""
Example: Text-to-Speech Streaming with the Speak V2 (Flux) WebSocket

This example shows how to stream text-to-speech conversion using the Speak V2
WebSocket. Speak V2 uses Flux voices (model strings of the form
`flux-{voice}-{language}`, e.g. `flux-alexis-en`); use Speak V1 for Aura voices.
"""

from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v2.types import SpeakV2Speak

SpeakV2SocketClientResponse = Union[str, bytes]

client = DeepgramClient()

try:
    with client.speak.v2.connect(model="flux-alexis-en", encoding="linear16", sample_rate="24000") as connection:

        def on_message(message: SpeakV2SocketClientResponse) -> None:
            if isinstance(message, bytes):
                print("Received audio data")
                # In production, you would write this audio data to a file or play it
                # with open("output.raw", "ab") as audio_file:
                #     audio_file.write(message)
            else:
                msg_type = getattr(message, "type", "Unknown")
                print(f"Received {msg_type} event")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # For sync version: Send messages before starting to listen
        # Note: start_listening() blocks, so send all messages first
        # For better control with bidirectional communication, use the async version
        connection.send_speak(SpeakV2Speak(text="Hello, this is a text to speech example."))

        # Flush to ensure all text is processed
        connection.send_flush()

        # Close the connection when done
        connection.send_close()

        # Start listening - this blocks until the connection closes
        # All messages should be sent before calling this in sync mode
        connection.start_listening()

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.speak.v2.connect(...) as connection:
    #     listen_task = asyncio.create_task(connection.start_listening())
    #     await connection.send_speak(SpeakV2Speak(text="..."))
    #     await connection.send_flush()
    #     await connection.send_close()
    #     await listen_task

except Exception as e:
    print(f"Error: {e}")
