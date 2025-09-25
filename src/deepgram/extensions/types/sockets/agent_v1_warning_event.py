# Agent V1 Warning Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1WarningEvent(UniversalBaseModel):
    """
    Notifies the client of non-fatal errors or warnings
    """
    
    type: typing.Literal["Warning"] = "Warning"
    """Message type identifier for warnings"""
    
    description: str
    """Description of the warning"""
    
    code: str
    """Warning code identifier"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow