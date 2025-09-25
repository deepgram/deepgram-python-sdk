# Agent V1 Conversation Text Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1ConversationTextEvent(UniversalBaseModel):
    """
    Facilitate real-time communication by relaying spoken statements from both the user and the assistant
    """
    
    type: typing.Literal["ConversationText"] = "ConversationText"
    """Message type identifier for conversation text"""
    
    role: typing.Literal["user", "assistant"]
    """Identifies who spoke the statement"""
    
    content: str
    """The actual statement that was spoken"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow