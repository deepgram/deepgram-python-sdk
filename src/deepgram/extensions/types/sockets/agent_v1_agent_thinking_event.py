# Agent V1 Agent Thinking Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1AgentThinkingEvent(UniversalBaseModel):
    """
    Inform the client when the agent is processing information
    """
    
    type: typing.Literal["AgentThinking"] = "AgentThinking"
    """Message type identifier for agent thinking"""
    
    content: str
    """The text of the agent's thought process"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow