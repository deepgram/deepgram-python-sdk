"""
Example: WebSocket Request Options - Additional Headers and Query Parameters

This example shows how to use request_options with WebSocket connections
to add additional headers and query parameters to the connection request.
"""

import os
import threading
import time

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import ListenV1Results

# Audio streaming configuration
CHUNK_SIZE = 8192
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
CHANNELS = 1
CHUNK_DELAY = CHUNK_SIZE / (SAMPLE_RATE * SAMPLE_WIDTH * CHANNELS)

client = DeepgramClient()

try:
    print("Connecting to Deepgram WebSocket with custom request options...")

    # Connect with additional headers and query parameters
    with client.listen.v1.connect(
        model="nova-3",
        language="en",
        smart_format=True,
        request_options={
            "additional_headers": {
                "X-Custom-Header": "custom-value",
                "X-Request-ID": "example-request-123",
            },
            # Note: additional_query_parameters are currently not working
            # for WebSocket connections, but the structure is shown here
            # for future compatibility
            "additional_query_parameters": {
                "detect_language": ["en", "es"],
            },
        },
    ) as connection:

        print("Connected successfully with custom headers!")

        # Register event handlers
        def on_open(_):
            print("Connection opened")

        def on_message(message):
            if isinstance(message, ListenV1Results):
                if message.channel and message.channel.alternatives:
                    transcript = message.channel.alternatives[0].transcript
                    if transcript:
                        print(f"Transcript: {transcript}")

        def on_error(error):
            print(f"Error: {error}")

        def on_close(_):
            print("Connection closed")

        connection.on(EventType.OPEN, on_open)
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.ERROR, on_error)
        connection.on(EventType.CLOSE, on_close)

        # Define a function to send audio in a background thread
        def send_audio():
            audio_path = os.path.join(os.path.dirname(__file__), "fixtures", "audio.wav")

            with open(audio_path, "rb") as audio_file:
                print(f"Streaming audio from {audio_path}")

                while True:
                    chunk = audio_file.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    connection.send_media(chunk)
                    time.sleep(CHUNK_DELAY)

            print("Finished sending audio")

        # Start sending audio in a background thread
        threading.Thread(target=send_audio, daemon=True).start()

        # Start listening - this blocks until the connection closes or times out
        connection.start_listening()

    # Additional request_options that can be used:
    # with client.listen.v1.connect(
    #     model="nova-3",
    #     language="en",
    #     smart_format=True,
    #     request_options={
    #         "additional_headers": {
    #             "X-Custom-Header": "custom-value",
    #             "X-Request-ID": "example-request-123",
    #             "X-Client-Version": "1.0.0",
    #         },
    #         "additional_query_parameters": {
    #             "detect_language": ["en", "es"],
    #             # Note: Additional query parameters for WebSocket are
    #             # currently not working, but may be supported in the future
    #         },
    #         "timeout_in_seconds": 30,
    #     }
    # ) as connection:
    #     # ... register handlers and start listening

except Exception as e:
    print(f"Error: {e}")
