# Deprecated compatibility wrapper for pre-7.12 Topics params.

import typing

import typing_extensions
from .shared_topics_results_topics_segments_item import SharedTopicsResultsTopicsSegmentsItemParams


class SharedTopicsResultsTopicsParams(typing_extensions.TypedDict):
    segments: typing_extensions.NotRequired[typing.Sequence[SharedTopicsResultsTopicsSegmentsItemParams]]
