# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import os
from dotenv import load_dotenv
import threading

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"


def main():
    try:
        deepgram = DeepgramClient()

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
            print(f"\n{metadata}\n")

        def on_error(error=None):
            if error is None:
                return
            print(f"\n{error}\n")

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            if result is None:
                return
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

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

        # connect to websocket
        options = LiveOptions(model="nova", interim_results=False, language="en-US")
        dg_connection.start(options)

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

                    dg_connection.send(data)

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
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()
