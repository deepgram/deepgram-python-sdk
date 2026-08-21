"""Regression coverage for read-only dictionary access on typed responses.

Listen V2 responses were raw dictionaries through SDK 7.6 because the response
union contained ``typing.Any``. SDK 7.7 fixed deserialization to return typed
models, which broke callers using the observed dictionary interface. Listen V2
response models now support both attribute and subscript access during that
transition.
"""

import json
import typing

import pytest

from deepgram.listen.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.listen.v2.types.listen_v2configure_failure import ListenV2ConfigureFailure
from deepgram.listen.v2.types.listen_v2configure_success import ListenV2ConfigureSuccess
from deepgram.listen.v2.types.listen_v2configure_success_thresholds import ListenV2ConfigureSuccessThresholds
from deepgram.listen.v2.types.listen_v2connected import ListenV2Connected
from deepgram.listen.v2.types.listen_v2fatal_error import ListenV2FatalError
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
    assert message.words[0].confidence == 0.96

    assert message["transcript"] == "hello"
    assert message.words[0]["confidence"] == 0.96
    assert message["words"][0]["confidence"] == 0.96
    assert message["future_field"] == "preserved"
    with pytest.raises(KeyError):
        message["languages"]


def test_sync_listen_v2_response_supports_both_access_styles() -> None:
    message = V2SocketClient(websocket=typing.cast(typing.Any, _FakeWebSocket())).recv()
    _assert_attribute_and_subscript_access(message)


async def test_async_listen_v2_response_supports_both_access_styles() -> None:
    message = await AsyncV2SocketClient(websocket=typing.cast(typing.Any, _FakeAsyncWebSocket())).recv()
    _assert_attribute_and_subscript_access(message)


def test_all_listen_v2_response_models_support_subscript_access() -> None:
    configure_success = ListenV2ConfigureSuccess(
        type="ConfigureSuccess",
        request_id="request-id",
        thresholds=ListenV2ConfigureSuccessThresholds(eot_threshold=0.7),
        keyterms=[],
        sequence_id=2,
    )
    responses: typing.List[typing.Any] = [
        ListenV2Connected(type="Connected", request_id="request-id", sequence_id=0),
        ListenV2ConfigureFailure(type="ConfigureFailure", request_id="request-id", sequence_id=1),
        configure_success,
        ListenV2FatalError(type="Error", sequence_id=3, code="ERROR", description="failure"),
    ]

    for response in responses:
        assert response["type"] == response.type
    assert configure_success.thresholds["eot_threshold"] == 0.7


def test_unrelated_models_do_not_gain_subscript_access() -> None:
    metadata = GetModelV1ResponseMetadata(uuid="model-id")

    assert metadata.uuid_ == "model-id"
    with pytest.raises(TypeError, match="not subscriptable"):
        metadata["uuid"]  # type: ignore[index]
