# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.clients.manage.client import ManageClientV1

load_dotenv()

API_KEY = os.getenv('DG_API_KEY_MANAGE')

# Create a Deepgram client using the API key
deepgram: DeepgramClient = DeepgramClient(API_KEY)

async def main():
    try:
        response = await deepgram.manage.get_projects()
        print(response)

        # FUTURE VERSIONINING:
        #   response = await deepgram.manage_v1.get_projects()
        #   print(response)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())