import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Request sent")
    with client.speak.v1.audio.with_raw_response.generate(
        text="Hello, this is a sample text to speech conversion.",
    ) as response:
        print("Response received")
except Exception as e:
    print(f"Caught: {e}")
