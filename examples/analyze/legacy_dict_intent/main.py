# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs
from datetime import datetime, timedelta

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AnalyzeOptions,
    TextSource,
)

load_dotenv()

TEXT_FILE = "conversation.txt"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key in the environment variables
        # config = DeepgramClientOptions(
        #     verbose=logging.SPAM,
        # )
        # deepgram = DeepgramClient("", config)
        # OR use defaults
        deepgram = DeepgramClient()

        # STEP 2 Call the transcribe_file method on the prerecorded class
        with open(TEXT_FILE, "r") as file:
            buffer_data = file.read()

        payload: TextSource = {
            "buffer": buffer_data,
        }

        options = {
            "language": "en",
            "intents": True,
        }

        before = datetime.now()
        response = deepgram.read.analyze.v("1").analyze_text(payload, options)
        after = datetime.now()

        print(response.to_json(indent=4))
        print("")
        difference = after - before
        print(f"time: {difference.seconds}")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
