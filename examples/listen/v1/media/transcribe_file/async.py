import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient()

async def main() -> None:
    try:
        # Path to audio file from fixtures
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(script_dir, "..", "..", "..", "..", "fixtures", "audio.wav")
        
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()

        print("Request sent")
        response = await client.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
        )
        print("Response received")
    except Exception as e:
        print(f"Caught: {e}")

asyncio.run(main())
