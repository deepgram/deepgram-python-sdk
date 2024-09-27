# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from signal import SIGINT, SIGTERM
import asyncio
import time
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    SpeakWebSocketEvents,
    SpeakWSOptions,
)

TTS_TEXT = "Hello, this is a text to speech example using Deepgram."

global warning_notice
warning_notice = True


async def main():
    try:
        loop = asyncio.get_event_loop()

        for signal in (SIGTERM, SIGINT):
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(shutdown(signal, loop, dg_connection)),
            )

        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        config: DeepgramClientOptions = DeepgramClientOptions(
            options={"auto_flush_speak_delta": "500", "speaker_playback": "true"},
            # verbose=verboselogs.SPAM,
        )
        deepgram: DeepgramClient = DeepgramClient("", config)

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.speak.asyncwebsocket.v("1")

        async def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        async def on_binary_data(self, data, **kwargs):
            global warning_notice
            if warning_notice:
                print("Received binary data")
                print("You can do something with the binary data here")
                print("OR")
                print(
                    "If you want to simply play the audio, set speaker_playback to true in the options for DeepgramClientOptions"
                )
                warning_notice = False

        async def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        async def on_flush(self, flushed, **kwargs):
            print(f"\n\n{flushed}\n\n")

        async def on_clear(self, clear, **kwargs):
            print(f"\n\n{clear}\n\n")

        async def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        async def on_warning(self, warning, **kwargs):
            print(f"\n\n{warning}\n\n")

        async def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        async def on_unhandled(self, unhandled, **kwargs):
            print(f"\n\n{unhandled}\n\n")

        dg_connection.on(SpeakWebSocketEvents.Open, on_open)
        dg_connection.on(SpeakWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(SpeakWebSocketEvents.Metadata, on_metadata)
        dg_connection.on(SpeakWebSocketEvents.Flushed, on_flush)
        dg_connection.on(SpeakWebSocketEvents.Cleared, on_clear)
        dg_connection.on(SpeakWebSocketEvents.Close, on_close)
        dg_connection.on(SpeakWebSocketEvents.Error, on_error)
        dg_connection.on(SpeakWebSocketEvents.Warning, on_warning)
        dg_connection.on(SpeakWebSocketEvents.Unhandled, on_unhandled)

        # connect to websocket
        options = SpeakWSOptions(
            model="aura-asteria-en",
            encoding="linear16",
            sample_rate=16000,
        )

        print("\n\nPress Enter to stop...\n\n")
        if await dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        # send the text to Deepgram
        await dg_connection.send_text(TTS_TEXT)
        # if auto_flush_speak_delta is not used, you must flush the connection by calling flush()
        await dg_connection.flush()

        # Indicate that we've finished
        await asyncio.sleep(7)

        # Close the connection
        await dg_connection.finish()

        print("Finished")

    except ValueError as e:
        print(f"Invalid value encountered: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def shutdown(signal, loop, dg_connection):
    print(f"Received exit signal {signal.name}...")
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")


asyncio.run(main())
