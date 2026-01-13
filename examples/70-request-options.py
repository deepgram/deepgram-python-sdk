"""
Example: Request Options - Additional Query Parameters

This example shows how to use request_options to add additional query parameters
to API requests, such as detect_language for language detection.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Transcribing with additional query parameters...")
    response = client.listen.v1.media.transcribe_url(
        url="https://dpgr.am/spacewalk.wav",
        model="nova-3",
        request_options={
            "additional_query_parameters": {
                "detect_language": ["en", "es"],
            }
        },
    )

    print("Transcription received:")
    if response.results and response.results.channels:
        transcript = response.results.channels[0].alternatives[0].transcript
        print(f"Transcript: {transcript}")

    # Additional query parameters can be used for various purposes:
    # - Language detection: "detect_language": ["en", "es"]
    # - Custom parameters: Add any query parameters needed for your use case

    # You can also combine with other request options:
    # response = client.listen.v1.media.transcribe_url(
    #     url="https://dpgr.am/spacewalk.wav",
    #     model="nova-3",
    #     request_options={
    #         "additional_query_parameters": {
    #             "detect_language": ["en", "es"],
    #         },
    #         "additional_headers": {
    #             "X-Custom-Header": "custom-value",
    #         },
    #         "timeout_in_seconds": 30,
    #         "max_retries": 3,
    #     }
    # )

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.listen.v1.media.transcribe_url(
    #     url="https://dpgr.am/spacewalk.wav",
    #     model="nova-3",
    #     request_options={
    #         "additional_query_parameters": {
    #             "detect_language": ["en", "es"],
    #         }
    #     }
    # )

except Exception as e:
    print(f"Error: {e}")
