"""Forward compatibility for Listen websocket responses this SDK does not know.

``construct_type`` returns ``None`` -- it never raises -- when no member of a
response union matches the incoming ``type``.  The generated ``except Exception``
guard therefore did not fire and a bare ``None`` was yielded to callers
(deepgram/deepgram-python-sdk#792).  Both Listen clients now fall back to the raw
JSON object instead.

The companion path, where ``construct_type`` *does* raise, is covered for every
socket client by ``test_core_internals_branches.py``.
"""

import json
import logging
import typing

import pytest

from deepgram.core.events import EventType
from deepgram.core.pydantic_utilities import IS_PYDANTIC_V2
from deepgram.listen.v1.socket_client import AsyncV1SocketClient, V1SocketClient, V1SocketClientResponse
from deepgram.listen.v1.types.listen_v1speech_started import ListenV1SpeechStarted
from deepgram.listen.v2.socket_client import AsyncV2SocketClient, V2SocketClient, V2SocketClientResponse
from deepgram.listen.v2.types.listen_v2warning import ListenV2Warning

UNKNOWN_RESPONSE: typing.Dict[str, typing.Any] = {
    "type": "FutureMessage",
    "request_id": "req-123",
    "sequence_id": 4,
    "details": {"reason": "new server feature", "values": [1, 2]},
}

# The Flux warning from #792, plus a V1 message, to pin that known types stay typed.
V2_KNOWN_RESPONSE: typing.Dict[str, typing.Any] = {
    "type": "Warning",
    "request_id": "req-123",
    "sequence_id": 5,
    "code": "FORCE_END_TURN_NO_ACTIVE_TURN",
    "description": "There is no active turn.",
}
V1_KNOWN_RESPONSE: typing.Dict[str, typing.Any] = {
    "type": "SpeechStarted",
    "channel": [0, 1],
    "timestamp": 0.5,
}


class _SyncWebSocket:
    def __init__(self, messages: typing.Sequence[typing.Any]) -> None:
        self.messages = list(messages)

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(self.messages)

    def recv(self) -> typing.Any:
        return self.messages.pop(0)


class _AsyncWebSocket:
    def __init__(self, messages: typing.Sequence[typing.Any]) -> None:
        self.messages = list(messages)

    async def __aiter__(self) -> typing.AsyncIterator[typing.Any]:
        for message in self.messages:
            yield message

    async def recv(self) -> typing.Any:
        return self.messages.pop(0)


_CLIENTS = [
    pytest.param(V1SocketClient, AsyncV1SocketClient, V1_KNOWN_RESPONSE, ListenV1SpeechStarted, id="listen-v1"),
    pytest.param(V2SocketClient, AsyncV2SocketClient, V2_KNOWN_RESPONSE, ListenV2Warning, id="listen-v2"),
]


def _sync_client(sync_cls: typing.Any, messages: typing.Sequence[typing.Any]) -> typing.Any:
    return sync_cls(websocket=typing.cast(typing.Any, _SyncWebSocket(messages)))


def _async_client(async_cls: typing.Any, messages: typing.Sequence[typing.Any]) -> typing.Any:
    return async_cls(websocket=typing.cast(typing.Any, _AsyncWebSocket(messages)))


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_iterator_returns_unknown_response_as_raw_json(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _sync_client(sync_cls, [json.dumps(UNKNOWN_RESPONSE)])

    assert list(client) == [UNKNOWN_RESPONSE]


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_iterator_returns_unknown_response_as_raw_json(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _async_client(async_cls, [json.dumps(UNKNOWN_RESPONSE)])

    assert [message async for message in client] == [UNKNOWN_RESPONSE]


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_listener_emits_unknown_response_as_raw_json(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _sync_client(sync_cls, [json.dumps(UNKNOWN_RESPONSE)])
    received: typing.List[typing.Any] = []
    errors: typing.List[typing.Any] = []
    client.on(EventType.MESSAGE, received.append)
    client.on(EventType.ERROR, errors.append)

    client.start_listening()

    assert received == [UNKNOWN_RESPONSE]
    assert errors == []


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_listener_emits_unknown_response_as_raw_json(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _async_client(async_cls, [json.dumps(UNKNOWN_RESPONSE)])
    received: typing.List[typing.Any] = []
    errors: typing.List[typing.Any] = []
    client.on(EventType.MESSAGE, received.append)
    client.on(EventType.ERROR, errors.append)

    await client.start_listening()

    assert received == [UNKNOWN_RESPONSE]
    assert errors == []


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_recv_returns_unknown_response_without_logging_payload(
    sync_cls: typing.Any,
    async_cls: typing.Any,
    known: typing.Any,
    known_type: typing.Any,
    caplog: pytest.LogCaptureFixture,
) -> None:
    client = _sync_client(sync_cls, [json.dumps(UNKNOWN_RESPONSE)])

    with caplog.at_level(logging.WARNING):
        assert client.recv() == UNKNOWN_RESPONSE

    assert "unrecognized" in caplog.text
    assert "new server feature" not in caplog.text  # the payload itself is never logged


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_recv_returns_unknown_response_as_raw_json(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _async_client(async_cls, [json.dumps(UNKNOWN_RESPONSE)])

    assert await client.recv() == UNKNOWN_RESPONSE


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_recv_keeps_known_responses_typed(
    sync_cls: typing.Any,
    async_cls: typing.Any,
    known: typing.Any,
    known_type: typing.Any,
    caplog: pytest.LogCaptureFixture,
) -> None:
    client = _sync_client(sync_cls, [json.dumps(known)])

    with caplog.at_level(logging.WARNING):
        response = client.recv()

    assert isinstance(response, known_type)
    assert response.type == known["type"]
    assert caplog.text == ""  # the dict fallback never shadows a known type


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_recv_keeps_known_responses_typed(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _async_client(async_cls, [json.dumps(known)])

    response = await client.recv()

    assert isinstance(response, known_type)
    assert response.type == known["type"]


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_iterator_passes_through_binary_frame(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    frame = b"audio-frame"
    client = _sync_client(sync_cls, [frame])

    assert list(client) == [frame]
    assert _sync_client(sync_cls, [frame]).recv() == frame


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_iterator_passes_through_binary_frame(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    frame = b"audio-frame"
    client = _async_client(async_cls, [frame])

    assert [message async for message in client] == [frame]
    assert await _async_client(async_cls, [frame]).recv() == frame


def _union_models(union: typing.Any) -> typing.List[typing.Any]:
    """Every pydantic member of a response union -- the dict fallback is not one."""
    return [member for member in typing.get_args(union) if isinstance(member, type) and member is not bytes]


def _type_literal(model: typing.Any) -> str:
    fields = model.model_fields if IS_PYDANTIC_V2 else model.__fields__
    return typing.cast(str, fields["type"].default)


_KNOWN_MODELS = [
    pytest.param(V1SocketClient, model, id=f"listen-v1-{model.__name__}")
    for model in _union_models(V1SocketClientResponse)
] + [
    pytest.param(V2SocketClient, model, id=f"listen-v2-{model.__name__}")
    for model in _union_models(V2SocketClientResponse)
]


@pytest.mark.parametrize("sync_cls,model", _KNOWN_MODELS)
def test_dict_fallback_never_shadows_a_known_response_type(
    sync_cls: typing.Any, model: typing.Any, caplog: pytest.LogCaptureFixture
) -> None:
    """Every member of both unions still decodes to its own model.

    The dict fallback sits last in each union and `construct_type` skips models
    whose `type` discriminant does not match before reaching it. If a regen ever
    renames a discriminant, that type would quietly degrade to a warned dict
    instead of failing loudly -- this matrix is what catches it.
    """
    client = _sync_client(sync_cls, [json.dumps({"type": _type_literal(model)})])

    with caplog.at_level(logging.WARNING):
        response = client.recv()

    assert isinstance(response, model)
    assert caplog.text == ""


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
def test_sync_null_frame_is_skipped_not_emitted(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    """A bare JSON `null` has nothing to hand back, so it is dropped rather than
    emitted as the `None` this fallback exists to avoid."""
    client = _sync_client(sync_cls, ["null"])
    received: typing.List[typing.Any] = []
    client.on(EventType.MESSAGE, received.append)

    client.start_listening()

    assert received == []
    assert list(_sync_client(sync_cls, ["null"])) == []


@pytest.mark.parametrize("sync_cls,async_cls,known,known_type", _CLIENTS)
async def test_async_null_frame_is_skipped_not_emitted(
    sync_cls: typing.Any, async_cls: typing.Any, known: typing.Any, known_type: typing.Any
) -> None:
    client = _async_client(async_cls, ["null"])
    received: typing.List[typing.Any] = []
    client.on(EventType.MESSAGE, received.append)

    await client.start_listening()

    assert received == []
    assert [message async for message in _async_client(async_cls, ["null"])] == []
