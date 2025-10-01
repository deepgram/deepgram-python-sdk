# Agent V1 Welcome Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1WelcomeMessage(UniversalBaseModel):
    """
    Confirms that the WebSocket connection has been successfully opened
    """
    
    type: typing.Literal["Welcome"]
    """Message type identifier"""
    
    request_id: str
    """Unique identifier for the request"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
