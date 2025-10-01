import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

try:
    # Using access token instead of API key
    authClient = DeepgramClient()

    print("Request sent")
    authResponse = authClient.auth.v1.tokens.grant()
    print("Response received")

    client = DeepgramClient(access_token=authResponse.access_token)

    print("Request sent")
    response = client.speak.v1.audio.generate(
        text="Hello, this is a sample text to speech conversion.",
    )
    print("Response received")
except Exception as e:
    print(f"Caught: {e}")
