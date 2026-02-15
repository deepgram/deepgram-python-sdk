import asyncio
import os

from dotenv import load_dotenv

print("Starting async transcribe_file example script")
load_dotenv()
print("Environment variables loaded")

from deepgram import AsyncDeepgramClient

print("Initializing AsyncDeepgramClient")
client = AsyncDeepgramClient()
print("AsyncDeepgramClient initialized")


async def main() -> None:
    try:
        # Path to audio file from fixtures
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(script_dir, "..", "..", "..", "..", "fixtures", "audio.wav")
        print(f"Loading audio file from: {audio_path}")
        
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()
        print(f"Audio file loaded, size: {len(audio_data)} bytes")

        model = "nova-3"
        print(f"Sending async transcription request - Model: {model}")
        response = await client.listen.v1.media.transcribe_file(
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


print("Running async main function")
asyncio.run(main())
print("Script completed")
