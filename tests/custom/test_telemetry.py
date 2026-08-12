"""Tests for the hand-written opt-out telemetry module.

Covers the SDK-specific risk areas:
- opt-out resolution (env kill-switch, flag, no-DSN inertness),
- PII/secret scrubbing,
- library isolation (a custom handler fully replaces Sentry),
- per-client isolation (one client's opt-out or handler never leaks to another).

Most of these do not require ``sentry-sdk`` to be installed; the no-DSN default
keeps Sentry inert, so the module no-ops cleanly on the core paths.
"""

import httpx
import pytest

from deepgram.telemetry import client as telemetry
from deepgram.telemetry import http_hooks
from deepgram.telemetry.client import TelemetrySink
from deepgram.telemetry.scrub import scrub_event


@pytest.fixture(autouse=True)
def _reset():
    telemetry._reset_for_tests()
    yield
    telemetry._reset_for_tests()


class _RecordingSink:
    """Minimal sink double that records capture_message calls."""

    def __init__(self):
        self.messages = []

    def capture_message(self, message, **kwargs):
        self.messages.append((message, kwargs))


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


class TestEnvironmentTag:
    def test_environment_defaults_to_unset(self, monkeypatch):
        # Never hard-code "production": the SDK runs in customer dev/CI/staging.
        monkeypatch.delenv(telemetry.ENVIRONMENT_ENV_VAR, raising=False)
        assert telemetry._resolve_environment() is None

    def test_environment_honours_override(self, monkeypatch):
        monkeypatch.setenv(telemetry.ENVIRONMENT_ENV_VAR, "staging")
        assert telemetry._resolve_environment() == "staging"


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

    def test_redacts_home_dir_username_from_stack_frames(self):
        event = {
            "exception": {
                "values": [
                    {
                        "stacktrace": {
                            "frames": [
                                {
                                    "abs_path": "/Users/jane.doe/src/acme/main.py",
                                    "filename": "acme/main.py",
                                },
                                {"abs_path": "/home/bob/.venv/lib/deepgram/client.py"},
                                {"abs_path": "C:\\Users\\jane\\app.py"},
                                {"abs_path": "/opt/app/no_home_here.py"},
                            ]
                        }
                    }
                ]
            },
            "threads": {
                "values": [
                    {"stacktrace": {"frames": [{"abs_path": "/Users/carol/t.py"}]}}
                ]
            },
        }
        out = scrub_event(event, {})
        frames = out["exception"]["values"][0]["stacktrace"]["frames"]
        assert frames[0]["abs_path"] == "/Users/<redacted>/src/acme/main.py"
        assert frames[0]["filename"] == "acme/main.py"  # no home segment, untouched
        assert frames[1]["abs_path"] == "/home/<redacted>/.venv/lib/deepgram/client.py"
        assert frames[2]["abs_path"] == "C:\\Users\\<redacted>\\app.py"
        assert frames[3]["abs_path"] == "/opt/app/no_home_here.py"  # unchanged
        thread_frame = out["threads"]["values"][0]["stacktrace"]["frames"][0]
        assert thread_frame["abs_path"] == "/Users/<redacted>/t.py"


class TestIsolation:
    def test_custom_handler_replaces_sentry(self):
        received = []

        def handler(exc, tags):
            received.append((exc, tags))

        sink = telemetry.init_telemetry(
            opt_out=False, handler=handler, version="9.9.9"
        )
        assert sink is not None

        err = ValueError("boom")
        sink.capture_exception(err, tags={"request_id": "r1"})

        assert len(received) == 1
        assert received[0][0] is err
        assert received[0][1]["request_id"] == "r1"

    def test_no_sink_is_safe(self):
        # No DSN, no handler: init returns None and an empty sink no-ops.
        assert telemetry.init_telemetry(opt_out=False, version="9.9.9") is None
        TelemetrySink().capture_exception(ValueError("boom"))  # must not raise

    def test_handler_errors_are_swallowed(self):
        def bad_handler(exc, tags):
            raise RuntimeError("handler blew up")

        sink = telemetry.init_telemetry(
            opt_out=False, handler=bad_handler, version="9.9.9"
        )
        assert sink is not None
        sink.capture_exception(ValueError("boom"))  # must not propagate


class TestPerClientIsolation:
    """Regression tests for the module-global state bugs.

    Historically ``init_telemetry`` short-circuited on a module-global
    ``_initialized`` flag and stored the handler in a module global, so a
    second client's opt-out was ignored and one client's handler caught every
    client's events. Sinks are now per-client, so neither can happen.
    """

    def test_opt_out_is_honoured_per_client_regardless_of_order(
        self, monkeypatch
    ):
        monkeypatch.setenv(telemetry.DSN_ENV_VAR, "https://k@o1.ingest.us.sentry.io/1")
        # Avoid needing sentry-sdk installed: stub the shared client builder.
        monkeypatch.setattr(
            telemetry, "_get_or_build_client", lambda dsn, version: object()
        )

        # An opted-in client arms; a later opted-out client stays inert...
        armed_first = telemetry.init_telemetry(opt_out=False, version="1.0.0")
        opted_out_second = telemetry.init_telemetry(opt_out=True, version="1.0.0")
        assert armed_first is not None
        assert opted_out_second is None

        # ...and the reverse order behaves the same (no sticky init state).
        opted_out_first = telemetry.init_telemetry(opt_out=True, version="1.0.0")
        armed_second = telemetry.init_telemetry(opt_out=False, version="1.0.0")
        assert opted_out_first is None
        assert armed_second is not None

    def test_handler_does_not_leak_across_clients(self):
        received_a, received_b = [], []
        sink_a = telemetry.init_telemetry(
            opt_out=False, handler=lambda exc, tags: received_a.append(exc), version="1"
        )
        sink_b = telemetry.init_telemetry(
            opt_out=False, handler=lambda exc, tags: received_b.append(exc), version="1"
        )
        assert sink_a is not None and sink_b is not None

        err = ValueError("only for B")
        sink_b.capture_exception(err)

        assert received_b == [err]
        assert received_a == []  # A's handler must not see B's events


class TestResponseHook:
    def _response(self, status, headers=None):
        request = httpx.Request("GET", "https://api.deepgram.com/v1/listen?model=nova")
        return httpx.Response(status, headers=headers or {}, request=request)

    def test_5xx_captured_with_request_id_and_no_query(self):
        sink = _RecordingSink()
        record = http_hooks._make_recorder(sink, "sess-1")
        record(self._response(503, {"dg-request-id": "req-42"}))

        assert len(sink.messages) == 1
        tags = sink.messages[0][1]["tags"]
        assert tags["http.status"] == "503"
        assert tags["request_id"] == "req-42"
        assert tags["session_id"] == "sess-1"
        assert tags["http.path"] == "/v1/listen"  # query stripped

    def test_4xx_not_captured(self):
        sink = _RecordingSink()
        http_hooks._make_recorder(sink, "s")(self._response(401))
        assert sink.messages == []

    def test_install_appends_hook_to_httpx_client(self):
        raw = httpx.Client()
        wrapper = type("W", (), {"httpx_client": type("H", (), {"httpx_client": raw})()})()
        try:
            assert http_hooks.install_response_capture(_RecordingSink(), wrapper, "s") is True
            assert len(raw.event_hooks.get("response", [])) == 1
        finally:
            raw.close()

    def test_install_is_idempotent(self):
        # A second install must not stack a duplicate response hook.
        raw = httpx.Client()
        wrapper = type("W", (), {"httpx_client": type("H", (), {"httpx_client": raw})()})()
        try:
            assert http_hooks.install_response_capture(_RecordingSink(), wrapper, "s") is True
            assert http_hooks.install_response_capture(_RecordingSink(), wrapper, "s") is True
            assert len(raw.event_hooks.get("response", [])) == 1
        finally:
            raw.close()

    def test_install_is_safe_when_no_client(self):
        wrapper = type("W", (), {"httpx_client": None})()
        assert http_hooks.install_response_capture(_RecordingSink(), wrapper, "s") is False


class TestSentryIsolation:
    """Requires sentry-sdk; validates we never touch the host app's global Sentry."""

    def test_isolated_client_leaves_global_untouched(self, monkeypatch):
        sentry_sdk = pytest.importorskip("sentry_sdk")
        monkeypatch.setenv(
            telemetry.DSN_ENV_VAR, "https://public@o0.ingest.us.sentry.io/1"
        )

        sink = telemetry.init_telemetry(opt_out=False, version="7.5.1")
        assert sink is not None
        # Our private client is configured and active (sends events)...
        assert sink._client is not None
        assert sink._client.is_active() is True
        # ...but the process-global Sentry client is never configured by us.
        assert sentry_sdk.get_client().dsn is None
        # And capturing through the isolated client must not raise.
        sink.capture_exception(ValueError("boom"), tags={"request_id": "r1"})
