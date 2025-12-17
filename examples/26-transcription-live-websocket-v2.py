"""
Example: Live Transcription with WebSocket V2 (Listen V2)

This example shows how to use Listen V2 for advanced conversational speech recognition
with contextual turn detection.
"""

from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)

ListenV2SocketClientResponse = Union[ListenV2Connected, ListenV2TurnInfo, ListenV2FatalError]

client = DeepgramClient()

try:
    with client.listen.v2.connect(model="flux-general-en", encoding="linear16", sample_rate="16000") as connection:

        def on_message(message: ListenV2SocketClientResponse) -> None:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

            # Extract transcription from TurnInfo events
            if isinstance(message, ListenV2TurnInfo):
                print(f"Turn transcript: {message.transcript}")
                print(f"Turn event: {message.event}")
                print(f"Turn index: {message.turn_index}")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
        connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        # Start listening - this blocks until the connection closes
        # In production, you would send audio data here using connection.send_listen_v_2_media()
        connection.start_listening()

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.listen.v2.connect(...) as connection:
    #     # ... same event handlers ...
    #     await connection.start_listening()

except Exception as e:
    print(f"Error: {e}")
