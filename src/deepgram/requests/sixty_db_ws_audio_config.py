# audio_config sub-struct of the create_context WS message.

import typing_extensions
from ..types.sixty_db_audio_encoding import SixtyDbAudioEncoding
from ..types.sixty_db_sample_rate_hertz import SixtyDbSampleRateHertz


class SixtyDbWsAudioConfigParams(typing_extensions.TypedDict):
    audio_encoding: typing_extensions.NotRequired[SixtyDbAudioEncoding]
    sample_rate_hertz: typing_extensions.NotRequired[SixtyDbSampleRateHertz]
