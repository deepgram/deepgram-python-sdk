# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions

load_dotenv()

AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}

def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient()

        # STEP 2 Call the transcribe_url method on the prerecorded class
        options = PrerecordedOptions(
            model="nova",
            smart_format=True,
            summarize="v2",
        )
        url_response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
        print(url_response)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
