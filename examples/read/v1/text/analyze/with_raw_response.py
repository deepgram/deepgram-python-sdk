from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Request sent")
    response = client.read.v1.text.with_raw_response.analyze(
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
