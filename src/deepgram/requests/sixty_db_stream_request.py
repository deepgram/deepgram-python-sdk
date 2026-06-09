# Request body for POST https://api.60db.ai/tts-stream (NDJSON streaming).
# Same shape as the one-shot synth minus output_format (stream format is
# fixed by the chunk protocol).

import typing_extensions


class SixtyDbStreamRequestParams(typing_extensions.TypedDict):
    text: str
    """
    Max 5000 characters.
    """

    voice_id: typing_extensions.NotRequired[str]
    enhance: typing_extensions.NotRequired[bool]
    speed: typing_extensions.NotRequired[float]
    stability: typing_extensions.NotRequired[float]
    similarity: typing_extensions.NotRequired[float]
