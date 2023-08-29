# Example filename: deepgram_test.py

import json
import asyncio

from deepgram import Deepgram

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'

# Location of the file you want to transcribe. Should include filename and extension.
# Example of a local file: ../../Audio/life-moves-pretty-fast.wav
# Example of a remote file: https://static.deepgram.com/examples/interview_speech-analytics.wav
FILE = 'https://static.deepgram.com/examples/interview_speech-analytics.wav'

# Mimetype for the file you want to transcribe
# Include this line only if transcribing a local file
# Example: audio/wav
MIMETYPE = 'audio/mpeg'


async def main():

    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # Check whether requested file is local or remote, and prepare source
    if FILE.startswith('http'):
        # file is remote
        # Set the source
        source = {
            'url': FILE
        }
    else:
        # file is local
        # Open the audio file
        audio = open(FILE, 'rb')

        # Set the source
        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }

    # Send the audio to Deepgram and get the response
    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            {
                'detect_language': "true",
                'summarize': "v2",
            }
        )
    )

    # Write the response to the console
    print(json.dumps(response, indent=4))

    # Write only the transcript to the console
    # print(response["results"]["channels"][0]["alternatives"][0]["transcript"])

    # print(response["results"]["channels"])

try:
    # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
    # await main()
    asyncio.run(main())
except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno
    print(f'line {line_number}: {exception_type} - {e}')
