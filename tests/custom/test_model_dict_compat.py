"""Regression coverage for read-only dictionary access on typed responses.

Listen V2 responses were raw dictionaries through SDK 7.6 because the response
union contained ``typing.Any``. SDK 7.7 fixed deserialization to return typed
models, which broke callers using the observed dictionary interface. Typed
models now support both attribute and subscript access during that transition.
"""

import json

import pytest

from deepgram.listen.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.listen.v2.types.listen_v2turn_info import ListenV2TurnInfo
from deepgram.types.get_model_v1response_metadata import GetModelV1ResponseMetadata

TURN_INFO = {
    "type": "TurnInfo",
    "request_id": "request-id",
    "sequence_id": 1,
    "event": "EndOfTurn",
    "turn_index": 0,
    "audio_window_start": 0.0,
    "audio_window_end": 1.0,
    "transcript": "hello",
    "words": [{"word": "hello", "confidence": 0.96}],
    "end_of_turn_confidence": 0.9,
    "future_field": "preserved",
}


class _FakeWebSocket:
    def recv(self) -> str:
        return json.dumps(TURN_INFO)


class _FakeAsyncWebSocket:
    async def recv(self) -> str:
        return json.dumps(TURN_INFO)


def _assert_attribute_and_subscript_access(message: object) -> None:
    assert isinstance(message, ListenV2TurnInfo)

    assert message.transcript == "hello"
    assert message["transcript"] == "hello"

    assert message.words[0].confidence == 0.96
    assert message.words[0]["confidence"] == 0.96
    assert message["words"][0]["confidence"] == 0.96

    assert message["future_field"] == "preserved"
    with pytest.raises(KeyError):
        message["trigger"]


def test_sync_listen_v2_response_supports_both_access_styles() -> None:
    message = V2SocketClient(websocket=_FakeWebSocket()).recv()
    _assert_attribute_and_subscript_access(message)


async def test_async_listen_v2_response_supports_both_access_styles() -> None:
    message = await AsyncV2SocketClient(websocket=_FakeAsyncWebSocket()).recv()
    _assert_attribute_and_subscript_access(message)


def test_subscript_access_uses_wire_aliases() -> None:
    metadata = GetModelV1ResponseMetadata(uuid="model-id")

    assert metadata.uuid_ == "model-id"
    assert metadata["uuid"] == "model-id"
    with pytest.raises(KeyError):
        metadata["uuid_"]
