# Agent V1 Injection Refused Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1InjectionRefusedEvent(UniversalBaseModel):
    """
    Receive injection refused message
    """
    
    type: typing.Literal["InjectionRefused"] = "InjectionRefused"
    """Message type identifier for injection refused"""
    
    message: str
    """Details about why the injection was refused"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow