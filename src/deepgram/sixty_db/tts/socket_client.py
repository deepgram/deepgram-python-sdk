# Async WebSocket client for wss://api.60db.ai/ws/tts.
#
# Lifecycle: connect -> connection_established -> create_context ->
# (send_text)* -> flush_context -> audio_chunks -> flush_completed ->
# close_context -> context_closed -> disconnect.
#
# Uses the `websockets` library which is already a runtime dep for the
# Deepgram voice_agent module.

from __future__ import annotations

import json
import typing
import uuid

import websockets

from ...core.api_error import ApiError
from ...types.sixty_db_ws_event import SixtyDbWsEvent

try:
    from websockets.legacy.client import WebSocketClientProtocol  # type: ignore
except ImportError:  # newer websockets versions
    from websockets import WebSocketClientProtocol  # type: ignore


class AsyncTtsSocketClient:
    """Async context-manager wrapper around the 60db TTS WebSocket.

    Typical usage:

        async with client.sixty_db.tts.websocket() as ws:
            ctx_id = await ws.create_context(voice_id="...")
            await ws.send_text("Hello, world.")
            await ws.flush()
            async for event in ws:
                if event.audio_chunk:
                    ...
                elif event.flush_completed:
                    break
            await ws.close_context()
    """

    def __init__(self, *, api_key: typing.Optional[str], ws_base: str):
        if not api_key:
            raise ApiError(
                body=(
                    "60db API key missing. Pass sixty_db_api_key= when constructing "
                    "DeepgramClient/AsyncDeepgramClient."
                )
            )
        self._api_key = api_key
        self._ws_base = ws_base
        self._ws: typing.Optional[WebSocketClientProtocol] = None
        self._context_id: typing.Optional[str] = None

    @property
    def context_id(self) -> typing.Optional[str]:
        """The active context_id, if create_context() has been called."""
        return self._context_id

    async def __aenter__(self) -> "AsyncTtsSocketClient":
        url = f"{self._ws_base}/ws/tts?apiKey={self._api_key}"
        self._ws = await websockets.connect(url)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    def _require_ws(self) -> WebSocketClientProtocol:
        if self._ws is None:
            raise ApiError(body="WebSocket not connected. Use 'async with client.sixty_db.tts.websocket() as ws:'.")
        return self._ws

    async def __aiter__(self) -> typing.AsyncIterator[SixtyDbWsEvent]:
        ws = self._require_ws()
        async for raw in ws:
            if isinstance(raw, bytes):
                # 60db sends only JSON text frames; ignore unexpected binary.
                continue
            yield SixtyDbWsEvent.model_validate(json.loads(raw))

    async def recv(self) -> SixtyDbWsEvent:
        """Receive a single event from the server."""
        ws = self._require_ws()
        raw = await ws.recv()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return SixtyDbWsEvent.model_validate(json.loads(raw))

    async def _send(self, payload: typing.Dict[str, typing.Any]) -> None:
        ws = self._require_ws()
        await ws.send(json.dumps(payload))

    async def create_context(
        self,
        *,
        voice_id: str,
        context_id: typing.Optional[str] = None,
        audio_encoding: typing.Optional[str] = None,
        sample_rate_hertz: typing.Optional[int] = None,
        speed: typing.Optional[float] = None,
        stability: typing.Optional[float] = None,
        similarity: typing.Optional[float] = None,
    ) -> str:
        """Send create_context. Returns the context_id (auto-generated if not supplied)."""
        ctx_id = context_id or str(uuid.uuid4())
        payload: typing.Dict[str, typing.Any] = {
            "context_id": ctx_id,
            "voice_id": voice_id,
        }
        audio_config: typing.Dict[str, typing.Any] = {}
        if audio_encoding is not None:
            audio_config["audio_encoding"] = audio_encoding
        if sample_rate_hertz is not None:
            audio_config["sample_rate_hertz"] = sample_rate_hertz
        if audio_config:
            payload["audio_config"] = audio_config
        if speed is not None:
            payload["speed"] = speed
        if stability is not None:
            payload["stability"] = stability
        if similarity is not None:
            payload["similarity"] = similarity
        await self._send({"create_context": payload})
        self._context_id = ctx_id
        return ctx_id

    async def send_text(self, text: str, *, context_id: typing.Optional[str] = None) -> None:
        ctx = context_id or self._context_id
        if ctx is None:
            raise ApiError(body="No active context. Call create_context() first.")
        await self._send({"send_text": {"context_id": ctx, "text": text}})

    async def flush(self, *, context_id: typing.Optional[str] = None) -> None:
        ctx = context_id or self._context_id
        if ctx is None:
            raise ApiError(body="No active context. Call create_context() first.")
        await self._send({"flush_context": {"context_id": ctx}})

    async def close_context(self, *, context_id: typing.Optional[str] = None) -> None:
        ctx = context_id or self._context_id
        if ctx is None:
            return
        await self._send({"close_context": {"context_id": ctx}})
