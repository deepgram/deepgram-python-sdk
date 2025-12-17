"""
Example: Live Transcription with WebSocket (Listen V1)

This example shows how to stream audio for real-time transcription using WebSocket.
"""

import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

client = DeepgramClient()

try:
    with client.listen.v1.connect(model="nova-3") as connection:
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

        # Start listening - this blocks until the connection closes
        # In production, you would send audio data here:
        # audio_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "audio.wav")
        # with open(audio_path, "rb") as audio_file:
        #     audio_data = audio_file.read()
        #     connection.send_listen_v_1_media(audio_data)
        
        connection.start_listening()
        
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # async with client.listen.v1.connect(model="nova-3") as connection:
    #     # ... same event handlers ...
    #     await connection.start_listening()
    
except Exception as e:
    print(f"Error: {e}")

