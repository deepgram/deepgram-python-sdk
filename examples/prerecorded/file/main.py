# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
from dotenv import load_dotenv

from deepgram import DeepgramClient, PrerecordedOptions, FileSource

load_dotenv()

API_KEY = os.getenv('DG_API_KEY')
AUDIO_FILE = "preamble.wav"

options: PrerecordedOptions = {
    "model": "nova",
    "smart_format": "true",
    "summarize": "v2",
}

# STEP 1 Create a Deepgram client using the API key (optional - add config options)
deepgram = DeepgramClient(API_KEY)

# STEP 2 Call the transcribe_file method on the prerecorded class
async def transcribe_file():
    # Logic to read the file
    with open(AUDIO_FILE, 'rb') as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }
    
    file_response = await deepgram.listen.prerecorded.transcribe_file(payload, options)
    return file_response

async def main():
    try:
        response = await transcribe_file()
        print(response)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
