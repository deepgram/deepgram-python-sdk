# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import time
import logging
from deepgram.utils import verboselogs

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


def main():
    # for debugging
    config: DeepgramClientOptions = DeepgramClientOptions(verbose=verboselogs.SPAM)
    deepgram: DeepgramClient = DeepgramClient("", config)
    # OR
    # deepgram: DeepgramClient = DeepgramClient()

    deepgram_connection = deepgram.listen.live.v("1")

    deepgram_connection.start(LiveOptions())

    # Deepgram will close the connection after 10-15s of silence, followed with another 5 seconds for a ping
    time.sleep(30)

    print("deadlock!")
    try:
        deepgram_connection.finish()
    finally:
        print("no deadlock...")


if __name__ == "__main__":
    main()
