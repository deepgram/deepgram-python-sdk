# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import time
import logging
from deepgram.utils import verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


def main():
    # for debugging
    config: DeepgramClientOptions = DeepgramClientOptions(
        verbose=verboselogs.DEBUG, options={"keepalive": "true"}
    )
    deepgram: DeepgramClient = DeepgramClient("", config)
    # OR
    # deepgram: DeepgramClient = DeepgramClient()

    deepgram_connection = deepgram.listen.live.v("1")

    deepgram_connection.start(LiveOptions())

    # press any key to exit
    input("\n\nPress Enter to exit...\n\n")

    print("deadlock!")
    try:
        deepgram_connection.finish()
    finally:
        print("no deadlock...")


if __name__ == "__main__":
    main()
