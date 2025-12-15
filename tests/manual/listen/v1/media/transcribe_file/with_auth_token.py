import os

from dotenv import load_dotenv

print("Starting transcribe_file with auth token example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

try:
    # Using access token instead of API key
    print("Initializing DeepgramClient for authentication")
    authClient = DeepgramClient()
    print("Auth client initialized")

    print("Requesting access token")
    authResponse = authClient.auth.v1.tokens.grant()
    print("Access token received successfully")
    print(f"Token type: {type(authResponse.access_token)}")

    print("Initializing DeepgramClient with access token")
    client = DeepgramClient(access_token=authResponse.access_token)
    print("Client initialized with access token")

    # Path to audio file from fixtures
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(script_dir, "..", "..", "..", "..", "fixtures", "audio.wav")
    print(f"Loading audio file from: {audio_path}")

    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    print(f"Audio file loaded, size: {len(audio_data)} bytes")

    model = "nova-3"
    print(f"Sending transcription request - Model: {model}")
    response = client.listen.v1.media.transcribe_file(
        request=audio_data,
        model=model,
    )
    print("Response received successfully")
    print(f"Response type: {type(response)}")
    # Extract full transcription from response
    if hasattr(response, "results") and response.results:
        if hasattr(response.results, "channels") and response.results.channels:
            channel = response.results.channels[0]
            if hasattr(channel, "alternatives") and channel.alternatives:
                transcript = (
                    channel.alternatives[0].transcript if hasattr(channel.alternatives[0], "transcript") else None
                )
                if transcript:
                    print(f"Full transcription: {transcript}")
                else:
                    print(f"Response body: {response}")
            else:
                print(f"Response body: {response}")
        else:
            print(f"Response body: {response}")
    else:
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
