# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

load_dotenv()

options = LiveOptions(
    model="nova",
    interim_results=False,
    language="en-US",
)

# URL for the realtime streaming audio you would like to transcribe
URL = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"


async def main():
    deepgram = DeepgramClient()

    # Create a websocket connection to Deepgram
    try:
        dg_connection = deepgram.listen.asynclive.v("1")

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
