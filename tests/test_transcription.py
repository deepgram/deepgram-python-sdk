import asyncio
import json
import pytest
import sys
import os.path

# from .conftest import option
from deepgram import Deepgram
from .mock_response import MOCK_RESPONSE


CURRENT_DIRECTORY = os.path.split(os.path.abspath(__file__))[0]

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
        {"url": AUDIO_URL},
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
        {"url": AUDIO_URL},
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
        {"url": AUDIO_URL},
        {
            "model": "nova",
            "smart_format": True,
            "replace": ["fast:slow", "miss:snooze"],
        },
    )
    actual_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    assert actual_transcript == MOCK_TRANSCRIPT.replace("fast", "slow").replace("miss", "snooze")


@pytest.mark.asyncio
async def test_transcribe_prerecorded_file():
    """
    Test basic asyncronous pre-recorded transcription.
    """
    example_wav_file = os.path.join(CURRENT_DIRECTORY, "the-missle-short.wav")
    with open(example_wav_file, "rb") as audio:
        response = await deepgram.transcription.prerecorded({"buffer": audio, "mimetype": "audio/wav"})()
        assert "results" in response
