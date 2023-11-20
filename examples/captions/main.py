# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
import json
from dotenv import load_dotenv
from deepgram_captions import DeepgramConverter, webvtt, srt

from deepgram import DeepgramClient, PrerecordedOptions

load_dotenv()

API_KEY = os.getenv('DG_API_KEY')
AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"}

options: PrerecordedOptions = {
    "model": "nova",
    "smart_format": "true",
    "summarize": "v2",
}

deepgram = DeepgramClient(API_KEY)


async def transcribe_url():
    url_response = await deepgram.listen.prerecorded.transcribe_url(AUDIO_URL, options)
    return url_response


async def main():
    try:
        # STEP 1: Transcribe audio using Deepgram
        response = await transcribe_url()

        # STEP 2: Convert Deepgram response to captions using deepgram_captions library
        transcription = DeepgramConverter(json.loads(response))

        # STEP 3: Generate captions in WebVTT format
        captions_webvtt = webvtt(transcription)
        print("WebVTT Captions:")
        print(captions_webvtt)

        # STEP 4: Generate captions in SRT format
        captions_srt = srt(transcription)
        print("\nSRT Captions:")
        print(captions_srt)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
