# Agent V1 Update Prompt Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1UpdatePromptMessage(UniversalBaseModel):
    """
    Send a message to update the system prompt of the agent
    """
    
    type: typing.Literal["UpdatePrompt"] = "UpdatePrompt"
    """Message type identifier for prompt update request"""
    
    prompt: str
    """The new system prompt to be used by the agent"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow