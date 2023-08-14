import asyncio
import pytest
import pytest_asyncio  # Required to ensure pytest-asyncio is installed
import os.path
import fuzzywuzzy.fuzz

# from .conftest import option
from deepgram import Deepgram


CURRENT_DIRECTORY = os.path.split(os.path.abspath(__file__))[0]
from deepgram import Deepgram, DeepgramApiError, DeepgramSetupError

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

def test_missing_api_key():
    with pytest.raises(DeepgramSetupError):
        Deepgram({})

def test_400_error():
    with pytest.raises(DeepgramApiError):
        deepgram.transcription.sync_prerecorded({"url": AUDIO_URL}, {"model": "nova", "language": "ta"})
