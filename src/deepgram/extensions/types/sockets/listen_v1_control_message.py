# Listen V1 Control Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class ListenV1ControlMessage(UniversalBaseModel):
    """
    Control messages for managing the Speech to Text WebSocket connection
    """
    
    type: typing.Literal["Finalize", "CloseStream", "KeepAlive"]
    """Message type identifier"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
