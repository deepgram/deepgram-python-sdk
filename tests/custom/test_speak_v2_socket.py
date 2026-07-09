"""
Coverage for the Speak V2 (Flux TTS) WebSocket socket client, added in the
2026-07-08 regen. Speak V2 is a public product but shipped with only indirect
coverage; this pins the behavior a future regen must not silently change:

  * send serialization — ``send_speak`` puts ``text`` on the wire; the no-payload
    control sends ``send_flush()`` / ``send_close()`` are callable with no
    argument and emit the correct default control message (hand-applied shim,
    frozen in .fernignore).
  * response parsing — inbound JSON resolves to the right ``SpeakV2*`` type via
    the ``type`` discriminant, and binary frames pass through as ``bytes``.
  * broad ``except`` — the listen loop surfaces *any* exception as an ERROR event
    (the generator narrows to ``websockets.WebSocketException``; the patch keeps
    the custom-transport error contract, which can raise arbitrary types).

Driven with a fake websocket — no network.
"""

import json

from deepgram.core.events import EventType
from deepgram.speak.v2.socket_client import V2SocketClient
from deepgram.speak.v2.types.speak_v2connected import SpeakV2Connected
from deepgram.speak.v2.types.speak_v2error import SpeakV2Error
from deepgram.speak.v2.types.speak_v2flushed import SpeakV2Flushed
from deepgram.speak.v2.types.speak_v2speak import SpeakV2Speak


class _FakeWebSocket:
    """Captures ``.send()`` payloads and replays ``incoming`` on iteration / recv."""

    def __init__(self, incoming=None, raise_on_iter=None):
        self.sent = []
        self._incoming = list(incoming or [])
        self._raise_on_iter = raise_on_iter

    def send(self, data):
        self.sent.append(data)

    def recv(self):
        return self._incoming.pop(0)

    def __iter__(self):
        if self._raise_on_iter is not None:
            raise self._raise_on_iter
        yield from self._incoming


def _sent_json(ws):
    assert len(ws.sent) == 1
    payload = ws.sent[0]
    return json.loads(payload) if isinstance(payload, str) else payload


class TestSpeakV2Send:
    def test_send_speak_serializes_text(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_speak(SpeakV2Speak(text="Hello, world!"))
        assert _sent_json(ws) == {"type": "Speak", "text": "Hello, world!"}

    def test_send_flush_no_arg_emits_default(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_flush()
        assert _sent_json(ws)["type"] == "Flush"

    def test_send_close_no_arg_emits_default(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_close()
        assert _sent_json(ws)["type"] == "Close"


class TestSpeakV2ResponseParsing:
    def test_recv_parses_connected(self):
        ws = _FakeWebSocket(
            incoming=[
                json.dumps(
                    {
                        "type": "Connected",
                        "request_id": "req-1",
                        "model_name": "flux-alexis-en",
                        "model_version": "1",
                        "model_uuids": ["uuid-1"],
                    }
                )
            ]
        )
        msg = V2SocketClient(websocket=ws).recv()
        assert isinstance(msg, SpeakV2Connected)
        assert msg.request_id == "req-1"

    def test_recv_parses_flushed_and_error(self):
        ws = _FakeWebSocket(
            incoming=[
                json.dumps({"type": "Flushed", "speech_id": "s-1"}),
                json.dumps({"type": "Error", "code": "SOME_CODE", "description": "boom"}),
            ]
        )
        client = V2SocketClient(websocket=ws)
        assert isinstance(client.recv(), SpeakV2Flushed)
        assert isinstance(client.recv(), SpeakV2Error)

    def test_recv_returns_binary_audio_passthrough(self):
        audio = b"\x00\x01\x02audio-frame"
        ws = _FakeWebSocket(incoming=[audio])
        assert V2SocketClient(websocket=ws).recv() == audio


class TestSpeakV2Broadexcept:
    def test_listen_loop_surfaces_non_websocket_error(self):
        # A custom transport can raise arbitrary exception types from iteration;
        # the narrow generated catch would let this escape instead of emitting ERROR.
        boom = ValueError("transport blew up")
        ws = _FakeWebSocket(raise_on_iter=boom)
        client = V2SocketClient(websocket=ws)

        events = []
        client.on(EventType.ERROR, lambda exc: events.append(("error", exc)))
        client.on(EventType.CLOSE, lambda _: events.append(("close", None)))

        client.start_listening()

        assert ("error", boom) in events
        assert events[-1] == ("close", None)
