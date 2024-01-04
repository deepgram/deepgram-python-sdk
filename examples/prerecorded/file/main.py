# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import (
    DeepgramClientOptions,
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

AUDIO_FILE = "preamble.wav"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        config: DeepgramClientOptions = DeepgramClientOptions(
            verbose=logging.SPAM,
        )

        deepgram: DeepgramClient = DeepgramClient("", config)

        # STEP 2 Call the transcribe_file method on the prerecorded class
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
