# Deprecated compatibility wrapper for pre-7.12 Topics params.

import typing_extensions
from .shared_topics_results_topics import SharedTopicsResultsTopicsParams


class SharedTopicsResultsParams(typing_extensions.TypedDict):
    topics: typing_extensions.NotRequired[SharedTopicsResultsTopicsParams]
