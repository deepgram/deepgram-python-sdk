# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dotenv import load_dotenv
import logging, verboselogs
from time import sleep

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()


def main():
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        # config = DeepgramClientOptions(
        #     verbose=logging.DEBUG,
        #     options={"keepalive": "true"}
        # )
        # deepgram: DeepgramClient = DeepgramClient("", config)
        # otherwise, use default config
        deepgram = DeepgramClient()

        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, addon=dict(myattr=True), **kwargs):
            if result is None:
                return
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

            # testing modifying self class
            if self.myattr is not None:
                print(f"myattr - {self.myattr}")
            else:
                print("Setting myattr=hello")
                setattr(self, "myattr", "hello")
            self.myattr = "bye"

            # testing kwargs
            val = kwargs["test"]
            print(f"kwargs - {val}")

        def on_metadata(self, metadata, **kwargs):
            if metadata is None:
                return
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            if error is None:
                return
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        dg_connection.start(options, addons=dict(myattr="hello"), test="hello")

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")
        # sleep(30)  # wait 30 seconds to see if there is any additional socket activity
        # print("Really done!")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
