# Agent V1 Function Call Response Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1FunctionCallResponseMessage(UniversalBaseModel):
    """
    Client-side or server-side function call response sent by the server
    """
    
    type: typing.Literal["FunctionCallResponse"] = "FunctionCallResponse"
    """Message type identifier for function call responses"""
    
    name: str
    """The name of the function being called"""
    
    content: str
    """The content or result of the function call"""
    
    id: typing.Optional[str] = None
    """The unique identifier for the function call (optional but recommended for traceability)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow