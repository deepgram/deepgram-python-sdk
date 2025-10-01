from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Request sent")
    response = client.listen.v1.media.transcribe_url(
        model="nova-3",
        url="https://dpgr.am/spacewalk.wav",
    )
    print("Response received")
except Exception as e:
    print(f"Caught: {e}")
