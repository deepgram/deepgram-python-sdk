"""Tests that control send_ methods work without requiring a message argument.

Regression test for the breaking change where optional message params were lost
during a Fern regen, causing TypeError for callers using no-arg control calls.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from deepgram.agent.v1.socket_client import AsyncV1SocketClient as AsyncAgentV1SocketClient
from deepgram.agent.v1.socket_client import V1SocketClient as AgentV1SocketClient
from deepgram.listen.v1.socket_client import AsyncV1SocketClient as AsyncListenV1SocketClient
from deepgram.listen.v1.socket_client import V1SocketClient as ListenV1SocketClient
from deepgram.listen.v2.socket_client import AsyncV2SocketClient as AsyncListenV2SocketClient
from deepgram.listen.v2.socket_client import V2SocketClient as ListenV2SocketClient
from deepgram.speak.v1.socket_client import AsyncV1SocketClient as AsyncSpeakV1SocketClient
from deepgram.speak.v1.socket_client import V1SocketClient as SpeakV1SocketClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_async_ws():
    ws = AsyncMock()
    ws.send = AsyncMock()
    return ws


def _make_sync_ws():
    ws = MagicMock()
    ws.send = MagicMock()
    return ws


def _sent_json(ws):
    """Return the parsed JSON from the first send() call."""
    call_args = ws.send.call_args
    data = call_args[0][0]
    return json.loads(data)


# ---------------------------------------------------------------------------
# speak/v1 — async
# ---------------------------------------------------------------------------

class TestAsyncSpeakV1ControlMessages:
    async def test_send_flush_no_args(self):
        ws = _make_async_ws()
        client = AsyncSpeakV1SocketClient(websocket=ws)
        await client.send_flush()
        assert _sent_json(ws)["type"] == "Flush"

    async def test_send_clear_no_args(self):
        ws = _make_async_ws()
        client = AsyncSpeakV1SocketClient(websocket=ws)
        await client.send_clear()
        assert _sent_json(ws)["type"] == "Clear"

    async def test_send_close_no_args(self):
        ws = _make_async_ws()
        client = AsyncSpeakV1SocketClient(websocket=ws)
        await client.send_close()
        assert _sent_json(ws)["type"] == "Close"


# ---------------------------------------------------------------------------
# speak/v1 — sync
# ---------------------------------------------------------------------------

class TestSyncSpeakV1ControlMessages:
    def test_send_flush_no_args(self):
        ws = _make_sync_ws()
        client = SpeakV1SocketClient(websocket=ws)
        client.send_flush()
        assert _sent_json(ws)["type"] == "Flush"

    def test_send_clear_no_args(self):
        ws = _make_sync_ws()
        client = SpeakV1SocketClient(websocket=ws)
        client.send_clear()
        assert _sent_json(ws)["type"] == "Clear"

    def test_send_close_no_args(self):
        ws = _make_sync_ws()
        client = SpeakV1SocketClient(websocket=ws)
        client.send_close()
        assert _sent_json(ws)["type"] == "Close"


# ---------------------------------------------------------------------------
# listen/v1 — async
# ---------------------------------------------------------------------------

class TestAsyncListenV1ControlMessages:
    async def test_send_finalize_no_args(self):
        ws = _make_async_ws()
        client = AsyncListenV1SocketClient(websocket=ws)
        await client.send_finalize()
        assert _sent_json(ws)["type"] == "Finalize"

    async def test_send_close_stream_no_args(self):
        ws = _make_async_ws()
        client = AsyncListenV1SocketClient(websocket=ws)
        await client.send_close_stream()
        assert _sent_json(ws)["type"] == "CloseStream"

    async def test_send_keep_alive_no_args(self):
        ws = _make_async_ws()
        client = AsyncListenV1SocketClient(websocket=ws)
        await client.send_keep_alive()
        assert _sent_json(ws)["type"] == "KeepAlive"


# ---------------------------------------------------------------------------
# listen/v1 — sync
# ---------------------------------------------------------------------------

class TestSyncListenV1ControlMessages:
    def test_send_finalize_no_args(self):
        ws = _make_sync_ws()
        client = ListenV1SocketClient(websocket=ws)
        client.send_finalize()
        assert _sent_json(ws)["type"] == "Finalize"

    def test_send_close_stream_no_args(self):
        ws = _make_sync_ws()
        client = ListenV1SocketClient(websocket=ws)
        client.send_close_stream()
        assert _sent_json(ws)["type"] == "CloseStream"

    def test_send_keep_alive_no_args(self):
        ws = _make_sync_ws()
        client = ListenV1SocketClient(websocket=ws)
        client.send_keep_alive()
        assert _sent_json(ws)["type"] == "KeepAlive"


# ---------------------------------------------------------------------------
# listen/v2 — async
# ---------------------------------------------------------------------------

class TestAsyncListenV2ControlMessages:
    async def test_send_close_stream_no_args(self):
        ws = _make_async_ws()
        client = AsyncListenV2SocketClient(websocket=ws)
        await client.send_close_stream()
        assert _sent_json(ws)["type"] == "CloseStream"


# ---------------------------------------------------------------------------
# listen/v2 — sync
# ---------------------------------------------------------------------------

class TestSyncListenV2ControlMessages:
    def test_send_close_stream_no_args(self):
        ws = _make_sync_ws()
        client = ListenV2SocketClient(websocket=ws)
        client.send_close_stream()
        assert _sent_json(ws)["type"] == "CloseStream"


# ---------------------------------------------------------------------------
# agent/v1 — async
# ---------------------------------------------------------------------------

class TestAsyncAgentV1ControlMessages:
    async def test_send_keep_alive_no_args(self):
        ws = _make_async_ws()
        client = AsyncAgentV1SocketClient(websocket=ws)
        await client.send_keep_alive()
        assert _sent_json(ws)["type"] == "KeepAlive"


# ---------------------------------------------------------------------------
# agent/v1 — sync
# ---------------------------------------------------------------------------

class TestSyncAgentV1ControlMessages:
    def test_send_keep_alive_no_args(self):
        ws = _make_sync_ws()
        client = AgentV1SocketClient(websocket=ws)
        client.send_keep_alive()
        assert _sent_json(ws)["type"] == "KeepAlive"
