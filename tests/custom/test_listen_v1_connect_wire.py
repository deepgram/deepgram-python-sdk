"""Wire-shape coverage for the Listen V1 multilingual ``connect`` request."""

import urllib.parse
from unittest.mock import patch

import deepgram.listen.v1.client as listen_v1_client
from deepgram import AsyncDeepgramClient, DeepgramClient


class _CaptureConnect:
    """Records the WebSocket URL while acting as sync and async context managers."""

    def __init__(self) -> None:
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


def _path_and_query(url):
    parts = urllib.parse.urlsplit(url)
    return parts.path, urllib.parse.parse_qs(parts.query)


def test_sync_connect_serializes_repeated_language_hints() -> None:
    capture = _CaptureConnect()
    with patch.object(listen_v1_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(api_key="test_api_key").listen.v1.connect(
            model="nova-3",
            language="multi",
            language_hint=["en", "es"],
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v1/listen"
    assert query["model"] == ["nova-3"]
    assert query["language"] == ["multi"]
    assert query["language_hint"] == ["en", "es"]


async def test_async_connect_serializes_repeated_language_hints() -> None:
    capture = _CaptureConnect()
    with patch.object(listen_v1_client, "websockets_client_connect", capture):
        async with AsyncDeepgramClient(api_key="test_api_key").listen.v1.connect(
            model="nova-3",
            language="multi",
            language_hint=["en", "es"],
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v1/listen"
    assert query["model"] == ["nova-3"]
    assert query["language"] == ["multi"]
    assert query["language_hint"] == ["en", "es"]
