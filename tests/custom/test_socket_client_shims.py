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

import pydantic
import pytest

from deepgram.agent.v1.socket_client import AsyncV1SocketClient, V1SocketClient, _sanitize_numeric_types
from deepgram.agent.v1.types.agent_v1force_end_turn import AgentV1ForceEndTurn
from deepgram.agent.v1.types.agent_v1settings import AgentV1Settings
from deepgram.agent.v1.types.agent_v1settings_agent import AgentV1SettingsAgent
from deepgram.agent.v1.types.agent_v1settings_agent_listen import AgentV1SettingsAgentListen
from deepgram.agent.v1.types.agent_v1settings_agent_listen_provider import AgentV1SettingsAgentListenProvider_V1
from deepgram.agent.v1.types.agent_v1settings_audio import AgentV1SettingsAudio
from deepgram.agent.v1.types.agent_v1settings_audio_input import AgentV1SettingsAudioInput
from deepgram.listen.v2.socket_client import AsyncV2SocketClient, V2SocketClient
from deepgram.listen.v2.types.listen_v2close_stream import ListenV2CloseStream
from deepgram.listen.v2.types.listen_v2configure import ListenV2Configure
from deepgram.listen.v2.types.listen_v2force_end_turn import ListenV2ForceEndTurn
from deepgram.speak.v2.socket_client import V2SocketClient as SpeakV2SocketClient
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi


class _FakeWebSocket:
    """Captures whatever the socket client hands to ``.send()``."""

    def __init__(self):
        self.sent = []

    def send(self, data):
        self.sent.append(data)


class _FakeAsyncWebSocket:
    """Async counterpart of _FakeWebSocket for the async socket clients."""

    def __init__(self):
        self.sent = []

    async def send(self, data):
        self.sent.append(data)


def _sent_json(ws):
    assert len(ws.sent) == 1
    payload = ws.sent[0]
    return json.loads(payload) if isinstance(payload, str) else payload


def _agent_settings_with_expressivity() -> AgentV1Settings:
    return AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
        agent=AgentV1SettingsAgent(
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3")
            ),
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini"),
                prompt="Be concise.",
            ),
            speak=SpeakSettingsV1(
                provider=SpeakSettingsV1Provider_Deepgram(
                    type="deepgram", version="v2", model="flux-alexis-en", expressivity=2
                )
            ),
        ),
    )


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

    def test_listen_v2_force_end_turn_no_arg(self):
        # send_force_end_turn was added in the 2026-08-18 regen and given the same
        # optional-no-payload default treatment as the sibling control sends.
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_force_end_turn()
        assert _sent_json(ws) == {"type": "ForceEndTurn"}

    def test_listen_v2_force_end_turn_explicit_message(self):
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_force_end_turn(ListenV2ForceEndTurn(type="ForceEndTurn"))
        assert _sent_json(ws)["type"] == "ForceEndTurn"

    def test_agent_force_end_turn_no_arg(self):
        ws = _FakeWebSocket()
        V1SocketClient(websocket=ws).send_force_end_turn()
        assert _sent_json(ws) == {"type": "ForceEndTurn"}

    def test_agent_force_end_turn_explicit_message(self):
        ws = _FakeWebSocket()
        V1SocketClient(websocket=ws).send_force_end_turn(AgentV1ForceEndTurn(type="ForceEndTurn"))
        assert _sent_json(ws) == {"type": "ForceEndTurn"}

    async def test_listen_v2_force_end_turn_async_no_arg(self):
        # Cover the async client's send_force_end_turn too (asyncio_mode="auto").
        ws = _FakeAsyncWebSocket()
        await AsyncV2SocketClient(websocket=ws).send_force_end_turn()
        assert _sent_json(ws) == {"type": "ForceEndTurn"}

    async def test_agent_force_end_turn_async_no_arg(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV1SocketClient(websocket=ws).send_force_end_turn()
        assert _sent_json(ws) == {"type": "ForceEndTurn"}


class TestAgentSettingsSerialization:
    @pytest.mark.parametrize("expressivity", [1.5, True, "2"])
    def test_expressivity_requires_a_plain_integer(self, expressivity):
        with pytest.raises(pydantic.ValidationError):
            SpeakSettingsV1Provider_Deepgram(
                type="deepgram", version="v2", model="flux-alexis-en", expressivity=expressivity
            )

    def test_sync_send_settings_serializes_expressivity(self):
        ws = _FakeWebSocket()
        V1SocketClient(websocket=ws).send_settings(_agent_settings_with_expressivity())
        assert _sent_json(ws)["agent"]["speak"]["provider"]["expressivity"] == 2

    async def test_async_send_settings_serializes_expressivity(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV1SocketClient(websocket=ws).send_settings(_agent_settings_with_expressivity())
        assert _sent_json(ws)["agent"]["speak"]["provider"]["expressivity"] == 2


class TestSendConfigureRawShim:
    def test_passthrough_dict_is_sent_verbatim(self):
        ws = _FakeWebSocket()
        body = {"type": "Configure", "language_hints": ["en", "es"]}
        V2SocketClient(websocket=ws).send_configure(body)
        assert _sent_json(ws) == body

    def test_typed_model_is_serialized_and_sent(self):
        # The other branch of the Union[ListenV2Configure, dict] shim: a typed
        # model goes through _send_model (.dict()) rather than the raw dict path.
        ws = _FakeWebSocket()
        V2SocketClient(websocket=ws).send_configure(ListenV2Configure(language_hints=["en"]))
        sent = _sent_json(ws)
        assert sent["type"] == "Configure"
        assert sent["language_hints"] == ["en"]

    async def test_typed_model_is_serialized_and_sent_async(self):
        ws = _FakeAsyncWebSocket()
        await AsyncV2SocketClient(websocket=ws).send_configure(ListenV2Configure(language_hints=["en"]))
        sent = _sent_json(ws)
        assert sent["type"] == "Configure"
        assert sent["language_hints"] == ["en"]

    async def test_passthrough_dict_is_sent_verbatim_async(self):
        ws = _FakeAsyncWebSocket()
        body = {"type": "Configure", "language_hints": ["en", "es"]}
        await AsyncV2SocketClient(websocket=ws).send_configure(body)
        assert _sent_json(ws) == body
