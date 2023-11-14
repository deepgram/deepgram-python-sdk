from deepgram import DeepgramClient, PrerecordedOptions
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('DG_API_KEY')
AUDIO_FILE = "preamble.wav"
AUDIO_URL = {"url":"https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"}
CALLBACK = "https://example.com/callback"

options: PrerecordedOptions = {
    "model": "nova",
    "smart_format": "true",
    "summarize": "v2",
}

# STEP 1 Create a Deepgram client using the API key (optional - add config options)
deepgram = DeepgramClient(API_KEY)

###### TRANSCRIBE A LOCAL FILE #####
async def transcribe_file():
    # Logic to read the file
    with open(AUDIO_FILE, 'rb') as file:
        buffer_data = file.read()

    PAYLOAD = {
        "buffer": buffer_data,
    }

    # STEP 2 Call the transcribe_file method on the prerecorded class
    file_response = await deepgram.listen.prerecorded.transcribe_file(PAYLOAD, options)
    return file_response


###### TRANSCRIBE A HOSTED FILE #####
async def transcribe_url():
    # STEP 2 Call the transcribe_url method on the prerecorded class
    url_response = await deepgram.listen.prerecorded.transcribe_url(AUDIO_URL, options)
    # url_response = await deepgram.listen.prerecorded.transcribe_url_callback(AUDIO_URL,CALLBACK, options)
    return url_response


async def main():
    # response = await transcribe_file()
    response = await transcribe_url()
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
