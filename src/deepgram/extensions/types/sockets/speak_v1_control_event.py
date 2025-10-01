# Speak V1 Control Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class SpeakV1ControlEvent(UniversalBaseModel):
    """
    Control event responses (Flushed, Cleared)
    """
    
    type: typing.Literal["Flushed", "Cleared"]
    """Message type identifier"""
    
    sequence_id: int
    """The sequence ID of the response"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
