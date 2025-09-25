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
    response = client.read.v1.text.analyze(
        request={"text": "Hello, world!"},
        language="en",
        sentiment=True,
        summarize=True,
        topics=True,
        intents=True,
    )
    print("Response received")
except Exception as e:
    print(f"Caught: {e}")
