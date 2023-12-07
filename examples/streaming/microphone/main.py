# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import logging, verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

# example of setting up a client config
# config = DeepgramClientOptions(
#     verbose=logging.SPAM,
#     options={'keepalive': 'true'}
# )

options = LiveOptions(
    punctuate=True,
    language="en-US",
    encoding="linear16",
    channels=1,
    sample_rate=16000,
)


def on_message(result=None):
    if result is None:
        return
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    print(f"speaker: {sentence}")


def on_metadata(metadata=None):
    if metadata is None:
        return
    print("")
    print(metadata)
    print("")


def on_error(error=None):
    if error is None:
        return
    print("")
    print(error)
    print("")


def main():
    # to specify a client config
    # deepgram: DeepgramClient = DeepgramClient("", config)
    # otherwise, use default config
    deepgram: DeepgramClient = DeepgramClient()

    try:
        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.live.v("1")
        dg_connection.start(options)

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the connection to close
        microphone.finish()

        # Indicate that we've finished sending data by sending the {"type": "CloseStream"}
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
