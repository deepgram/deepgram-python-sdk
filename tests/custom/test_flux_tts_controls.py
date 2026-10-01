"""Deterministic coverage for Flux batch and streaming control response shapes."""

import json

import httpx
import respx

from deepgram import DeepgramClient
from deepgram.environment import DeepgramClientEnvironment
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
                headers={"dg-pronunciations-applied": "1", "dg-breaks-applied": "1", "dg-warnings": "PRON-001"},
                content=b"audio",
            )
        )
        with DeepgramClient(environment=ENVIRONMENT, api_key="test").speak.v2.audio.with_raw_response.generate(
            model="flux-alexis-en", text='Hello {"word":"Deepgram","pronounce":"diːpɡræm"}'
        ) as response:
            assert b"".join(response.data) == b"audio"
            assert response.headers["dg-pronunciations-applied"] == "1"
            assert response.headers["dg-breaks-applied"] == "1"
            assert response.headers["dg-warnings"] == "PRON-001"
    assert json.loads(route.calls.last.request.content) == {
        "text": 'Hello {"word":"Deepgram","pronounce":"diːpɡræm"}'
    }


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
