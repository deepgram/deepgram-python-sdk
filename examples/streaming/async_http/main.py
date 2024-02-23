# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

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
    # config = DeepgramClientOptions(
    #     verbose=logging.DEBUG,
    #     options={"keepalive": "true"}
    # )
    # deepgram: DeepgramClient = DeepgramClient(API_KEY, config)
    # otherwise, use default config
    deepgram = DeepgramClient(API_KEY)

    # Create a websocket connection to Deepgram
    try:
        dg_connection = deepgram.listen.asynclive.v("1")

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

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        # connect to websocket
        options = LiveOptions(
            model="nova-2",
            language="en-US",
        )

        await dg_connection.start(options)

        # Send streaming audio from the URL to Deepgram
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as audio:
                while True:
                    data = await audio.content.readany()
                    # send audio data through the socket
                    await dg_connection.send(data)
                    # If no data is being sent from the live stream, then break out of the loop.
                    if not data:
                        break

        # Indicate that we've finished sending data by sending the {"type": "CloseStream"}
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


asyncio.run(main())
