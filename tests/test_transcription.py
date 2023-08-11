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
