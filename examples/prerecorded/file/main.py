# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import (
    DeepgramClientOptions,
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

API_KEY = os.getenv("DG_API_KEY")
AUDIO_FILE = "preamble.wav"

# Create a Deepgram client using the API key
config: DeepgramClientOptions = DeepgramClientOptions(
    verbose=logging.SPAM,
)

options: PrerecordedOptions = PrerecordedOptions(
    model="nova",
    smart_format="true",
    summarize="v2",
)

# STEP 1 Create a Deepgram client using the API key (optional - add config options)
deepgram: DeepgramClient = DeepgramClient(API_KEY, config)


# STEP 2 Call the transcribe_file method on the prerecorded class
async def transcribe_file():
    # Logic to read the file
    with open(AUDIO_FILE, "rb") as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }

    file_response = await deepgram.listen.prerecorded.v("1").transcribe_file(
        payload, options
    )
    return file_response


async def main():
    try:
        response = await transcribe_file()
        print(response)
        print("")
        json = response.to_json()
        print("")
        print(json)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())