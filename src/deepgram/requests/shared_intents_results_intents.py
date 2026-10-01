# Deprecated compatibility wrapper for pre-7.12 Intents params.

import typing

import typing_extensions
from .shared_intents_results_intents_segments_item import SharedIntentsResultsIntentsSegmentsItemParams


class SharedIntentsResultsIntentsParams(typing_extensions.TypedDict):
    segments: typing_extensions.NotRequired[typing.Sequence[SharedIntentsResultsIntentsSegmentsItemParams]]
