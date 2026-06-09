# Response body for POST https://api.60db.ai/tts-synthesize.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class SixtyDbSynthesizeResponse(UncheckedBaseModel):
    success: typing.Optional[bool] = pydantic.Field(default=None)
    message: typing.Optional[str] = pydantic.Field(default=None)
    audio_base64: typing.Optional[str] = pydantic.Field(default=None)
    """
    Base64-encoded audio payload. Decode with base64.b64decode().
    """

    sample_rate: typing.Optional[int] = pydantic.Field(default=None)
    duration_seconds: typing.Optional[float] = pydantic.Field(default=None)
    encoding: typing.Optional[str] = pydantic.Field(default=None)
    output_format: typing.Optional[str] = pydantic.Field(default=None)

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
