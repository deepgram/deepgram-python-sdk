# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from datetime import datetime, timedelta
from io import BufferedReader
from deepgram import DeepgramClientOptions
import logging

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    StreamSource,
    PrerecordedOptions,
)

load_dotenv()

AUDIO_FILE = "preamble.wav"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram = DeepgramClient("", config)
        # OR use defaults
        # deepgram = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the rest class
        with open(AUDIO_FILE, "rb") as stream:
            payload: StreamSource = {
                "stream": stream,
            }
            options = PrerecordedOptions(
                model="nova-3",
            )
            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
            print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
