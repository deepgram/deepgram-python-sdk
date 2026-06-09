# Request body for POST https://api.60db.ai/tts-synthesize.

import typing_extensions
from ..types.sixty_db_output_format import SixtyDbOutputFormat


class SixtyDbSynthesizeRequestParams(typing_extensions.TypedDict):
    text: str
    """
    Max 5000 characters.
    """

    voice_id: typing_extensions.NotRequired[str]
    voice: typing_extensions.NotRequired[str]
    enhance: typing_extensions.NotRequired[bool]
    speed: typing_extensions.NotRequired[float]
    stability: typing_extensions.NotRequired[float]
    similarity: typing_extensions.NotRequired[float]
    output_format: typing_extensions.NotRequired[SixtyDbOutputFormat]
