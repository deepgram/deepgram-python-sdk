# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
from dotenv import load_dotenv

from deepgram import DeepgramClient, PrerecordedOptions

load_dotenv()

API_KEY = os.getenv("DG_API_KEY")
AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}

options: PrerecordedOptions = PrerecordedOptions(
    model="nova-2",
    smart_format=True,
    summarize="v2",
)

# STEP 1 Create a Deepgram client using the API key (optional - add config options)
deepgram: DeepgramClient = DeepgramClient(API_KEY)


# STEP 2 Call the transcribe_url method on the prerecorded class
async def transcribe_url():
    url_response = await deepgram.listen.asyncprerecorded.v("1").transcribe_url(
        AUDIO_URL, options
    )
    return url_response


async def main():
    try:
        response = await transcribe_url()
        print(response.to_json(indent=4))
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
