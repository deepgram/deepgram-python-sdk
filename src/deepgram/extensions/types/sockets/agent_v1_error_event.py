# Agent V1 Error Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1ErrorEvent(UniversalBaseModel):
    """
    Receive an error message from the server when an error occurs
    """
    
    type: typing.Literal["Error"]
    """Message type identifier for error responses"""
    
    description: str
    """A description of what went wrong"""
    
    code: str
    """Error code identifying the type of error"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
