# Agent V1 Agent Started Speaking Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1AgentStartedSpeakingEvent(UniversalBaseModel):
    """
    Get notified when the server begins streaming an agent's audio response for playback. 
    This message is only sent when the experimental flag is enabled
    """
    
    type: typing.Literal["AgentStartedSpeaking"] = "AgentStartedSpeaking"
    """Message type identifier for agent started speaking"""
    
    total_latency: float
    """Seconds from receiving the user's utterance to producing the agent's reply"""
    
    tts_latency: float
    """The portion of total latency attributable to text-to-speech"""
    
    ttt_latency: float
    """The portion of total latency attributable to text-to-text (usually an LLM)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow