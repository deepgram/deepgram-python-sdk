# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    SpeakOptions,
)

load_dotenv()

SPEAK_OPTIONS = {"text": "Hello world!"}
filename = "test.mp3"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(
            api_key="", config=ClientOptionsFromEnv(verbose=verboselogs.SPAM)
        )

        # STEP 2 Call the save method on the speak property
        options = SpeakOptions(
            model="aura-asteria-en",
        )

        response = deepgram.speak.rest.v("1").stream_memory(SPEAK_OPTIONS, options)

        # save to file
        with open(filename, "wb+") as file:
            file.write(response.stream_memory.getbuffer())
            file.flush()

        # file metadata
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
