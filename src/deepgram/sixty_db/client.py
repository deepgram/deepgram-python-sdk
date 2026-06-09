# Top-level 60db sub-client. Holds the 60db API key + httpx client and lazily
# exposes namespaced surfaces (currently just .tts).

from __future__ import annotations

import typing

import httpx

if typing.TYPE_CHECKING:
    from .tts.client import AsyncTtsClient, TtsClient


class SixtyDbClient:
    """Synchronous 60db client. Reached via DeepgramClient.sixty_db."""

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
        self._tts: typing.Optional[TtsClient] = None

    @property
    def tts(self):
        if self._tts is None:
            from .tts.client import TtsClient  # noqa: E402

            self._tts = TtsClient(
                api_key=self._api_key,
                httpx_client=self._httpx_client,
                timeout=self._timeout,
            )
        return self._tts


class AsyncSixtyDbClient:
    """Async 60db client. Reached via AsyncDeepgramClient.sixty_db."""

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
        self._tts: typing.Optional[AsyncTtsClient] = None

    @property
    def tts(self):
        if self._tts is None:
            from .tts.client import AsyncTtsClient  # noqa: E402

            self._tts = AsyncTtsClient(
                api_key=self._api_key,
                httpx_client=self._httpx_client,
                timeout=self._timeout,
            )
        return self._tts
