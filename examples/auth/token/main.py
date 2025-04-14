# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions
)

load_dotenv()

def main():
    try:
        # STEP 1 Create a Deepgram client using the DEEPGRAM_API_KEY from your environment variables
        config = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram: DeepgramClient = DeepgramClient(os.getenv("DEEPGRAM_API_KEY", ""), config)

        # STEP 2 Call the grant_token method on the auth rest class
        response = deepgram.auth.v("1").grant_token()
        print(f"response: {response}\n\n")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
