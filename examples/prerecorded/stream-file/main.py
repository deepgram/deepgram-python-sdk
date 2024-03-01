# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs
from datetime import datetime, timedelta
from io import BufferedReader
from deepgram import DeepgramClientOptions
import logging

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    ReadStreamSource,
    PrerecordedOptions,
)

load_dotenv()

AUDIO_FILE = "preamble.wav"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config = DeepgramClientOptions(
            verbose=logging.SPAM,
        )
        deepgram = DeepgramClient("", config)
        # OR use defaults
        # deepgram = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the prerecorded class
        stream = open(AUDIO_FILE, "rb")

        payload: ReadStreamSource = {
            "stream": stream,
        }

        options = PrerecordedOptions(
            model="nova",
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        print(response.to_json(indent=4))

        stream.close()

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
