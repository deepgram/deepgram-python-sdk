"""
Example: Error Handling

This example shows how to handle errors when using the Deepgram SDK.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.errors.bad_request_error import BadRequestError

client = DeepgramClient()

try:
    # Example 1: Handling API errors
    print("Example 1: Handling API errors")
    try:
        response = client.listen.v1.media.transcribe_url(
            url="https://invalid-url.example.com/audio.wav",
            model="nova-3",
        )
    except ApiError as e:
        print("API Error occurred:")
        print(f"  Status code: {e.status_code}")
        print(f"  Body: {e.body}")
        print(f"  Headers: {e.headers}")

    # Example 2: Handling specific error types
    print("\nExample 2: Handling BadRequestError")
    try:
        # This might fail with a bad request error
        response = client.listen.v1.media.transcribe_url(
            url="",  # Invalid empty URL
            model="nova-3",
        )
    except BadRequestError as e:
        print("Bad Request Error:")
        print(f"  Status code: {e.status_code}")
        print(f"  Body: {e.body}")
    except ApiError as e:
        print(f"Other API Error: {e.status_code}")

    # Example 3: Handling network errors
    print("\nExample 3: Handling network errors")
    try:
        response = client.listen.v1.media.transcribe_url(
            url="https://dpgr.am/spacewalk.wav",
            model="nova-3",
        )
        print("Request successful!")
    except Exception as e:
        # Catch-all for network errors, timeouts, etc.
        print(f"Error occurred: {type(e).__name__}: {e}")

    # Example 4: Using try-except with WebSocket connections
    print("\nExample 4: Error handling with WebSocket")
    try:
        from deepgram.core.events import EventType

        with client.listen.v1.connect(model="nova-3") as connection:

            def on_error(error):
                print(f"WebSocket error: {error}")

            connection.on(EventType.ERROR, on_error)
            # Connection will handle errors automatically
            connection.start_listening()
    except Exception as e:
        print(f"Connection error: {e}")

    # Best practices:
    # 1. Always wrap API calls in try-except blocks
    # 2. Check for specific error types (ApiError, BadRequestError)
    # 3. Log error details for debugging
    # 4. Handle errors gracefully in production code

except Exception as e:
    print(f"Unexpected error: {e}")
