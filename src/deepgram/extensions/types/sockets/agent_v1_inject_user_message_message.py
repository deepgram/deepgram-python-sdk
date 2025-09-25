# Agent V1 Inject User Message Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1InjectUserMessageMessage(UniversalBaseModel):
    """
    Send a text based message to the agent
    """
    
    type: typing.Literal["InjectUserMessage"] = "InjectUserMessage"
    """Message type identifier for injecting a user message"""
    
    content: str
    """The specific phrase or statement the agent should respond to"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow