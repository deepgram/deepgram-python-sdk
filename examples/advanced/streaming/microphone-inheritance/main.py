# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dotenv import load_dotenv
import logging, verboselogs
from time import sleep

from deepgram import (
    ClientOptionsFromEnv,
    LiveTranscriptionEvents,
    LiveClient,
    LiveOptions,
    Microphone,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    ErrorResponse,
)

load_dotenv()


# more complex example
class MyLiveClient(LiveClient):
    def __init__(self, config: LiveClient):
        super().__init__(config)
        super().on(LiveTranscriptionEvents.Transcript, self.on_message)
        super().on(LiveTranscriptionEvents.Metadata, self.on_metadata)
        super().on(LiveTranscriptionEvents.SpeechStarted, self.on_speech_started)
        super().on(LiveTranscriptionEvents.UtteranceEnd, self.on_utterance_end)
        super().on(LiveTranscriptionEvents.Error, self.on_error)
        # self.test = "child"

    def on_message(self, parent, result, **kwargs):
        # print(f"child attr: {self.test}")
        # print(f"parent attr: {parent.endpoint}")
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

    def on_metadata(self, parent, metadata, **kwargs):
        print(f"\n\n{metadata}\n\n")

    def on_speech_started(self, parent, speech_started, **kwargs):
        print(f"\n\n{speech_started}\n\n")

    def on_utterance_end(self, parent, utterance_end, **kwargs):
        print(f"\n\n{utterance_end}\n\n")

    def on_error(self, parent, error, **kwargs):
        print(f"\n\n{error}\n\n")


def main():
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        # config: ClientOptionsFromEnv = ClientOptionsFromEnv(
        #     verbose=logging.DEBUG,
        #     options={"keepalive": "true"}
        # )
        # liveClient: MyLiveClient = MyLiveClient(config)
        # otherwise, use default config
        liveClient: MyLiveClient = MyLiveClient(ClientOptionsFromEnv())

        options: LiveOptions = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
        )
        liveClient.start(
            options,
            members=dict(myattr="hello", mytest="goodbye"),
            addons=dict(smart_format=True),
            test="hello",
        )

        # Open a microphone stream
        microphone: Microphone = Microphone(liveClient.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        liveClient.finish()

        print("Finished")
        # sleep(30)  # wait 30 seconds to see if there is any additional socket activity
        # print("Really done!")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
