# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from datetime import datetime, timedelta

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
    UrlSource,
)

load_dotenv()

AUDIO_FILE = "preamble.wav"
CALL_BACK_URL = (
    "https://127.0.0.1:8000"  # TODO: MUST REPLACE WITH YOUR OWN CALLBACK ENDPOINT
)


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config: DeepgramClientOptions = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )

        deepgram: DeepgramClient = DeepgramClient("", config)

        # STEP 2 Call the transcribe_file method on the rest class
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }
        # For URL hosted audio files, comment out the above and uncomment the below
        # payload: UrlSource = {
        #     "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
        # }

        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
            utterances=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_file_callback(
            payload, CALL_BACK_URL, options=options
        )
        # For URL hosted audio files, comment out the above and uncomment the below
        # response = deepgram.listen.rest.v("1").transcribe_url_callback(
        #     payload, CALL_BACK_URL, options=options
        # )
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
