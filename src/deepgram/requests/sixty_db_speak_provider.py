# TypedDict mirror of SixtyDbSpeakProvider for use anywhere a SpeakSettings
# provider config is passed as a dict-style argument.

import typing

import typing_extensions
from ..types.sixty_db_speak_provider_voice_id import SixtyDbSpeakProviderVoiceId


class SixtyDbSpeakProviderParams(typing_extensions.TypedDict):
    type: typing.Literal["sixty_db"]
    voice_id: SixtyDbSpeakProviderVoiceId
    speed: typing_extensions.NotRequired[float]
    stability: typing_extensions.NotRequired[float]
    similarity: typing_extensions.NotRequired[float]
    language: typing_extensions.NotRequired[str]
