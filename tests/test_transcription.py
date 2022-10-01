import os
import pytest

from deepgram._types import (Options, PrerecordedOptions)
from deepgram.transcription import *


@pytest.fixture
def example_wav_url() -> str:
    return os.environ.get('DEEPGRAM_PRERECORDED_URL', None)


@pytest.fixture
def example_wav_file() -> str:
    return os.environ.get('DEEPGRAM_PRERECORDED_WAV', None)


@pytest.fixture
def options() -> Options:
    return {
        'api_key': os.environ.get('DEEPGRAM_API_KEY', None),
    }


class TestPrerecordedTranscription:
    @pytest.fixture(autouse=True)
    def set_instance(self, options: Options) -> PrerecordedTranscription:
        self.instance = PrerecordedTranscription(options, None)

    
    @pytest.mark.asyncio
    async def test_transcribe_prerecorded_url(self, example_wav_url):
        source = PrerecordedOptions({'url': example_wav_url})
        response = await self.instance(source)
        assert 'results' in response


    @pytest.mark.asyncio
    async def test_transcribe_prerecorded_file(self, example_wav_file):
        with open(example_wav_file, 'rb') as audio:
            source = PrerecordedOptions(
                {'buffer': audio, 'mimetype': 'audio/wav'}
            )
            response = await self.instance(source)
            assert 'results' in response


class TestTranscription:
    @pytest.fixture(autouse=True)
    def set_instance(self, options: Options) -> Transcription:
        self.instance = Transcription(options)


    @pytest.mark.asyncio
    async def test_prerecorded(self, example_wav_url):
        source = PrerecordedOptions({'url': example_wav_url})
        response = await self.instance.prerecorded(source)
        assert 'results' in response
