# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
import threading

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()


def main():
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        # config: DeepgramClientOptions = DeepgramClientOptions(verbose=verboselogs.DEBUG)
        # deepgram: DeepgramClient = DeepgramClient("", config)
        # otherwise, use default config
        deepgram: DeepgramClient = DeepgramClient()

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.websocket.v("1")

        def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        # def on_metadata(self, metadata, **kwargs):
        #     print(f"\n\n{metadata}\n\n")

        # def on_speech_started(self, speech_started, **kwargs):
        #     print(f"\n\n{speech_started}\n\n")

        # def on_utterance_end(self, utterance_end, **kwargs):
        #     print(f"\n\n{utterance_end}\n\n")

        def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        # def on_unhandled(self, unhandled, **kwargs):
        #     print(f"\n\n{unhandled}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        # dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        # dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        # dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        # dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        # connect to websocket
        options = LiveOptions(
            model="nova-3",
            language="en-US",
            encoding="linear16",
            sample_rate=22050,
            smart_format=True,
        )

        print("\n\nPress Enter to stop recording...\n\n")
        if dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        # open file for reading
        with open("microsoft_headquarters.wav", "rb") as f:
            dg_connection.send(f.read())

        # signal finished
        input("")

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
