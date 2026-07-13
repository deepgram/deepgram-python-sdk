"""
Wire-shape coverage for the Speak V2 (Flux TTS) ``connect`` request.

The *outbound message* JSON is pinned in ``test_speak_v2_socket.py``; this pins
the *request* side of the handshake, which otherwise had no automated coverage:

  * the connection targets the ``/v2/speak`` path, and
  * query parameters serialize correctly — in particular a Python ``bool``
    ``mip_opt_out=True`` must reach the wire as lowercase ``true`` (not
    ``"True"``). That coercion is the whole job of the frozen
    ``core/query_encoder.py`` patch, so this test doubles as its wire-level guard.

No network / WireMock: the public ``connect`` builds the URL and hands it to the
``websockets`` connect entrypoint, so we replace that entrypoint with a capture
shim and assert on the URL it was given. Covers the sync and async clients.

Hand-written and frozen in ``.fernignore`` — Fern only generates HTTP WireMock
wire tests, never a websocket-connect wire test, so a regen would not reproduce
this file.
"""

import urllib.parse
from unittest.mock import patch

import deepgram.speak.v2.client as speak_v2_client
from deepgram import AsyncDeepgramClient, DeepgramClient


class _CaptureConnect:
    """Stands in for ``websockets(.sync).connect``: records the URL it is called
    with, then behaves as both a sync and async context manager yielding a
    throwaway protocol object."""

    def __init__(self):
        self.url = None
        self.kwargs = None

    def __call__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs
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


def test_sync_connect_targets_v2_speak_and_serializes_query():
    capture = _CaptureConnect()
    with patch.object(speak_v2_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(api_key="test_api_key").speak.v2.connect(
            model="flux-alexis-en",
            encoding="linear16",
            sample_rate="24000",
            mip_opt_out=True,
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v2/speak"
    assert query["model"] == ["flux-alexis-en"]
    assert query["encoding"] == ["linear16"]
    assert query["sample_rate"] == ["24000"]
    # The load-bearing assertion: Python True must serialize as "true", not "True".
    assert query["mip_opt_out"] == ["true"]


async def test_async_connect_targets_v2_speak_and_serializes_query():
    capture = _CaptureConnect()
    with patch.object(speak_v2_client, "websockets_client_connect", capture):
        async with AsyncDeepgramClient(api_key="test_api_key").speak.v2.connect(
            model="flux-alexis-en",
            mip_opt_out=True,
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v2/speak"
    assert query["model"] == ["flux-alexis-en"]
    assert query["mip_opt_out"] == ["true"]
