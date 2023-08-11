import asyncio
import json
import pytest
import sys

# from .conftest import option
from deepgram import Deepgram
from .mock_response import MOCK_RESPONSE

api_key = pytest.api_key
assert api_key, "Pass Deepgram API key as an argument: `pytest --api-key <key> tests/`"

deepgram = Deepgram(api_key)

MOCK_TRANSCRIPT = "Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while. you could miss it"
AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

def test_transcribe_prerecorded():
    """
    Test basic synchronous pre-recorded transcription.
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
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert actual_transcript == MOCK_TRANSCRIPT

def test_transcribe_prerecorded_find_and_replace_string():
    """
    Test find-and-replace with a string of one term.
    """
    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
            "replace": "fast:slow",
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert actual_transcript == MOCK_TRANSCRIPT.replace("fast", "slow")

def test_transcribe_prerecorded_find_and_replace_list():
    """
    Test find-and-replace with a list of two terms.
    """
    response = deepgram.transcription.sync_prerecorded(
        {
            "url": AUDIO_URL
        },
        {
            "model": "nova",
            "smart_format": True,
            "replace": ["fast:slow", "miss:snooze"],
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert actual_transcript == MOCK_TRANSCRIPT.replace("fast", "slow").replace("miss", "snooze")

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


