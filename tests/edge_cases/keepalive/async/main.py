# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import time
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


async def main():
    # for debugging
    config: DeepgramClientOptions = DeepgramClientOptions(
        verbose=logging.DEBUG, options={"keepalive": "true"}
    )
    deepgram: DeepgramClient = DeepgramClient("", config)

    deepgram_connection = deepgram.listen.asynclive.v("1")

    await deepgram_connection.start(LiveOptions())

    # Wait for a while to simulate a long-running connection
    await asyncio.sleep(600)

    print("deadlock!")
    try:
        await deepgram_connection.finish()
    finally:
        print("no deadlock...")


asyncio.run(main())
