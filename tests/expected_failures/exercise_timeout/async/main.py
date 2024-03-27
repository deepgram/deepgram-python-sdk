# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import time
import logging, verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


async def main():
    # for debugging
    config: DeepgramClientOptions = DeepgramClientOptions(verbose=logging.DEBUG)
    deepgram: DeepgramClient = DeepgramClient("", config)
    # OR
    # deepgram: DeepgramClient = DeepgramClient()

    deepgram_connection = deepgram.listen.asynclive.v("1")

    await deepgram_connection.start(LiveOptions())

    # Deepgram will close the connection after 10-15s of silence, followed with another 5 seconds for a ping
    await asyncio.sleep(30)

    print("deadlock!")
    try:
        await deepgram_connection.finish()
    finally:
        print("no deadlock...")


asyncio.run(main())
