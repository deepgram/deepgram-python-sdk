# 60db TTS client. Three surfaces:
#  - synthesize(): one-shot REST POST /tts-synthesize -> SixtyDbSynthesizeResponse
#  - stream():     NDJSON stream POST /tts-stream -> Iterator[SixtyDbStreamChunk]
#  - websocket():  async WS context manager (delegates to socket_client.py)
#
# Auth: Authorization: Bearer <api_key> (REST), apiKey query param (WS).
# The api_key is supplied by the parent SixtyDbClient (which got it from
# DeepgramClient(sixty_db_api_key=...)).

from __future__ import annotations

import json
import typing

import httpx

from ...core.api_error import ApiError
from ...types.sixty_db_stream_chunk import SixtyDbStreamChunk
from ...types.sixty_db_synthesize_response import SixtyDbSynthesizeResponse

if typing.TYPE_CHECKING:
    from .socket_client import AsyncTtsSocketClient

_REST_BASE = "https://api.60db.ai"
_WS_BASE = "wss://api.60db.ai"

# Optional REST args shared by synthesize() and stream(). Centralised so we
# can keep both call sites in sync without copy-paste drift.
_OPTIONAL_REST_FIELDS = ("voice_id", "voice", "enhance", "speed", "stability", "similarity", "output_format")


def _build_body(text: str, **opts: typing.Any) -> typing.Dict[str, typing.Any]:
    body: typing.Dict[str, typing.Any] = {"text": text}
    for k in _OPTIONAL_REST_FIELDS:
        v = opts.get(k)
        if v is not None:
            body[k] = v
    return body


def _auth_headers(api_key: typing.Optional[str]) -> typing.Dict[str, str]:
    if not api_key:
        raise ApiError(
            body=(
                "60db API key missing. Pass sixty_db_api_key= when constructing "
                "DeepgramClient/AsyncDeepgramClient."
            )
        )
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


class TtsClient:
    """Synchronous 60db TTS client."""

    def __init__(
        self,
        *,
        api_key: typing.Optional[str],
        httpx_client: httpx.Client,
        timeout: typing.Optional[float] = None,
    ):
        self._api_key = api_key
        self._httpx_client = httpx_client
        self._timeout = timeout

    def synthesize(
        self,
        *,
        text: str,
        voice_id: typing.Optional[str] = None,
        voice: typing.Optional[str] = None,
        enhance: typing.Optional[bool] = None,
        speed: typing.Optional[float] = None,
        stability: typing.Optional[float] = None,
        similarity: typing.Optional[float] = None,
        output_format: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
    ) -> SixtyDbSynthesizeResponse:
        """POST /tts-synthesize. Returns full audio in one base64-encoded blob."""
        body = _build_body(
            text=text,
            voice_id=voice_id,
            voice=voice,
            enhance=enhance,
            speed=speed,
            stability=stability,
            similarity=similarity,
            output_format=output_format,
        )
        resp = self._httpx_client.post(
            f"{_REST_BASE}/tts-synthesize",
            json=body,
            headers=_auth_headers(self._api_key),
            timeout=timeout if timeout is not None else self._timeout,
        )
        if resp.status_code >= 400:
            raise ApiError(status_code=resp.status_code, body=resp.text)
        return SixtyDbSynthesizeResponse.model_validate(resp.json())

    def stream(
        self,
        *,
        text: str,
        voice_id: typing.Optional[str] = None,
        enhance: typing.Optional[bool] = None,
        speed: typing.Optional[float] = None,
        stability: typing.Optional[float] = None,
        similarity: typing.Optional[float] = None,
        timeout: typing.Optional[float] = None,
    ) -> typing.Iterator[SixtyDbStreamChunk]:
        """POST /tts-stream. Yields one parsed SixtyDbStreamChunk per NDJSON line.

        Iteration ends when the server emits {"type": "complete"} or closes the
        connection. Error chunks are yielded as-is; callers decide whether to
        raise or recover.
        """
        body = _build_body(
            text=text,
            voice_id=voice_id,
            enhance=enhance,
            speed=speed,
            stability=stability,
            similarity=similarity,
        )
        with self._httpx_client.stream(
            "POST",
            f"{_REST_BASE}/tts-stream",
            json=body,
            headers=_auth_headers(self._api_key),
            timeout=timeout if timeout is not None else self._timeout,
        ) as resp:
            if resp.status_code >= 400:
                raise ApiError(status_code=resp.status_code, body=resp.read().decode("utf-8", errors="replace"))
            for line in resp.iter_lines():
                if not line:
                    continue
                yield SixtyDbStreamChunk.model_validate(json.loads(line))


class AsyncTtsClient:
    """Async 60db TTS client. REST mirrors the sync client; websocket() opens
    a long-lived bidirectional session."""

    def __init__(
        self,
        *,
        api_key: typing.Optional[str],
        httpx_client: httpx.AsyncClient,
        timeout: typing.Optional[float] = None,
    ):
        self._api_key = api_key
        self._httpx_client = httpx_client
        self._timeout = timeout

    async def synthesize(
        self,
        *,
        text: str,
        voice_id: typing.Optional[str] = None,
        voice: typing.Optional[str] = None,
        enhance: typing.Optional[bool] = None,
        speed: typing.Optional[float] = None,
        stability: typing.Optional[float] = None,
        similarity: typing.Optional[float] = None,
        output_format: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
    ) -> SixtyDbSynthesizeResponse:
        body = _build_body(
            text=text,
            voice_id=voice_id,
            voice=voice,
            enhance=enhance,
            speed=speed,
            stability=stability,
            similarity=similarity,
            output_format=output_format,
        )
        resp = await self._httpx_client.post(
            f"{_REST_BASE}/tts-synthesize",
            json=body,
            headers=_auth_headers(self._api_key),
            timeout=timeout if timeout is not None else self._timeout,
        )
        if resp.status_code >= 400:
            raise ApiError(status_code=resp.status_code, body=resp.text)
        return SixtyDbSynthesizeResponse.model_validate(resp.json())

    async def stream(
        self,
        *,
        text: str,
        voice_id: typing.Optional[str] = None,
        enhance: typing.Optional[bool] = None,
        speed: typing.Optional[float] = None,
        stability: typing.Optional[float] = None,
        similarity: typing.Optional[float] = None,
        timeout: typing.Optional[float] = None,
    ) -> typing.AsyncIterator[SixtyDbStreamChunk]:
        body = _build_body(
            text=text,
            voice_id=voice_id,
            enhance=enhance,
            speed=speed,
            stability=stability,
            similarity=similarity,
        )
        async with self._httpx_client.stream(
            "POST",
            f"{_REST_BASE}/tts-stream",
            json=body,
            headers=_auth_headers(self._api_key),
            timeout=timeout if timeout is not None else self._timeout,
        ) as resp:
            if resp.status_code >= 400:
                body_text = (await resp.aread()).decode("utf-8", errors="replace")
                raise ApiError(status_code=resp.status_code, body=body_text)
            async for line in resp.aiter_lines():
                if not line:
                    continue
                yield SixtyDbStreamChunk.model_validate(json.loads(line))

    def websocket(self) -> "AsyncTtsSocketClient":
        """Open an async WebSocket session against wss://api.60db.ai/ws/tts.

        Returned object is an async context manager:

            async with client.sixty_db.tts.websocket() as ws:
                await ws.create_context(voice_id="...")
                await ws.send_text("Hello")
                await ws.flush()
                async for event in ws:
                    ...
        """
        from .socket_client import AsyncTtsSocketClient  # noqa: E402

        return AsyncTtsSocketClient(api_key=self._api_key, ws_base=_WS_BASE)
