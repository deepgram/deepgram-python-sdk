# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    UrlSource,
)

load_dotenv()

AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key
        print("Step 1: Creating client with API key...")
        config = DeepgramClientOptions(verbose=verboselogs.INFO)
        api_client = DeepgramClient(api_key=os.getenv("DG_API_KEY", ""), config=config)
        print(
            f"API client created with auth: {api_client._config.headers.get('Authorization', 'Not set')}"
        )

        # STEP 2 Use the API key client to get an access token with custom TTL
        print("\nStep 2: Getting access token with custom TTL (600 seconds)...")
        response = api_client.auth.v("1").grant_token(ttl_seconds=600)
        access_token = response.access_token
        print(f"Access token received: {access_token[:20]}...{access_token[-10:]}")
        print(f"Token expires in: {response.expires_in} seconds")

        # STEP 3 Create a new client using the access token (Bearer auth)
        print("\nStep 3: Creating client with Bearer token...")
        bearer_client = DeepgramClient(access_token=access_token)
        bearer_auth_header = bearer_client._config.headers.get(
            "Authorization", "Not set"
        )
        print(f"Bearer client created with auth: {bearer_auth_header[:30]}...")

        # STEP 4 Use the Bearer token client to transcribe audio
        print("\nStep 4: Transcribing audio with Bearer token...")
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        transcription_response = bearer_client.listen.rest.v("1").transcribe_url(
            AUDIO_URL, options
        )
        transcript = (
            transcription_response.results.channels[0].alternatives[0].transcript
        )

        print(f"Transcription successful!")
        print(f"Transcript: {transcript}")
        print(
            f"\n✅ Complete workflow successful: API Key → Access Token → Bearer Auth → Transcription"
        )

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
