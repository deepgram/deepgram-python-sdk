import asyncio

from dotenv import load_dotenv

print("Starting async speak v1 connect example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v1.types import (
    SpeakV1Cleared,
    SpeakV1Flushed,
    SpeakV1Metadata,
    SpeakV1Warning,
)
from typing import Union

SpeakV1SocketClientResponse = Union[str, SpeakV1Metadata, SpeakV1Flushed, SpeakV1Cleared, SpeakV1Warning]

print("Initializing AsyncDeepgramClient")
client = AsyncDeepgramClient()
print("AsyncDeepgramClient initialized")


async def main() -> None:
    try:
        model = "aura-2-asteria-en"
        encoding = "linear16"
        sample_rate = 24000
        print(f"Establishing async connection - Model: {model}, Encoding: {encoding}, Sample Rate: {sample_rate}")
        async with client.speak.v1.connect(model=model, encoding=encoding, sample_rate=sample_rate) as connection:
            print("Connection context entered")

            def on_message(message: SpeakV1SocketClientResponse) -> None:
                if isinstance(message, bytes):
                    print("Received audio event")
                    print(f"Event body (audio data length): {len(message)} bytes")
                else:
                    msg_type = getattr(message, "type", "Unknown")
                    print(f"Received {msg_type} event")
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

            # Send control messages
            from deepgram.speak.v1.types import SpeakV1Flush, SpeakV1Close

            print("Sending Flush control message")
            await connection.send_speak_v_1_flush(SpeakV1Flush(type="Flush"))
            print("Sending Close control message")
            await connection.send_speak_v_1_close(SpeakV1Close(type="Close"))

            print("Waiting 3 seconds for events...")
            await asyncio.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
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
