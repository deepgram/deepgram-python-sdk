# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from signal import SIGINT, SIGTERM
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"


async def main():
    # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
    # config: DeepgramClientOptions = DeepgramClientOptions(
    #     verbose=logging.DEBUG,
    #     options={"keepalive": "true"}
    # )
    # deepgram: DeepgramClient = DeepgramClient(API_KEY, config)
    # otherwise, use default config
    deepgram: DeepgramClient = DeepgramClient(API_KEY)

    # Create a websocket connection to Deepgram
    try:
        loop = asyncio.get_event_loop()

        for signal in (SIGTERM, SIGINT):
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(shutdown(signal, loop, dg_connection)),
            )

        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"speaker: {sentence}")

        async def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        async def on_speech_started(self, speech_started, **kwargs):
            print(f"\n\n{speech_started}\n\n")

        async def on_utterance_end(self, utterance_end, **kwargs):
            print(f"\n\n{utterance_end}\n\n")

        async def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        async def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)

        # connect to websocket
        options: LiveOptions = LiveOptions(
            model="nova-2",
            language="en-US",
        )

        await dg_connection.start(options)

        # Send streaming audio from the URL to Deepgram and  wait until cancelled
        print("Press Ctrl+C to stop...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL) as audio:
                    while True:
                        data = await audio.content.readany()
                        # send audio data through the socket
                        await dg_connection.send(data)
                        # If no data is being sent from the live stream, then break out of the loop.
                        if not data:
                            break
        except asyncio.CancelledError:
            # This block will be executed when the shutdown coroutine cancels all tasks
            pass
        finally:
            await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


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
