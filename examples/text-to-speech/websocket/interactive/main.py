# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dotenv import load_dotenv
import threading
from websockets.exceptions import ConnectionClosedError
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    SpeakWebSocketEvents,
    SpeakOptions,
)

load_dotenv()


TTS_TEXT = "Hello, this is a text to speech example using Deepgram."
AUDIO_FILE = "output.mp3"


def main():
    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        config: DeepgramClientOptions = DeepgramClientOptions(verbose=verboselogs.DEBUG)
        deepgram: DeepgramClient = DeepgramClient("", config)
        # otherwise, use default config
        # deepgram: DeepgramClient = DeepgramClient()

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.speak.websocket.v("1")
        # print(dg_connection)

        def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")
            thread = threading.Thread(target=send_tts_text, args=(self,))
            thread.start()
            thread.join()

        def on_binary_data(self, data, **kwargs):
            print("Received binary data:")
            with open(AUDIO_FILE, "ab") as f:
                f.write(data)

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_flush(self, flush, **kwargs):
            print(f"\n\n{flush}\n\n")

        def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        def on_warning(self, warning, **kwargs):
            print(f"\n\n{warning}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"\n\n{unhandled}\n\n")

        dg_connection.on(SpeakWebSocketEvents.Open, on_open)
        dg_connection.on(SpeakWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(SpeakWebSocketEvents.Metadata, on_metadata)
        dg_connection.on(SpeakWebSocketEvents.Flush, on_flush)
        dg_connection.on(SpeakWebSocketEvents.Close, on_close)
        dg_connection.on(SpeakWebSocketEvents.Error, on_error)
        dg_connection.on(SpeakWebSocketEvents.Warning, on_warning)
        dg_connection.on(SpeakWebSocketEvents.Unhandled, on_unhandled)

        lock = threading.Lock()

        def send_tts_text(dg_connection):
            with lock:
                dg_connection.send(TTS_TEXT)

        # connect to websocket
        options = SpeakOptions(model="aura-asteria-en")

        print("\n\nPress Enter to stop...\n\n")
        if dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        # Indicate that we've finished
        input("\n\nPress Enter to stop...\n\n")
        dg_connection.finish()

        print("Finished")

    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except ValueError as e:
        print(f"Invalid value encountered: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
