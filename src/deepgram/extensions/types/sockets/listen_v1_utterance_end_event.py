# Listen V1 Utterance End Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ListenV1UtteranceEndEvent(UniversalBaseModel):
    """
    An utterance has ended
    """
    
    type: typing.Literal["UtteranceEnd"]
    """Message type identifier"""
    
    channel: typing.List[int]
    """The channel"""
    
    last_word_end: float
    """The last word end"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
