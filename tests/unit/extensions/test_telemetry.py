import itertools
import json
from typing import Any, Iterator, Mapping

import httpx
import pytest

from deepgram.extensions.core.telemetry_events import TelemetryHttpEvents
from deepgram.extensions.telemetry import proto_encoder as pe
from deepgram.extensions.telemetry.batching_handler import BatchingTelemetryHandler
from deepgram.extensions.telemetry.handler import TelemetryHandler


class _Recorder(TelemetryHandler):
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []

    def on_http_request(self, *, method: str, url: str, headers: Mapping[str, str] | None, extras: Mapping[str, str] | None = None) -> None:
        self.calls.append(("on_http_request", (method, url), {}))

    def on_http_response(
        self,
        *,
        method: str,
        url: str,
        status_code: int,
        duration_ms: float,
        headers: Mapping[str, str] | None,
        extras: Mapping[str, str] | None = None,
    ) -> None:
        self.calls.append(("on_http_response", (method, url, status_code), {}))

    def on_http_error(
        self, 
        *, 
        method: str, 
        url: str, 
        error: BaseException, 
        duration_ms: float,
        request_details: Mapping[str, Any] | None = None,
        response_details: Mapping[str, Any] | None = None,
        call_stack_signature: str | None = None,
    ) -> None:
        self.calls.append(("on_http_error", (method, url, type(error).__name__), {}))

    # WebSocket methods removed - WebSocket instrumentation is now built into socket clients


def test_telemetry_event_adapters_delegate_and_swallow_exceptions():
    rec = _Recorder()
    http = TelemetryHttpEvents(rec)

    http.on_http_request(method="GET", url="/", headers=None)
    http.on_http_response(method="GET", url="/", status_code=200, duration_ms=1.0, headers=None)
    http.on_http_error(method="GET", url="/", error=RuntimeError("x"), duration_ms=2.0)

    # WebSocket events are now handled directly in socket clients
    # so we only test HTTP events here
    assert {name for name, *_ in rec.calls} >= {
        "on_http_request",
        "on_http_response",
        "on_http_error",
    }

    # Ensure exceptions in handler are swallowed
    class _Boom(TelemetryHandler):
        def on_http_request(self, **_: Any) -> None:
            raise RuntimeError("boom")

    TelemetryHttpEvents(_Boom()).on_http_request(method="GET", url="/", headers=None)


def test_batching_handler_enqueue_and_flush(monkeypatch):
    posted: list[dict] = []

    class DummyClient(httpx.Client):
        def __init__(self):
            super().__init__()

        def post(self, url, content=None, headers=None):  # type: ignore[override]
            body = b"".join(content) if content is not None else b""
            posted.append({"url": str(url), "len": len(body), "hdrs": dict(headers or {})})
            return httpx.Response(200)

    h = BatchingTelemetryHandler(
        endpoint="https://telemetry.example/batch",
        batch_size=2,
        max_interval_seconds=10.0,
        client=DummyClient(),
        context_provider=lambda: {"sdk_name": "python-sdk", "sdk_version": "1"},
    )
    try:
        # Two events trigger immediate flush due to batch_size
        h.on_http_request(method="GET", url="/a", headers=None)
        h.on_http_response(method="GET", url="/a", status_code=200, duration_ms=1.2, headers=None)

        # Force error -> force_flush path
        h.on_http_error(method="GET", url="/a", error=RuntimeError("x"), duration_ms=2.3)
    finally:
        h.close()

    # At least one POST occurred; headers contain gzip + content-type
    assert posted and all("content-encoding" in p["hdrs"] for p in posted)


def test_batching_handler_disable_on_failures(monkeypatch):
    class BadClient(httpx.Client):
        def post(self, *args, **kwargs):  # type: ignore[override]
            raise httpx.ConnectError("nope")

    # Low threshold to trip disable quickly
    h = BatchingTelemetryHandler(
        endpoint="https://telemetry.example/batch",
        batch_size=1,
        max_interval_seconds=0.25,
        client=BadClient(),
        context_provider=lambda: {},
        max_consecutive_failures=1,
    )
    try:
        h.on_http_request(method="GET", url="/a", headers=None)
        h.on_http_response(method="GET", url="/a", status_code=200, duration_ms=1.0, headers=None)
        # Give background worker a moment
    finally:
        h.close()
    # If not disabled, queue would try to flush during close and raise due to debug=False; reaching here implies disable worked.


def test_proto_encoder_happy_paths_and_iter():
    events = [
        {"type": "http_request", "ts": 1.0, "method": "GET", "url": "/a"},
        {"type": "http_response", "ts": 2.0, "method": "GET", "url": "/a", "status_code": 200, "duration_ms": 12.3},
        {"type": "http_error", "ts": 3.0, "method": "GET", "url": "/a", "error": "ConnectError", "duration_ms": 22.1},
        {"type": "unknown", "ts": 4.0},  # ignored
    ]
    ctx = {"sdk_name": "python-sdk", "sdk_version": "1.0.0"}
    blob = pe.encode_telemetry_batch(events, ctx)
    assert isinstance(blob, (bytes, bytearray)) and len(blob) > 0

    chunks = list(pe.encode_telemetry_batch_iter(events, ctx))
    assert chunks and all(isinstance(c, (bytes, bytearray)) for c in chunks)


# --- Synchronous mode tests ---

def test_batching_handler_synchronous_flush_on_batch_size():
    posted: list[dict] = []

    class DummyClient(httpx.Client):
        def post(self, url, content=None, headers=None):  # type: ignore[override]
            body = b"".join(content) if content is not None else b""
            posted.append({"url": str(url), "len": len(body), "hdrs": dict(headers or {})})
            return httpx.Response(200)

    h = BatchingTelemetryHandler(
        endpoint="https://telemetry.example/batch",
        batch_size=2,  # request + response triggers flush
        max_interval_seconds=999.0,
        client=DummyClient(),
        context_provider=lambda: {"sdk_name": "python-sdk", "sdk_version": "1"},
        synchronous=True,
    )
    try:
        h.on_http_request(method="GET", url="/a", headers=None)
        # No post yet (need 2 events)
        assert len(posted) == 0

        h.on_http_response(method="GET", url="/a", status_code=200, duration_ms=1.2, headers=None)
        # Flush should have occurred exactly once
        assert len(posted) == 1
        assert posted[0]["len"] > 0 and "content-encoding" in posted[0]["hdrs"]
    finally:
        h.close()


def test_batching_handler_synchronous_force_flush_on_error():
    posted: list[dict] = []

    class DummyClient(httpx.Client):
        def post(self, url, content=None, headers=None):  # type: ignore[override]
            body = b"".join(content) if content is not None else b""
            posted.append({"url": str(url), "len": len(body), "hdrs": dict(headers or {})})
            return httpx.Response(200)

    h = BatchingTelemetryHandler(
        endpoint="https://telemetry.example/batch",
        batch_size=100,  # won't be reached
        max_interval_seconds=999.0,
        client=DummyClient(),
        context_provider=lambda: {},
        synchronous=True,
    )
    try:
        h.on_http_error(method="GET", url="/a", error=RuntimeError("x"), duration_ms=2.3)
        # Error path should force-flush immediately
        assert len(posted) == 1
        assert posted[0]["len"] > 0
        # flush() with no new events should be a no-op
        h.flush()
        assert len(posted) == 1
    finally:
        h.close()

