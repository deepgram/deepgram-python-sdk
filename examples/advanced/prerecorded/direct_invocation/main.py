# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs
import traceback

from deepgram import ClientOptionsFromEnv, PrerecordedOptions, PreRecordedClient

load_dotenv()

AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}


def main():
    try:
        # STEP 1 Create a Deepgram PreRecordedClient using a specific config
        # config: ClientOptionsFromEnv = ClientOptionsFromEnv(
        #     verbose=verboselogs.NOTICE,
        # )
        # asyncClient: PreRecordedClient = PreRecordedClient(config)
        # OR just use the default config
        asyncClient: PreRecordedClient = PreRecordedClient(ClientOptionsFromEnv())

        # STEP 2 Call the transcribe_url method on the prerecorded class
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            summarize="v2",
        )
        response = asyncClient.transcribe_url(AUDIO_URL, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
