# Agent V1 Update Speak Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel

# Import the complete speak provider types from settings message
from .agent_v1_settings_message import (
    AgentV1SpeakProviderConfig,
)


class AgentV1UpdateSpeakMessage(UniversalBaseModel):
    """
    Send a message to change the Speak model in the middle of a conversation
    """
    
    type: typing.Literal["UpdateSpeak"] = "UpdateSpeak"
    """Message type identifier for updating the speak model"""
    
    speak: AgentV1SpeakProviderConfig
    """Configuration for the speak model with proper nested types"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow