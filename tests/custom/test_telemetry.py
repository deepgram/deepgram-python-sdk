"""Tests for the hand-written opt-out telemetry module.

Covers the three SDK-specific risk areas:
- opt-out resolution (env kill-switch, flag, no-DSN inertness),
- PII/secret scrubbing,
- library isolation (a custom handler fully replaces Sentry).

These do not require ``sentry-sdk`` to be installed; the no-DSN default keeps
Sentry inert, so the module no-ops cleanly on the core paths.
"""

import httpx
import pytest

from deepgram.telemetry import client as telemetry
from deepgram.telemetry import http_hooks
from deepgram.telemetry.scrub import scrub_event


@pytest.fixture(autouse=True)
def _reset():
    telemetry._reset_for_tests()
    yield
    telemetry._reset_for_tests()


class TestOptOutResolution:
    def test_disabled_by_default_without_dsn(self):
        # No DSN embedded/supplied -> inert even when not opted out.
        assert telemetry.is_enabled(opt_out=False) is False

    def test_opt_out_flag_disables(self, monkeypatch):
        monkeypatch.setenv(telemetry.DSN_ENV_VAR, "https://k@o1.ingest.us.sentry.io/1")
        assert telemetry.is_enabled(opt_out=True) is False

    def test_env_kill_switch_wins(self, monkeypatch):
        monkeypatch.setenv(telemetry.DSN_ENV_VAR, "https://k@o1.ingest.us.sentry.io/1")
        monkeypatch.setenv(telemetry.DISABLE_ENV_VAR, "1")
        assert telemetry.is_enabled(opt_out=False) is False

    def test_enabled_with_real_dsn_and_no_opt_out(self, monkeypatch):
        monkeypatch.setenv(telemetry.DSN_ENV_VAR, "https://k@o1.ingest.us.sentry.io/1")
        assert telemetry.is_enabled(opt_out=False) is True

    def test_placeholder_dsn_is_not_real(self, monkeypatch):
        monkeypatch.setenv(
            telemetry.DSN_ENV_VAR, "https://PLACEHOLDER@x.ingest.us.sentry.io/0"
        )
        assert telemetry.is_enabled(opt_out=False) is False


class TestScrubbing:
    def test_strips_secrets_and_pii(self):
        event = {
            "request": {
                "headers": {"Authorization": "Bearer secret", "X-Trace": "keep"},
                "data": "raw-audio-bytes",
                "query_string": "key=abc123",
                "cookies": {"sid": "x"},
            },
            "user": {
                "email": "a@b.com",
                "id": "u1",
                "ip_address": "1.2.3.4",
                "geo": {"country_code": "GB"},
            },
            "server_name": "customers-laptop",
            "extra": {"payload": "transcript"},
        }
        out = scrub_event(event, {})
        assert out is not None
        req = out["request"]
        assert req["headers"]["Authorization"] == "[Filtered]"
        assert req["headers"]["X-Trace"] == "keep"
        assert req["data"] == "[Filtered]"
        assert req["query_string"] == "[Filtered]"
        assert req["cookies"] == {}
        assert out["user"] == {}
        assert "server_name" not in out
        assert "extra" not in out

    def test_never_raises_on_malformed_event(self):
        # Non-dict headers must not blow up the scrubber.
        assert scrub_event({"request": {"headers": "oops"}}, {}) is not None


class TestIsolation:
    def test_custom_handler_replaces_sentry(self):
        received = []

        def handler(exc, tags):
            received.append((exc, tags))

        assert (
            telemetry.init_telemetry(opt_out=False, handler=handler, version="9.9.9")
            is True
        )

        err = ValueError("boom")
        telemetry.capture_exception(err, tags={"request_id": "r1"})

        assert len(received) == 1
        assert received[0][0] is err
        assert received[0][1]["request_id"] == "r1"

    def test_no_sink_is_safe(self):
        # No DSN, no handler: init returns False and capture is a silent no-op.
        assert telemetry.init_telemetry(opt_out=False, version="9.9.9") is False
        telemetry.capture_exception(ValueError("boom"))  # must not raise

    def test_handler_errors_are_swallowed(self):
        def bad_handler(exc, tags):
            raise RuntimeError("handler blew up")

        telemetry.init_telemetry(opt_out=False, handler=bad_handler, version="9.9.9")
        telemetry.capture_exception(ValueError("boom"))  # must not propagate


class TestResponseHook:
    def _response(self, status, headers=None):
        request = httpx.Request("GET", "https://api.deepgram.com/v1/listen?model=nova")
        return httpx.Response(status, headers=headers or {}, request=request)

    def test_5xx_captured_with_request_id_and_no_query(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            http_hooks, "capture_message", lambda msg, **kw: calls.append((msg, kw))
        )
        record = http_hooks._make_recorder("sess-1")
        record(self._response(503, {"dg-request-id": "req-42"}))

        assert len(calls) == 1
        tags = calls[0][1]["tags"]
        assert tags["http.status"] == "503"
        assert tags["request_id"] == "req-42"
        assert tags["session_id"] == "sess-1"
        assert tags["http.path"] == "/v1/listen"  # query stripped

    def test_4xx_not_captured(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            http_hooks, "capture_message", lambda msg, **kw: calls.append(msg)
        )
        http_hooks._make_recorder("s")(self._response(401))
        assert calls == []

    def test_install_appends_hook_to_httpx_client(self):
        raw = httpx.Client()
        wrapper = type("W", (), {"httpx_client": type("H", (), {"httpx_client": raw})()})()
        try:
            assert http_hooks.install_response_capture(wrapper, "sess") is True
            assert len(raw.event_hooks.get("response", [])) == 1
        finally:
            raw.close()

    def test_install_is_safe_when_no_client(self):
        wrapper = type("W", (), {"httpx_client": None})()
        assert http_hooks.install_response_capture(wrapper, "sess") is False


class TestSentryIsolation:
    """Requires sentry-sdk; validates we never touch the host app's global Sentry."""

    def test_isolated_client_leaves_global_untouched(self, monkeypatch):
        sentry_sdk = pytest.importorskip("sentry_sdk")
        monkeypatch.setenv(
            telemetry.DSN_ENV_VAR, "https://public@o0.ingest.us.sentry.io/1"
        )

        assert telemetry.init_telemetry(opt_out=False, version="7.5.1") is True
        # Our private client is configured and active (sends events)...
        assert telemetry._client is not None
        assert telemetry._client.is_active() is True
        # ...but the process-global Sentry client is never configured by us.
        assert sentry_sdk.get_client().dsn is None
        # And capturing through the isolated client must not raise.
        telemetry.capture_exception(ValueError("boom"), tags={"request_id": "r1"})
