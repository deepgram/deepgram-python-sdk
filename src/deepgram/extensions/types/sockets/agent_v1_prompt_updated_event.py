# Agent V1 Prompt Updated Event - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AgentV1PromptUpdatedEvent(UniversalBaseModel):
    """
    Confirms that an UpdatePrompt message from the client has been applied
    """
    
    type: typing.Literal["PromptUpdated"] = "PromptUpdated"
    """Message type identifier for prompt update confirmation"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow