# Listen V1 Speech Started Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ListenV1SpeechStartedEvent(UniversalBaseModel):
    """
    vad_events is true and speech has been detected
    """
    
    type: typing.Literal["SpeechStarted"]
    """Message type identifier"""
    
    channel: typing.List[int]
    """The channel"""
    
    timestamp: float
    """The timestamp"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
