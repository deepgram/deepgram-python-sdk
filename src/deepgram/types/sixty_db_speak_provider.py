# Mirrors ElevenLabsSpeakProvider in shape so 60db can be wired into the same
# SpeakSettings discriminated union pattern that the Agent/VoiceAgent surfaces
# use. type="sixty_db" is the union discriminant.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel
from .sixty_db_speak_provider_voice_id import SixtyDbSpeakProviderVoiceId


class SixtyDbSpeakProvider(UncheckedBaseModel):
    type: typing.Literal["sixty_db"] = "sixty_db"
    voice_id: SixtyDbSpeakProviderVoiceId = pydantic.Field()
    """
    60db voice ID. See https://docs.60db.ai for the catalog.
    """

    speed: typing.Optional[float] = pydantic.Field(default=None)
    """
    Playback speed multiplier. Range 0.5 - 2.0.
    """

    stability: typing.Optional[float] = pydantic.Field(default=None)
    """
    Voice stability. 0-100. Lower = expressive, higher = consistent.
    """

    similarity: typing.Optional[float] = pydantic.Field(default=None)
    """
    Similarity to source voice. 0-100.
    """

    language: typing.Optional[str] = pydantic.Field(default=None)
    """
    Optional language hint. 60db auto-detects from supported languages
    (en, hi, bn, gu, kn, ml, mr, pa, ta, te).
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
