"""
Coverage for the Speak V2 (Flux TTS) barge-in and mid-stream reconfiguration
surface added in the 2026-08-11 regen. ``test_speak_v2_socket.py`` pins the
speak/flush/close surface and forward compatibility; this file pins what that
regen introduced, which shipped with no automated coverage:

  * ``send_interrupt`` — barge-in, with and without a ``playback_offset``.
  * ``send_configure`` — mid-stream ``speed`` changes.
  * response parsing — ``SpeechInterrupted`` (including nested metadata and the
    ``controls_applied`` counters), plus the ``ConfigureSuccess`` /
    ``ConfigureFailure`` acknowledgements.
  * connect query — the ``speed`` and ``expressivity`` parameters.

Both ``send_*`` methods here are generator-owned (they take a required message
model, unlike the patched no-payload ``send_flush``/``send_close``), so these
tests guard the wire shape a future regen must not silently change.

Note on ``_declared_fields``: these models are ``extra="allow"``, so asserting
``msg.<field>`` alone passes even when the field is *not declared* — the value
just arrives as an undeclared extra. Where the point is to pin the schema (not
just the value), assert against the declared field set instead.

Driven with a fake websocket / a capture shim — no network.
"""

import json
import urllib.parse
from unittest.mock import patch

import deepgram.speak.v2.client as speak_v2_client
from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.pydantic_utilities import IS_PYDANTIC_V2
from deepgram.speak.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.speak.v2.types.speak_v2configure import SpeakV2Configure
from deepgram.speak.v2.types.speak_v2configure_failure import SpeakV2ConfigureFailure
from deepgram.speak.v2.types.speak_v2configure_success import SpeakV2ConfigureSuccess
from deepgram.speak.v2.types.speak_v2interrupt import SpeakV2Interrupt
from deepgram.speak.v2.types.speak_v2interrupt_playback_offset import SpeakV2InterruptPlaybackOffset
from deepgram.speak.v2.types.speak_v2speech_interrupted import SpeakV2SpeechInterrupted
from deepgram.speak.v2.types.speak_v2speech_interrupted_metadata import SpeakV2SpeechInterruptedMetadata
from deepgram.speak.v2.types.speak_v2speech_interrupted_metadata_controls_applied import (
    SpeakV2SpeechInterruptedMetadataControlsApplied,
)

# A full server-emitted SpeechInterrupted frame. Every field on the nested
# metadata is required by the model, so this doubles as a shape assertion.
_SPEECH_INTERRUPTED = {
    "type": "SpeechInterrupted",
    "audio_played_ms": 1200,
    "text_spoken": "Hello there",
    "text_remaining": "how are you?",
    "metadata": {
        "speech_id": "speech-1",
        "audio_duration_ms": 4000,
        "input_character_count": 24,
        "billable_character_count": 24,
        "controls_applied": {
            "pronunciations_applied": 2,
            "breaks_applied": 1,
            "pronunciation_warnings": 0,
        },
    },
}


def _declared_fields(model_cls):
    """The model's *declared* field names (works on pydantic v1 and v2)."""
    return set(model_cls.model_fields if IS_PYDANTIC_V2 else model_cls.__fields__)


class _FakeWebSocket:
    """Captures ``.send()`` payloads and replays ``incoming`` on recv."""

    def __init__(self, incoming=None):
        self.sent = []
        self._incoming = list(incoming or [])

    def send(self, data):
        self.sent.append(data)

    def recv(self):
        return self._incoming.pop(0)

    def __iter__(self):
        yield from self._incoming


class _FakeAsyncWebSocket:
    """Async analogue of ``_FakeWebSocket``."""

    def __init__(self, incoming=None):
        self.sent = []
        self._incoming = list(incoming or [])

    async def send(self, data):
        self.sent.append(data)

    async def recv(self):
        return self._incoming.pop(0)


def _sent_json(ws):
    assert len(ws.sent) == 1
    payload = ws.sent[0]
    return json.loads(payload) if isinstance(payload, str) else payload


class TestSpeakV2Interrupt:
    def test_send_interrupt_serializes_bare(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_interrupt(SpeakV2Interrupt())
        assert _sent_json(ws) == {"type": "Interrupt"}

    def test_send_interrupt_no_arg_emits_default(self):
        # Interrupt carries no required payload, so it is callable with no
        # argument like the sibling send_flush()/send_close() controls
        # (hand-applied shim, frozen in .fernignore).
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_interrupt()
        assert _sent_json(ws) == {"type": "Interrupt"}

    async def test_async_send_interrupt_no_arg_emits_default(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV2SocketClient(websocket=ws).send_interrupt()
        assert _sent_json(ws) == {"type": "Interrupt"}

    def test_send_interrupt_serializes_playback_offset(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_interrupt(
            SpeakV2Interrupt(playback_offset=SpeakV2InterruptPlaybackOffset(value=1500))
        )
        assert _sent_json(ws) == {
            "type": "Interrupt",
            "playback_offset": {"type": "time_ms", "value": 1500},
        }

    async def test_async_send_interrupt_serializes(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV2SocketClient(websocket=ws).send_interrupt(SpeakV2Interrupt())
        assert _sent_json(ws) == {"type": "Interrupt"}

    def test_recv_parses_speech_interrupted(self):
        ws = _FakeWebSocket(incoming=[json.dumps(_SPEECH_INTERRUPTED)])
        msg = V2SocketClient(websocket=ws).recv()

        assert isinstance(msg, SpeakV2SpeechInterrupted)
        assert msg.audio_played_ms == 1200
        assert msg.text_spoken == "Hello there"
        assert msg.text_remaining == "how are you?"
        assert msg.metadata.speech_id == "speech-1"
        assert msg.metadata.billable_character_count == 24
        assert msg.metadata.controls_applied.breaks_applied == 1
        assert msg.metadata.controls_applied.pronunciations_applied == 2

    def test_speech_interrupted_metadata_schema_is_declared(self):
        # extra="allow" means value assertions alone can't detect a dropped
        # field, so pin the declared schema explicitly.
        assert {
            "speech_id",
            "audio_duration_ms",
            "input_character_count",
            "billable_character_count",
            "controls_applied",
        } <= _declared_fields(SpeakV2SpeechInterruptedMetadata)
        assert {
            "pronunciations_applied",
            "breaks_applied",
            "pronunciation_warnings",
        } <= _declared_fields(SpeakV2SpeechInterruptedMetadataControlsApplied)

    async def test_async_recv_parses_speech_interrupted(self):
        ws = _FakeAsyncWebSocket(incoming=[json.dumps(_SPEECH_INTERRUPTED)])
        msg = await AsyncV2SocketClient(websocket=ws).recv()
        assert isinstance(msg, SpeakV2SpeechInterrupted)
        assert msg.metadata.controls_applied.breaks_applied == 1


class TestSpeakV2Configure:
    def test_send_configure_serializes_speed(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_configure(SpeakV2Configure(speed=1.25))
        assert _sent_json(ws) == {"type": "Configure", "speed": 1.25}

    async def test_async_send_configure_serializes_speed(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV2SocketClient(websocket=ws).send_configure(SpeakV2Configure(speed=0.8))
        assert _sent_json(ws) == {"type": "Configure", "speed": 0.8}

    def test_recv_parses_configure_success(self):
        ws = _FakeWebSocket(
            incoming=[json.dumps({"type": "ConfigureSuccess", "applied": {"speed": 1.25}})]
        )
        msg = V2SocketClient(websocket=ws).recv()
        assert isinstance(msg, SpeakV2ConfigureSuccess)
        assert msg.applied.speed == 1.25

    def test_recv_parses_configure_failure(self):
        ws = _FakeWebSocket(
            incoming=[
                json.dumps(
                    {
                        "type": "ConfigureFailure",
                        "code": "SPEED_OUT_OF_RANGE",
                        "field": "speed",
                        "value": 9.0,
                        "description": "speed must be between 0.5 and 2.0",
                    }
                )
            ]
        )
        msg = V2SocketClient(websocket=ws).recv()
        assert isinstance(msg, SpeakV2ConfigureFailure)
        assert msg.code == "SPEED_OUT_OF_RANGE"
        assert msg.field == "speed"
        assert msg.value == 9.0
        assert "0.5" in msg.description


class _CaptureConnect:
    """Stands in for ``websockets(.sync).connect``: records the URL it is given."""

    def __init__(self):
        self.url = None

    def __call__(self, url, **kwargs):
        self.url = url
        return self

    def __enter__(self):
        return object()

    def __exit__(self, *exc):
        return False

    async def __aenter__(self):
        return object()

    async def __aexit__(self, *exc):
        return False


def _query(url):
    return urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)


def test_sync_connect_serializes_speed_and_expressivity():
    capture = _CaptureConnect()
    with patch.object(speak_v2_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(api_key="test_api_key").speak.v2.connect(
            model="flux-alexis-en",
            speed=1.25,
            expressivity=3,
        ):
            pass

    query = _query(capture.url)
    assert query["speed"] == ["1.25"]
    assert query["expressivity"] == ["3"]


async def test_async_connect_serializes_speed_and_expressivity():
    capture = _CaptureConnect()
    with patch.object(speak_v2_client, "websockets_client_connect", capture):
        async with AsyncDeepgramClient(api_key="test_api_key").speak.v2.connect(
            model="flux-alexis-en",
            speed=0.75,
            expressivity=1,
        ):
            pass

    query = _query(capture.url)
    assert query["speed"] == ["0.75"]
    assert query["expressivity"] == ["1"]
