# Client -> server create_context WS message. Must be the first message
# sent after connection_established.

import typing_extensions
from .sixty_db_ws_audio_config import SixtyDbWsAudioConfigParams


class SixtyDbWsCreateContextParams(typing_extensions.TypedDict):
    context_id: typing_extensions.NotRequired[str]
    """
    Optional. Auto-generated UUID if omitted.
    """

    voice_id: str
    audio_config: typing_extensions.NotRequired[SixtyDbWsAudioConfigParams]
    speed: typing_extensions.NotRequired[float]
    stability: typing_extensions.NotRequired[float]
    similarity: typing_extensions.NotRequired[float]
