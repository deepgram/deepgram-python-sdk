# Server -> client messages on wss://api.60db.ai/ws/tts.
#
# 60db wraps each event in a single outer key (connection_established,
# context_created, audio_chunk, flush_completed, context_closed, error)
# rather than a flat {type: ...} discriminator. We model the envelope as a
# single class with all sub-objects optional; the WS client iterates raw
# events and picks the populated field. `audioContent` keeps its camelCase
# wire name via alias.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.unchecked_base_model import UncheckedBaseModel


class SixtyDbWsConnectionEstablished(UncheckedBaseModel):
    service: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    credit_balance: typing.Optional[float] = None
    workspace: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow


class SixtyDbWsContextCreated(UncheckedBaseModel):
    context_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow


class SixtyDbWsAudioChunk(UncheckedBaseModel):
    context_id: typing.Optional[str] = None
    audio_content: typing.Optional[str] = pydantic.Field(default=None, alias="audioContent")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True, populate_by_name=True
        )  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow
            allow_population_by_field_name = True


class SixtyDbWsFlushCompleted(UncheckedBaseModel):
    context_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow


class SixtyDbWsContextClosed(UncheckedBaseModel):
    context_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow


class SixtyDbWsError(UncheckedBaseModel):
    context_id: typing.Optional[str] = None
    message: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow


class SixtyDbWsEvent(UncheckedBaseModel):
    """Envelope for any server -> client message. Exactly one field is set."""

    connection_established: typing.Optional[SixtyDbWsConnectionEstablished] = None
    context_created: typing.Optional[SixtyDbWsContextCreated] = None
    audio_chunk: typing.Optional[SixtyDbWsAudioChunk] = None
    flush_completed: typing.Optional[SixtyDbWsFlushCompleted] = None
    context_closed: typing.Optional[SixtyDbWsContextClosed] = None
    error: typing.Optional[SixtyDbWsError] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore
    else:

        class Config:
            frozen = True
            extra = pydantic.Extra.allow
