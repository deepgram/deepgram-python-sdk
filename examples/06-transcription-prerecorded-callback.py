"""
Example: Transcribe Prerecorded Audio with Callback

This example shows how to transcribe audio asynchronously using a callback URL.
The transcription result will be sent to your callback URL when ready.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Sending transcription request with callback...")
    response = client.listen.v1.media.transcribe_url(
        url="https://dpgr.am/spacewalk.wav",
        callback="https://your-callback-url.com/webhook",
        model="nova-3",
    )
    
    # This returns a "listen accepted" response, not the full transcription
    # The actual transcription will be sent to your callback URL
    print(f"Request accepted. Request ID: {response.request_id}")
    print("Transcription will be sent to your callback URL when ready.")
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.listen.v1.media.transcribe_url(..., callback="...")
    
except Exception as e:
    print(f"Error: {e}")

