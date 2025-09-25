# Listen V1 Metadata Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ListenV1MetadataEvent(UniversalBaseModel):
    """
    Metadata event - these are usually information describing the connection
    """
    
    type: typing.Literal["Metadata"]
    """Message type identifier"""
    
    transaction_key: typing.Optional[str] = None
    """The transaction key (deprecated)"""
    
    request_id: str
    """The request ID"""
    
    sha256: str
    """The sha256"""
    
    created: str
    """The created timestamp"""
    
    duration: float
    """The duration"""
    
    channels: float
    """The channels"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
