# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import aiofiles
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from datetime import datetime
import httpx

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

AUDIO_FILE = "preamble.wav"


async def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config: DeepgramClientOptions = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram: DeepgramClient = DeepgramClient("", config)
        # OR use defaults
        # deepgram: DeepgramClient = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the rest class
        async with aiofiles.open(AUDIO_FILE, "rb") as file:
            buffer_data = await file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )

        before = datetime.now()
        response = await deepgram.listen.asyncrest.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        after = datetime.now()

        print(response.to_json(indent=4))
        print("")
        difference = after - before
        print(f"time: {difference.seconds}")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
