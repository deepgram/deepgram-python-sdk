"""
Example: Transcribe Prerecorded Audio with Callback

This example shows how to transcribe audio asynchronously using a callback URL.
The transcription result will be sent to your callback URL when ready.

Set DEEPGRAM_CALLBACK_URL to a publicly reachable URL before running this
example. The service must be able to resolve and reach the callback host.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient


def main() -> int:
    callback_url = os.getenv("DEEPGRAM_CALLBACK_URL")
    if not callback_url:
        print("Set DEEPGRAM_CALLBACK_URL to a publicly reachable callback URL.", file=sys.stderr)
        return 2

    client = DeepgramClient()
    print("Sending transcription request with callback...")
    try:
        response = client.listen.v1.media.transcribe_url(
            url="https://dpgr.am/spacewalk.wav",
            callback=callback_url,
            model="nova-3",
        )
    except Exception as exc:
        print(f"Callback transcription failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    # This returns a "listen accepted" response, not the full transcription
    # The actual transcription will be sent to your callback URL
    print(f"Request accepted. Request ID: {response.request_id}")
    print(f"Transcription will be sent to {callback_url} when ready.")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.listen.v1.media.transcribe_url(..., callback="...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
