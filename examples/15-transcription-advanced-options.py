"""
Example: Transcription with Advanced Options

This example shows how to use advanced transcription options like
smart formatting, punctuation, diarization, and more.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    print("Transcribing with advanced options...")
    response = client.listen.v1.media.transcribe_url(
        url="https://dpgr.am/spacewalk.wav",
        model="nova-3",
        language="multi",
        # Requires Nova-3 multilingual language hints, which are rolling out server-side.
        language_hint=["en"],
        # Advanced options
        smart_format=True,
        punctuate=True,
        diarize=True,
        # Additional options
        # paragraphs=True,
        # utterances=True,
        # detect_language=True,
        # keywords=["important", "keyword"],
        # search=["search term"],
    )

    print("Transcription received:")
    if response.results and response.results.channels:
        channel = response.results.channels[0]
        if channel.alternatives:
            alternative = channel.alternatives[0]
            transcript = alternative.transcript
            print(f"Transcript: {transcript}")

            if alternative.languages is not None:
                print(f"Detected languages: {', '.join(alternative.languages)}")
            if alternative.languages_hinted is not None:
                print(f"Applied language hints: {', '.join(alternative.languages_hinted)}")

            # Show speaker diarization if available
            if alternative.words:
                print("\nSpeaker diarization:")
                for word in alternative.words:
                    speaker = getattr(word, "speaker", None)
                    language = getattr(word, "language", None)
                    if speaker is not None:
                        language_label = f" ({language})" if language is not None else ""
                        print(f"  Speaker {speaker}{language_label}: {word.word}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # response = await client.listen.v1.media.transcribe_url(...)

    # With additional query parameters:
    # response = client.listen.v1.media.transcribe_url(
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
