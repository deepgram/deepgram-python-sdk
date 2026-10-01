"""Deterministic coverage for Flux batch and streaming control response shapes."""

import json

import httpx
import pytest
import respx

from deepgram import DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment
from deepgram.helpers import TextBuilder
from deepgram.speak.v2.socket_client import V2SocketClient
from deepgram.speak.v2.types import SpeakV2ConfigureFailure, SpeakV2SpeechMetadata, SpeakV2Warning

HOST = "controls.deepgram.test"
ENVIRONMENT = DeepgramClientEnvironment(
    base=f"https://{HOST}", production=f"wss://{HOST}", agent=f"wss://{HOST}", agent_rest=f"https://{HOST}"
)


class _FakeWebSocket:
    def __init__(self, message):
        self.message = json.dumps(message)

    def recv(self):
        return self.message


def test_batch_raw_response_exposes_control_headers_and_serializes_controls() -> None:
    with respx.mock:
        route = respx.post(f"https://{HOST}/v2/speak").mock(
            return_value=httpx.Response(
                200,
                headers={"dg-pronunciations-applied": "1", "dg-breaks-applied": "0", "dg-warnings": "PRON-001"},
                content=b"audio",
            )
        )
        text = TextBuilder().text("Hello ").pronunciation("Deepgram", "diːpɡræm").text(".").build()
        with DeepgramClient(environment=ENVIRONMENT, api_key="test").speak.v2.audio.with_raw_response.generate(
            model="flux-alexis-en", text=text
        ) as response:
            assert b"".join(response.data) == b"audio"
            assert response.headers["dg-pronunciations-applied"] == "1"
            assert response.headers["dg-breaks-applied"] == "0"
            assert response.headers["dg-warnings"] == "PRON-001"
    assert json.loads(route.calls.last.request.content) == {
        "text": r'Hello \{"word": "Deepgram", "pronounce": "diːpɡræm"\}.'
    }


def test_batch_speed_with_pronunciation_raises_control_combination_error() -> None:
    with respx.mock:
        route = respx.post(f"https://{HOST}/v2/speak").mock(
            return_value=httpx.Response(
                400,
                json={
                    "err_code": "CONTROL_COMBINATION_INVALID",
                    "err_msg": "pronunciation controls require speed 1.0",
                },
            )
        )
        text = TextBuilder().pronunciation("Deepgram", "diːpɡræm").build()
        with pytest.raises(ApiError) as excinfo:
            list(
                DeepgramClient(environment=ENVIRONMENT, api_key="test").speak.v2.audio.generate(
                    model="flux-alexis-en", text=text, speed=1.1
                )
            )

    assert excinfo.value.status_code == 400
    assert excinfo.value.body["err_code"] == "CONTROL_COMBINATION_INVALID"
    assert json.loads(route.calls.last.request.content) == {
        "text": r'\{"word": "Deepgram", "pronounce": "diːpɡræm"\}'
    }
    assert route.calls.last.request.url.params["speed"] == "1.1"


def test_streaming_control_failure_warning_and_counters_parse() -> None:
    configure = V2SocketClient(
        websocket=_FakeWebSocket(
            {"type": "ConfigureFailure", "code": "CONTROL_COMBINATION_INVALID", "description": "flush the buffered turn"}
        )
    ).recv()
    assert isinstance(configure, SpeakV2ConfigureFailure)
    assert configure.code == "CONTROL_COMBINATION_INVALID"

    warning = V2SocketClient(websocket=_FakeWebSocket({"type": "Warning", "code": "PRONUNCIATION_WARNINGS", "description": "IPA warning"})).recv()
    assert isinstance(warning, SpeakV2Warning)
    assert warning.code == "PRONUNCIATION_WARNINGS"

    metadata = V2SocketClient(
        websocket=_FakeWebSocket(
            {"type": "SpeechMetadata", "speech_id": "speech", "audio_duration_ms": 10, "input_character_count": 5, "billable_character_count": 5, "controls_applied": {"pronunciations_applied": 1, "breaks_applied": 0, "pronunciation_warnings": 1}}
        )
    ).recv()
    assert isinstance(metadata, SpeakV2SpeechMetadata)
    assert metadata.controls_applied.pronunciations_applied == 1
    assert metadata.controls_applied.breaks_applied == 0
    assert metadata.controls_applied.pronunciation_warnings == 1
