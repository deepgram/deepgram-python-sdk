"""
Coverage for the hand-maintained socket-client shims (frozen in .fernignore),
which previously had no automated tests. A future regen could silently revert
any of these; these tests gate them.

  * ``_sanitize_numeric_types`` — the agent socket client coerces whole-number
    floats to ``int`` before send (the API rejects e.g. ``sample_rate=44100.0``),
    and ``_send_model`` pipes payloads through it.
  * Optional ``message`` param on no-payload control sends — ``send_close_stream()``
    / ``send_keep_alive()`` are callable with no argument and emit the correct
    default control message.
  * listen/v2 ``send_configure(message: typing.Any)`` — raw passthrough shim
    (the generated ``ListenV2Configure`` model is intentionally bypassed).

The sync socket clients are driven with a fake websocket that captures whatever
is handed to ``.send()`` — the same payload that goes on the wire.
"""

import json

from deepgram.agent.v1.socket_client import V1SocketClient, _sanitize_numeric_types
from deepgram.listen.v2.socket_client import V2SocketClient
from deepgram.listen.v2.types.listen_v2close_stream import ListenV2CloseStream
from deepgram.speak.v2.socket_client import V2SocketClient as SpeakV2SocketClient


class _FakeWebSocket:
    """Captures whatever the socket client hands to ``.send()``."""

    def __init__(self):
        self.sent = []

    def send(self, data):
        self.sent.append(data)


def _sent_json(ws):
    assert len(ws.sent) == 1
    payload = ws.sent[0]
    return json.loads(payload) if isinstance(payload, str) else payload


class TestSanitizeNumericTypes:
    def test_whole_float_becomes_int(self):
        result = _sanitize_numeric_types(44100.0)
        assert result == 44100
        assert isinstance(result, int)

    def test_non_whole_float_unchanged(self):
        result = _sanitize_numeric_types(0.5)
        assert result == 0.5
        assert isinstance(result, float)

    def test_recurses_through_dicts_and_lists(self):
        out = _sanitize_numeric_types({"sample_rate": 44100.0, "nested": [1.0, 2.5, {"x": 3.0}]})
        assert out == {"sample_rate": 44100, "nested": [1, 2.5, {"x": 3}]}

    def test_passthrough_other_types(self):
        assert _sanitize_numeric_types("44100.0") == "44100.0"
        assert _sanitize_numeric_types(7) == 7
        assert _sanitize_numeric_types(None) is None

    def test_wired_into_agent_send_model(self):
        # _send_model must pipe the serialized payload through _sanitize_numeric_types.
        class _Stub:
            def dict(self):
                return {"sample_rate": 16000.0}

        ws = _FakeWebSocket()
        V1SocketClient(websocket=ws)._send_model(_Stub())
        assert _sent_json(ws) == {"sample_rate": 16000}


class TestOptionalMessageControlSends:
    def test_listen_v2_close_stream_no_arg(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_close_stream()
        assert _sent_json(ws)["type"] == "CloseStream"

    def test_listen_v2_close_stream_explicit_message(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_close_stream(ListenV2CloseStream(type="CloseStream"))
        assert _sent_json(ws)["type"] == "CloseStream"

    def test_agent_keep_alive_no_arg(self):
        ws = _FakeWebSocket()
        V1SocketClient(websocket=ws).send_keep_alive()
        assert _sent_json(ws)["type"] == "KeepAlive"

    def test_speak_v2_flush_no_arg(self):
        ws = _FakeWebSocket()
        SpeakV2SocketClient(websocket=ws).send_flush()
        assert _sent_json(ws)["type"] == "Flush"

    def test_speak_v2_close_no_arg(self):
        ws = _FakeWebSocket()
        SpeakV2SocketClient(websocket=ws).send_close()
        assert _sent_json(ws)["type"] == "Close"


class TestSendConfigureRawShim:
    def test_passthrough_dict_is_sent_verbatim(self):
        ws = _FakeWebSocket()
        body = {"type": "Configure", "language_hints": ["en", "es"]}
        V2SocketClient(websocket=ws).send_configure(body)
        assert _sent_json(ws) == body
