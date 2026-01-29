# Speak V1 Warning Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class SpeakV1WarningEvent(UniversalBaseModel):
    """
    Warning event from the TTS WebSocket
    """
    
    type: typing.Literal["Warning"]
    """Message type identifier"""

    warn_msg: str
    """A description of what went wrong"""

    warn_code: str
    """Warning code identifying the type of warning"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
