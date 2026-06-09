# NDJSON line type emitted by POST https://api.60db.ai/tts-stream.
# Server sends one JSON object per line; `type` is the discriminant.
# Audio payload arrives base64-encoded under result.audioContent.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class SixtyDbStreamChunkResult(UncheckedBaseModel):
    # 60db returns camelCase here; alias keeps the snake_case attr ergonomic.
    audio_content: typing.Optional[str] = pydantic.Field(default=None, alias="audioContent")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True, populate_by_name=True
        )  # type: ignore
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
            allow_population_by_field_name = True


class SixtyDbStreamChunk(UncheckedBaseModel):
    type: typing.Optional[str] = pydantic.Field(default=None)
    """
    One of "chunk", "complete", "error".
    """

    result: typing.Optional[SixtyDbStreamChunkResult] = pydantic.Field(default=None)
    """
    Present on "chunk" lines. Holds the base64 audio payload.
    """

    message: typing.Optional[str] = pydantic.Field(default=None)
    """
    Present on "error" lines.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
