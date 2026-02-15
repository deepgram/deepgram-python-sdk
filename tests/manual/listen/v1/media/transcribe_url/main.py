from dotenv import load_dotenv

print("Starting transcribe_url example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import DeepgramClient

print("Initializing DeepgramClient")
client = DeepgramClient()
print("DeepgramClient initialized")

try:
    model = "nova-3"
    url = "https://dpgr.am/spacewalk.wav"
    print(f"Sending transcription request - Model: {model}, URL: {url}")
    response = client.listen.v1.media.transcribe_url(
        model=model,
        url=url,
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
