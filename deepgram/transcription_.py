import asyncio

from .transcription import Transcription
from ._types import TranscriptionSource, PrerecordedOptions, PrerecordedTranscriptionResponse


class Transcription(Transcription):
    def prerecorded(
        self, source: TranscriptionSource, 
        options: PrerecordedOptions = None, **kwargs
        ) -> PrerecordedTranscriptionResponse:

        """Synchronously retrieves a transcription for an already-existing audio file,
        local or web-hosted"""

        return asyncio.run(super().prerecorded(source, options, **kwargs))