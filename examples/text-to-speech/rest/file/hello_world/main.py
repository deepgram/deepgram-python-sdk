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

SPEAK_TEXT = {"text": "Hello world!"}
filename = "test.mp3"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(
            api_key="", config=ClientOptionsFromEnv(verbose=verboselogs.SPAM)
        )

        # STEP 2 Call the save method on the speak property
        options = SpeakOptions(
            model="aura-2-thalia-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
