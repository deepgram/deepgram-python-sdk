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

options = PrerecordedOptions(
    model="nova",
    smart_format=True,
    summarize="v2",
)

# STEP 1 Create a Deepgram client using the API key (optional - add config options)
config = DeepgramClientOptions(
    verbose=logging.SPAM,
)

deepgram = DeepgramClient("", config)


# STEP 2 Call the transcribe_url method on the prerecorded class
def transcribe_url():
    url_response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
    return url_response


def main():
    try:
        response = transcribe_url()
        print(response)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
