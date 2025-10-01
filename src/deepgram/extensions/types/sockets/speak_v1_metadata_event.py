# Speak V1 Metadata Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class SpeakV1MetadataEvent(UniversalBaseModel):
    """
    Metadata sent after the WebSocket handshake
    """
    
    type: typing.Literal["Metadata"]
    """Message type identifier"""
    
    request_id: str
    """Unique identifier for the request"""
    
    model_name: str
    """Name of the model being used"""
    
    model_version: str
    """Version of the model being used"""
    
    model_uuid: str
    """Unique identifier for the model"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
