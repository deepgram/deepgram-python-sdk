# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
from deepgram.utils import verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions

load_dotenv()


def main():
    try:
        # STEP 1 Create a Deepgram client using the DEEPGRAM_API_KEY from your environment variables
        config = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram: DeepgramClient = DeepgramClient(
            os.getenv("DEEPGRAM_API_KEY", ""), config
        )

        # STEP 2 Call the grant_token method on the auth rest class
        print("Testing grant_token with default TTL (30 seconds)...")
        response = deepgram.auth.v("1").grant_token()
        print(f"Default TTL response: {response}\n")

        # STEP 3 Call the grant_token method with custom TTL
        print("Testing grant_token with custom TTL (300 seconds)...")
        response_custom = deepgram.auth.v("1").grant_token(ttl_seconds=300)
        print(f"Custom TTL response: {response_custom}\n")

        # STEP 4 Test boundary values
        print("Testing grant_token with minimum TTL (1 second)...")
        response_min = deepgram.auth.v("1").grant_token(ttl_seconds=1)
        print(f"Minimum TTL response: {response_min}\n")

        print("Testing grant_token with maximum TTL (3600 seconds)...")
        response_max = deepgram.auth.v("1").grant_token(ttl_seconds=3600)
        print(f"Maximum TTL response: {response_max}\n")

        print("✅ All grant_token tests completed successfully!")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
