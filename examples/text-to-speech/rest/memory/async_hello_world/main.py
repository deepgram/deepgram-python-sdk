# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio, aiofiles
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    SpeakOptions,
)

load_dotenv()

SPEAK_TEXT = {"text": "Hello world!"}
filename = "test.mp3"


async def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key="", config=ClientOptionsFromEnv())

        # STEP 2 Call the save method on the asyncspeak property
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        response = await deepgram.speak.asyncrest.v("1").stream_memory(
            SPEAK_TEXT, options
        )

        # save to file
        async with aiofiles.open(filename, "wb") as out:
            await out.write(response.stream_memory.getbuffer())
            await out.flush()

        # file metadata
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
