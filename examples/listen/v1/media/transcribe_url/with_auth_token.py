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
    response = client.listen.v1.media.transcribe_url(
        model="nova-3",
        url="https://dpgr.am/spacewalk.wav",
    )
    print("Response received")
except Exception as e:
    print(f"Caught: {e}")
