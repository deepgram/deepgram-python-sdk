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
        # Nova-3 multilingual: language_hint biases detection toward the languages
        # you expect. It does not restrict the transcript to them, and it applies
        # only with language="multi". For a single known language, use e.g.
        # language="en-US" and omit language_hint.
        language="multi",
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
            transcript = channel.alternatives[0].transcript
            print(f"Transcript: {transcript}")

            # Only present with language="multi"; languages can be absent on
            # audio that switches languages.
            if channel.alternatives[0].languages is not None:
                print(f"Detected languages: {', '.join(channel.alternatives[0].languages)}")
            # Nova-3 multilingual returns [] when no language hint was sent.
            if channel.alternatives[0].languages_hinted is not None:
                print(f"Language hints used: {', '.join(channel.alternatives[0].languages_hinted)}")

            # Show speaker diarization if available
            if channel.alternatives[0].words:
                print("\nSpeaker diarization:")
                for word in channel.alternatives[0].words:
                    speaker = getattr(word, "speaker", None)
                    if speaker is not None:
                        print(f"  Speaker {speaker}: {word.word}")

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
