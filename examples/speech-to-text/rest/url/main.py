# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    PrerecordedOptions,
)

load_dotenv()

AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}


def main():
    try:
        # STEP 1 Create a Deepgram client using the DEEPGRAM_API_KEY from your environment variables
        deepgram: DeepgramClient = DeepgramClient()

        # STEP 2 Call the transcribe_url method on the rest class
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )
        response = deepgram.listen.rest.v("1").transcribe_url(AUDIO_URL, options)
        print(f"response: {response}\n\n")
        # print(f"metadata: {response['metadata']}\n\n")
        # print(
        #     f"transcript: {response.results.channels[0].alternatives[0]['transcript']}\n\n"
        # )
        # for word in response.results.channels[0].alternatives[0].words:
        #     print(f"Word: {word.word}, Start: {word.start}, End: {word.end}")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
