# Deprecated compatibility wrapper for the pre-7.12 Intents response shape.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .shared_intents_results_intents_segments_item import SharedIntentsResultsIntentsSegmentsItem


class SharedIntentsResultsIntents(UncheckedBaseModel):
    segments: typing.Optional[typing.List[SharedIntentsResultsIntentsSegmentsItem]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
