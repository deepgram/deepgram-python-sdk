import os

from dotenv import load_dotenv

print("Starting speak v1 audio generate example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    text = "Hello, this is a sample text to speech conversion."
    print(f"Sending text-to-speech generation request - Text: {text[:50]}...")
    response = client.speak.v1.audio.generate(
        text=text,
    )
    print("Response received successfully")
    print(f"Response type: {type(response)}")
    if hasattr(response, "audio"):
        print(f"Audio data length: {len(response.audio) if response.audio else 0} bytes")
    print(f"Response body: {response}")
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
