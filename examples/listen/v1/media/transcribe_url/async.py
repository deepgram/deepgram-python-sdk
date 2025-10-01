import asyncio

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient()

async def main() -> None:
    try:
        print("Request sent")
        response = await client.listen.v1.media.transcribe_url(
            model="nova-3",
            url="https://dpgr.am/spacewalk.wav",
        )
        print("Response received")
    except Exception as e:
        print(f"Caught: {e}")

asyncio.run(main())
