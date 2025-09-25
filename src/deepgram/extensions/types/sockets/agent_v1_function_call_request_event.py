# Agent V1 Function Call Request Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1FunctionCallRequestFunction(UniversalBaseModel):
    """Function call request details"""
    
    id: str
    """Unique identifier for the function call"""
    
    name: str
    """The name of the function to call"""
    
    arguments: str
    """JSON string containing the function arguments"""
    
    client_side: bool
    """Whether the function should be executed client-side"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1FunctionCallRequestEvent(UniversalBaseModel):
    """
    Client-side or server-side function call request sent by the server
    """
    
    type: typing.Literal["FunctionCallRequest"] = "FunctionCallRequest"
    """Message type identifier for function call requests"""
    
    functions: typing.List[AgentV1FunctionCallRequestFunction]
    """Array of functions to be called"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow