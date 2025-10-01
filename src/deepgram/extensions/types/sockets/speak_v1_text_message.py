# Speak V1 Text Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class SpeakV1TextMessage(UniversalBaseModel):
    """
    Request to convert text to speech
    """
    
    type: typing.Literal["Speak"]
    """Message type identifier"""
    
    text: str
    """The input text to be converted to speech"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
