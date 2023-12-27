# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs
import httpx

from deepgram import (
    DeepgramClientOptions,
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    UrlSource,
    PreRecordedClient,
)

load_dotenv()

AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
AUDIO_FILE = "preamble.wav"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        deepgram: DeepgramClient = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the prerecorded class
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        # comment out/in the one you want to test
        payload: UrlSource = {
            "url": AUDIO_URL,
        }
        # OR
        # payload: FileSource = {
        #     "buffer": buffer_data,
        # }

        options = PrerecordedOptions(
            model="nova",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )
        file_response = deepgram.listen.prerecorded.v("1").transcribe(payload, options)

        print(f"\n\n{file_response}\n\n")
        json = file_response.to_json()
        print(f"{json}\n")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
