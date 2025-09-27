# Agent V1 Inject Agent Message Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1InjectAgentMessageMessage(UniversalBaseModel):
    """
    Immediately trigger an agent response during a conversation
    """
    
    type: typing.Literal["InjectAgentMessage"] = "InjectAgentMessage"
    """Message type identifier for injecting an agent message"""
    
    message: str
    """The statement that the agent should say"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow