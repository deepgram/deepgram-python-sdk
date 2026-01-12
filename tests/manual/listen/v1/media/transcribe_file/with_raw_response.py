import os

from dotenv import load_dotenv

print("Starting transcribe_file with raw response example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    # Path to audio file from fixtures
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(script_dir, "..", "..", "..", "..", "fixtures", "audio.wav")
    print(f"Loading audio file from: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    print(f"Audio file loaded, size: {len(audio_data)} bytes")

    model = "nova-3"
    print(f"Sending transcription request with raw response - Model: {model}")
    response = client.listen.v1.media.with_raw_response.transcribe_file(
        request=audio_data,
        model=model,
    )
    print("Raw response received successfully")
    print(f"Response type: {type(response)}")
    if hasattr(response, "status_code"):
        print(f"Status code: {response.status_code}")
    if hasattr(response, "headers"):
        print(f"Response headers: {response.headers}")
    # Extract full transcription from response body
    if hasattr(response, "parsed") and response.parsed:
        parsed = response.parsed
        if hasattr(parsed, "results") and parsed.results:
            if hasattr(parsed.results, "channels") and parsed.results.channels:
                channel = parsed.results.channels[0]
                if hasattr(channel, "alternatives") and channel.alternatives:
                    transcript = (
                        channel.alternatives[0].transcript if hasattr(channel.alternatives[0], "transcript") else None
                    )
                    if transcript:
                        print(f"Full transcription: {transcript}")
                    else:
                        print(f"Response body: {parsed}")
                else:
                    print(f"Response body: {parsed}")
            else:
                print(f"Response body: {parsed}")
        else:
            print(f"Response body: {parsed}")
    elif hasattr(response, "body"):
        print(f"Response body: {response.body}")
    else:
        print(f"Response: {response}")
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
