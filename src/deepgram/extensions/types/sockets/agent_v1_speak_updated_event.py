# Agent V1 Speak Updated Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1SpeakUpdatedEvent(UniversalBaseModel):
    """
    Confirms that an UpdateSpeak message from the client has been applied
    """
    
    type: typing.Literal["SpeakUpdated"] = "SpeakUpdated"
    """Message type identifier for speak update confirmation"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow