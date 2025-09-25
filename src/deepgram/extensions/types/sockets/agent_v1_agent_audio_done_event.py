# Agent V1 Agent Audio Done Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1AgentAudioDoneEvent(UniversalBaseModel):
    """
    Get signals that the server has finished sending the final audio segment to the client
    """
    
    type: typing.Literal["AgentAudioDone"] = "AgentAudioDone"
    """Message type identifier indicating the agent has finished sending audio"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow