"""Regression coverage for rejected WebSocket handshakes.

When the server rejects the opening handshake (HTTP 401 for bad credentials,
429 for a rate limit, ...), every ``connect()`` must raise ``ApiError`` with the
HTTP status code. ``websockets`` has two exception classes for this:

* the legacy asyncio client raises ``InvalidStatusCode`` (``exc.status_code``)
* ``websockets.sync.client`` raises ``InvalidStatus`` (``exc.response.status_code``)

The async clients use the first and the sync clients use the second, so
``core/websocket_compat.py`` must match both. These tests start a real local
``websockets`` server that rejects the handshake. They drive the real client
libraries instead of a patched ``connect``, because a patched ``connect`` can
only raise the class that the test itself selects.
"""

import contextlib
import http
import threading
import typing

import pytest
from websockets.exceptions import InvalidStatus
from websockets.sync.server import serve

from deepgram import AsyncDeepgramClient, DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.websocket_compat import InvalidWebSocketStatus, get_status_code
from deepgram.environment import DeepgramClientEnvironment

# (leaf client path, connect kwargs) for every generated WebSocket surface.
WS_ENDPOINTS: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]] = [
    ("listen.v1", {"model": "nova-3"}),
    ("listen.v2", {"model": "flux-general-en"}),
    ("speak.v1", {}),
    ("speak.v2", {"model": "flux-alexis-en"}),
    ("agent.v1", {}),
]
_WS_IDS = [endpoint[0] for endpoint in WS_ENDPOINTS]
_STATUSES = [401, 429]


@contextlib.contextmanager
def _rejecting_server(status: int) -> typing.Iterator[DeepgramClientEnvironment]:
    """Run a local server that answers every handshake with ``status``."""

    def _reject(connection: typing.Any, request: typing.Any) -> typing.Any:
        return connection.protocol.reject(http.HTTPStatus(status), "rejected\n")

    def _handler(connection: typing.Any) -> None:  # pragma: no cover - never reached
        connection.close()

    server = serve(_handler, "127.0.0.1", 0, process_request=_reject)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.socket.getsockname()[1]
        yield DeepgramClientEnvironment(
            base=f"http://127.0.0.1:{port}",
            production=f"ws://127.0.0.1:{port}",
            agent=f"ws://127.0.0.1:{port}",
            agent_rest=f"http://127.0.0.1:{port}",
        )
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _resolve(client: typing.Any, dotted_path: str) -> typing.Any:
    obj = client
    for part in dotted_path.split("."):
        obj = getattr(obj, part)
    return obj


@pytest.mark.parametrize("status", _STATUSES)
@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
def test_sync_connect_maps_rejected_handshake_to_api_error(
    leaf: str, kwargs: typing.Dict[str, typing.Any], status: int
) -> None:
    with _rejecting_server(status) as environment:
        client = DeepgramClient(api_key="test_api_key", environment=environment)

        with pytest.raises(ApiError) as high_level:
            with _resolve(client, leaf).connect(**kwargs):
                pass
        assert high_level.value.status_code == status

        with pytest.raises(ApiError) as raw:
            with _resolve(client, leaf).with_raw_response.connect(**kwargs):
                pass
        assert raw.value.status_code == status


@pytest.mark.parametrize("status", _STATUSES)
@pytest.mark.parametrize("leaf,kwargs", WS_ENDPOINTS, ids=_WS_IDS)
async def test_async_connect_maps_rejected_handshake_to_api_error(
    leaf: str, kwargs: typing.Dict[str, typing.Any], status: int
) -> None:
    with _rejecting_server(status) as environment:
        client = AsyncDeepgramClient(api_key="test_api_key", environment=environment)

        with pytest.raises(ApiError) as high_level:
            async with _resolve(client, leaf).connect(**kwargs):
                pass
        assert high_level.value.status_code == status

        with pytest.raises(ApiError) as raw:
            async with _resolve(client, leaf).with_raw_response.connect(**kwargs):
                pass
        assert raw.value.status_code == status


def test_invalid_websocket_status_matches_the_sync_client_exception() -> None:
    assert issubclass(InvalidStatus, InvalidWebSocketStatus)


def test_get_status_code_reads_both_exception_layouts() -> None:
    legacy = type("_Legacy", (Exception,), {})()
    legacy.status_code = 401  # type: ignore[attr-defined]

    current = type("_Current", (Exception,), {})()
    current.response = type("_Response", (), {"status_code": 429})()  # type: ignore[attr-defined]

    assert get_status_code(legacy) == 401
    assert get_status_code(current) == 429
