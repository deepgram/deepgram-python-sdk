"""
Wire-shape coverage for the Listen V2 (Flux STT) ``connect`` request.

Mirrors ``test_speak_v2_connect_wire.py`` for the STT side, which otherwise had
no automated coverage of the ``/v2/listen`` handshake. Pins:

  * the connection targets the ``/v2/listen`` path, and
  * query parameters serialize correctly — in particular the ``numerals`` param
    added in the 2026-07-20 regen (docs deepgram-docs#1020) must reach the wire
    as ``numerals=true``. ``numerals`` is a connection-time query param only (it
    is not toggleable via the ``Configure`` control message).

No network / WireMock: the public ``connect`` builds the URL and hands it to the
``websockets`` connect entrypoint, so we replace that entrypoint with a capture
shim and assert on the URL it was given. Covers the sync and async clients.

Hand-written and frozen in ``.fernignore`` — Fern only generates HTTP WireMock
wire tests, never a websocket-connect wire test, so a regen would not reproduce
this file.
"""

import urllib.parse
from unittest.mock import patch

import deepgram.listen.v2.client as listen_v2_client
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


def test_sync_connect_targets_v2_listen_and_serializes_numerals():
    capture = _CaptureConnect()
    with patch.object(listen_v2_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(api_key="test_api_key").listen.v2.connect(
            model="flux-general-en",
            numerals="true",
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v2/listen"
    assert query["model"] == ["flux-general-en"]
    # The load-bearing assertion: numerals must reach the wire as "true".
    assert query["numerals"] == ["true"]


def test_sync_connect_omits_numerals_when_absent():
    capture = _CaptureConnect()
    with patch.object(listen_v2_client.websockets_sync_client, "connect", capture):
        with DeepgramClient(api_key="test_api_key").listen.v2.connect(
            model="flux-general-en",
        ):
            pass

    _, query = _path_and_query(capture.url)
    assert "numerals" not in query


async def test_async_connect_targets_v2_listen_and_serializes_numerals():
    capture = _CaptureConnect()
    with patch.object(listen_v2_client, "websockets_client_connect", capture):
        async with AsyncDeepgramClient(api_key="test_api_key").listen.v2.connect(
            model="flux-general-en",
            numerals="true",
        ):
            pass

    path, query = _path_and_query(capture.url)
    assert path == "/v2/listen"
    assert query["model"] == ["flux-general-en"]
    assert query["numerals"] == ["true"]
