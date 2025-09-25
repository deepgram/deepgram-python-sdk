import asyncio

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient()

async def main() -> None:
    try:
        print("Request sent")
        response = await client.read.v1.text.analyze(
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

asyncio.run(main())
