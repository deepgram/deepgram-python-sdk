# Agent V1 User Started Speaking Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1UserStartedSpeakingEvent(UniversalBaseModel):
    """
    Notify the client that the user has begun speaking
    """
    
    type: typing.Literal["UserStartedSpeaking"] = "UserStartedSpeaking"
    """Message type identifier indicating that the user has begun speaking"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow