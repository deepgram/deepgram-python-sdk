import asyncio
import pytest
import pytest_asyncio  # Required to ensure pytest-asyncio is installed
import os.path
import fuzzywuzzy.fuzz

# from .conftest import option
from deepgram import Deepgram


CURRENT_DIRECTORY = os.path.split(os.path.abspath(__file__))[0]

api_key = pytest.api_key
assert api_key, "Pass Deepgram API key as an argument: `pytest --api-key <key> tests/`"

deepgram = Deepgram(api_key)

MOCK_TRANSCRIPT = "Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while. you could miss it."
AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
TRANSCRIPT_SIMILARITY_THRESHOLD = 98  # The STT is not deterministic, so the transcript can change. Units = percent.


def test_transcribe_prerecorded():
    """
    Test basic synchronous pre-recorded transcription.
    """
    response = deepgram.transcription.sync_prerecorded(
        {"url": AUDIO_URL},
        {
            "model": "nova",
            "smart_format": True,
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert fuzzywuzzy.fuzz.ratio(actual_transcript, MOCK_TRANSCRIPT) > TRANSCRIPT_SIMILARITY_THRESHOLD


def test_transcribe_prerecorded_find_and_replace_string():
    """
    Test find-and-replace with a string of one term.
    """
    response = deepgram.transcription.sync_prerecorded(
        {"url": AUDIO_URL},
        {
            "model": "nova",
            "smart_format": True,
            "replace": "fast:slow",
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert fuzzywuzzy.fuzz.ratio(actual_transcript, MOCK_TRANSCRIPT.replace("fast", "slow")) > TRANSCRIPT_SIMILARITY_THRESHOLD


def test_transcribe_prerecorded_find_and_replace_list():
    """
    Test find-and-replace with a list of two terms.
    """
    response = deepgram.transcription.sync_prerecorded(
        {"url": AUDIO_URL},
        {
            "model": "nova",
            "smart_format": True,
            "replace": ["fast:slow", "miss:snooze"],
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert fuzzywuzzy.fuzz.ratio(actual_transcript, MOCK_TRANSCRIPT.replace("fast", "slow").replace("miss", "snooze")) > TRANSCRIPT_SIMILARITY_THRESHOLD


@pytest.mark.asyncio  # Requires pytest-asyncio to be installed
async def test_transcribe_prerecorded_file():
    """
    Test basic asyncronous pre-recorded transcription.
    """
    example_wav_file = os.path.join(CURRENT_DIRECTORY, "the-missile-short.wav")
    with open(example_wav_file, "rb") as audio:
        response = await deepgram.transcription.prerecorded({"buffer": audio, "mimetype": "audio/wav"})
        assert "results" in response

def test_prerecorded_json_structure():
    """
    Testing the JSON structure of the Deepgram response. This should be consistent across all outputs
    unless there is a breaking change in the API itself.
    """
    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
        },
    )

    # Checks that both results and metadata are present in the base response
    assert set(response.keys()) == set(['results','metadata'])
    
    # Checks that metadata contains the expected keys
    assert set(response['metadata'].keys()) == set(['channels','created','duration','model_info','models','request_id','sha256','transaction_key'])

    # Checks that the results key contains the expected keys
    assert list(response['results'].keys()) == ['channels']

    # Checks that the channels key contains the expected keys
    assert len(response['results']['channels']) == 1

    # Checks if alternatives is present in the channels[0] object
    assert list(response['results']['channels'][0].keys()) == ['alternatives']

    # Checks if alternatives is a list of length 1
    assert len(response['results']['channels'][0]['alternatives']) == 1
    
    # Checks if the alternatives[0] object contains the expected keys
    assert set(response['results']['channels'][0]['alternatives'][0].keys()) == set(['transcript', 'confidence', 'words', 'paragraphs'])

    # Checks if the transcript is a string
    assert type(response['results']['channels'][0]['alternatives'][0]['transcript']) == str

    # Checks if the confidence is a float
    assert type(response['results']['channels'][0]['alternatives'][0]['confidence']) == float

    # Checks if the words is a list
    assert type(response['results']['channels'][0]['alternatives'][0]['words']) == list

    # Checks if the paragraphs is a dict
    assert type(response['results']['channels'][0]['alternatives'][0]['paragraphs']) == dict

    # Checks if the transcript within the paragraphs object is a string
    assert type(response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']) == str

    # Checks if the paragraphs within the paragraphs object is a list
    assert type(response['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs']) == list

    # Checks if the paragraphs[0] object contains the expected keys
    assert set(response['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs'][0]) == set(['sentences', 'num_words', 'start', 'end'])

def test_diarization():

    """
    Testing the diarization output of the Deepgram response.
    
    """

    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
            "diarize": True
        },
    )

    # Checks if the speakers key is present in the alternatives[0] object
    assert set(response['results']['channels'][0]['alternatives'][0]['paragraphs']['paragraphs'][0].keys()) == set(['sentences','speaker', 'num_words', 'start', 'end'])

def test_summarize():
    """
    Checking the summarize output of the Deepgram response, especially for summarize v2.
    """
    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
            "summarize": 'v2'
        },
    )
    
    # Checks if the summary object has the expected keys
    assert set(response['results']['summary'].keys()) == set(['result', 'short'])
    # Check if the result is a string
    assert type(response['results']['summary']['result']) == str
    # Check if the short is a string
    assert type(response['results']['summary']['short']) == str

def test_topic_detection():
    """
    Checking the topic detection output of the Deepgram response.
    """
    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
            "detect_topics": True
        },
    )

    # Checks if the topics key is present in the alternatives[0] object
    assert type(response['results']['channels'][0]['alternatives'][0]['topics']) == list

    # Checks if the topics[0] object is a dict
    assert type(response['results']['channels'][0]['alternatives'][0]['topics'][0]) == dict

    # Checks if the topics[0] object contains the expected keys
    assert set(response['results']['channels'][0]['alternatives'][0]['topics'][0].keys()) == set(['text', 'start_word', 'end_word', 'topics'])

    # Checks if the topics object is a list
    assert type(response['results']['channels'][0]['alternatives'][0]['topics'][0]['topics']) == list

