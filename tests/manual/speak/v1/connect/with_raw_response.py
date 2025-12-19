from dotenv import load_dotenv

print("Starting speak v1 connect with raw response example script")
load_dotenv()
print("Environment variables loaded")

import threading
import time

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.speak.v1.types import (
    SpeakV1Cleared,
    SpeakV1Flushed,
    SpeakV1Metadata,
    SpeakV1Warning,
)
from typing import Union

SpeakV1SocketClientResponse = Union[str, SpeakV1Metadata, SpeakV1Flushed, SpeakV1Cleared, SpeakV1Warning]

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    model = "aura-2-asteria-en"
    encoding = "linear16"
    sample_rate = 24000
    print(
        f"Establishing connection with raw response - Model: {model}, Encoding: {encoding}, Sample Rate: {sample_rate}"
    )
    with client.speak.v1.with_raw_response.connect(
        model=model, encoding=encoding, sample_rate=sample_rate
    ) as connection:
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

        # EXAMPLE ONLY: Start listening in a background thread for demo purposes
        # In production, you would typically call connection.start_listening() directly
        # which blocks until the connection closes, or integrate into your async event loop
        print("Starting listening thread")
        threading.Thread(target=connection.start_listening, daemon=True).start()

        # Send control messages
        from deepgram.speak.v1.types import SpeakV1Flush, SpeakV1Close

        print("Sending Flush control message")
        connection.send_speak_v_1_flush(SpeakV1Flush(type="Flush"))
        print("Sending Close control message")
        connection.send_speak_v_1_close(SpeakV1Close(type="Close"))

        print("Waiting 3 seconds for events...")
        time.sleep(3)  # EXAMPLE ONLY: Wait briefly to see some events before exiting
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
print("Script completed")
