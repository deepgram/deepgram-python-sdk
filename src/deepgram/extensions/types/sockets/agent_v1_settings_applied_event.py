# Agent V1 Settings Applied Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1SettingsAppliedEvent(UniversalBaseModel):
    """
    Confirm the server has successfully received and applied the Settings message
    """
    
    type: typing.Literal["SettingsApplied"] = "SettingsApplied"
    """Message type identifier for settings applied confirmation"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow