# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
import threading

from deepgram import (
    ListenWebSocketClient,
    ClientOptionsFromEnv,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"


def main():
    try:
        # STEP 1 Create a Deepgram ListenWebSocketClient using a specific config
        # config: ClientOptionsFromEnv = ClientOptionsFromEnv(
        #     verbose=verboselogs.DEBUG, options={"keepalive": "true"}
        # )
        # liveClient: ListenWebSocketClient = ListenWebSocketClient("", config)
        # OR just use the default config
        liveClient: ListenWebSocketClient = ListenWebSocketClient(
            ClientOptionsFromEnv()
        )

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_speech_started(self, speech_started, **kwargs):
            print(f"\n\n{speech_started}\n\n")

        def on_utterance_end(self, utterance_end, **kwargs):
            print(f"\n\n{utterance_end}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        liveClient.on(LiveTranscriptionEvents.Transcript, on_message)
        liveClient.on(LiveTranscriptionEvents.Metadata, on_metadata)
        liveClient.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        liveClient.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        liveClient.on(LiveTranscriptionEvents.Error, on_error)

        # connect to websocket
        options: LiveOptions = LiveOptions(model="nova-3", language="en-US")

        if liveClient.start(options) is False:
            print("Failed to connect to Deepgram")
            return

        lock_exit = threading.Lock()
        exit = False

        # define a worker thread
        def myThread():
            with httpx.stream("GET", URL) as r:
                for data in r.iter_bytes():
                    lock_exit.acquire()
                    if exit:
                        break
                    lock_exit.release()

                    liveClient.send(data)

        # start the worker thread
        myHttp = threading.Thread(target=myThread)
        myHttp.start()

        # signal finished
        input("Press Enter to stop recording...\n\n")
        lock_exit.acquire()
        exit = True
        lock_exit.release()

        # Wait for the HTTP thread to close and join
        myHttp.join()

        # Indicate that we've finished
        liveClient.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
