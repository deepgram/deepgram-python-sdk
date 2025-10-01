import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Request sent")
    response = client.speak.v1.audio.generate(
        text="Hello, this is a sample text to speech conversion.",
    )
    print("Response received")
except Exception as e:
    print(f"Caught: {e}")
