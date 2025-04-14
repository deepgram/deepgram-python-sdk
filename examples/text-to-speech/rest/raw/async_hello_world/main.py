# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import aiofiles
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    SpeakOptions,
)

load_dotenv()

SPEAK_TEXT = {"text": "Hello world!"}
filename = "test.mp3"


async def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        config: DeepgramClientOptions = DeepgramClientOptions(
            # verbose=verboselogs.SPAM,
        )
        deepgram: DeepgramClient = DeepgramClient("", config)

        # STEP 2 Call the save method on the asyncspeak property
        options = SpeakOptions(
            model="aura-2-thalia-en",
        )

        response = await deepgram.speak.asyncrest.v("1").stream_raw(SPEAK_TEXT, options)

        print(f"Response: {response}")
        for header in response.headers:
            print(f"{header}: {response.headers[header]}")
        async with aiofiles.open(filename, "wb") as out:
            async for data in response.aiter_bytes():
                await out.write(data)
                await out.flush()
        await response.aclose()

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
