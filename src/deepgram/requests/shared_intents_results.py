# Deprecated compatibility wrapper for pre-7.12 Intents params.

import typing_extensions
from .shared_intents_results_intents import SharedIntentsResultsIntentsParams


class SharedIntentsResultsParams(typing_extensions.TypedDict):
    intents: typing_extensions.NotRequired[SharedIntentsResultsIntentsParams]
