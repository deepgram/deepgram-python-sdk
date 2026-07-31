"""Isolated, opt-out Sentry telemetry for the Deepgram Python SDK.

Design constraints specific to running inside a *library* (not the CLI, which
owns its whole process):

1. NEVER call the global ``sentry_sdk.init()``. That installs process-wide
   integrations (excepthook, atexit, logging) and hijacks the host
   application's own Sentry configuration. We instead build a private
   ``sentry_sdk.Client`` and capture events by calling ``client.capture_event``
   directly — the customer's global Sentry scope is left completely untouched.
   (A bound ``Scope`` is deliberately avoided: in sentry-sdk 2.x a manually
   constructed ``Scope`` does not treat its client as active, so
   ``Scope.capture_*`` silently no-ops. Calling the client directly is the
   reliable isolated path.)
2. Disable all default/auto integrations so we never capture the host app's
   unrelated errors.
3. Never capture local variables or request bodies (audio, keys, transcripts).

The public opt-out surface lives on ``DeepgramClient``/``AsyncDeepgramClient``
(``telemetry_opt_out=`` and ``telemetry_handler=``); this module implements
what those parameters actually do.
"""

from __future__ import annotations

import atexit
import os
import platform
import sys
from typing import Any, Callable, Dict, Optional

from .scrub import scrub_event

# Environment overrides.
#   DEEPGRAM_TELEMETRY_DISABLED=1  -> hard off, wins over everything
#   DEEPGRAM_SDK_TELEMETRY_DSN     -> supply/override the Sentry DSN
DISABLE_ENV_VAR = "DEEPGRAM_TELEMETRY_DISABLED"
DSN_ENV_VAR = "DEEPGRAM_SDK_TELEMETRY_DSN"

# No real DSN is embedded yet. Until a public data-collection policy is
# published AND product signs off on phoning home by default, telemetry stays
# inert unless a DSN is supplied via DEEPGRAM_SDK_TELEMETRY_DSN: with no
# resolvable DSN, `init_telemetry` no-ops regardless of the opt-out flag. Drop
# the real public (ingest-only) DSN here to arm it by default. See the SDK
# Observability task.
_EMBEDDED_DSN = ""

# Custom handler set by the caller (telemetry_handler=). When present it fully
# replaces Sentry: we hand it the exception and never phone home ourselves.
TelemetryHandler = Callable[[BaseException, Dict[str, str]], None]

_client: Any = None
_base_tags: Dict[str, str] = {}
_custom_handler: Optional[TelemetryHandler] = None
_initialized = False


def _resolve_dsn() -> Optional[str]:
    dsn = os.environ.get(DSN_ENV_VAR) or _EMBEDDED_DSN
    if not dsn or "PLACEHOLDER" in dsn:
        return None
    return dsn


def is_enabled(opt_out: bool) -> bool:
    """Whether Sentry phone-home should run for this client.

    Order: env kill-switch, then the caller's opt-out flag, then whether a real
    DSN is resolvable. A custom handler is considered "enabled" separately (it
    doesn't need a DSN) and is wired up in ``init_telemetry``.
    """
    if os.environ.get(DISABLE_ENV_VAR, "").lower() in {"1", "true", "yes"}:
        return False
    if opt_out:
        return False
    return _resolve_dsn() is not None


def init_telemetry(
    *,
    opt_out: bool,
    handler: Optional[TelemetryHandler] = None,
    version: str = "unknown",
) -> bool:
    """Set up telemetry for a client. Idempotent and never raises.

    Returns whether a capture sink (custom handler or Sentry client) is active.
    A custom handler always takes precedence over Sentry.
    """
    global _client, _base_tags, _custom_handler, _initialized

    if handler is not None:
        _custom_handler = handler
        return True

    if _initialized:
        return _client is not None
    _initialized = True

    if not is_enabled(opt_out):
        return False

    dsn = _resolve_dsn()

    try:
        from sentry_sdk import Client  # type: ignore[import-not-found]
    except ImportError:
        # `sentry-sdk` is an optional extra; absence just means no phone-home.
        return False

    try:
        _client = Client(
            dsn=dsn,
            release=f"deepgram-sdk@{version}",
            environment="production",
            # Library isolation: no process-wide patching, no host-app capture.
            default_integrations=False,
            auto_enabling_integrations=False,
            integrations=[],
            # Treat the SDK's own package as first-party so Sentry highlights
            # these frames and stack-trace linking (code mappings) resolves them.
            in_app_include=["deepgram"],
            # PII / payload safety.
            send_default_pii=False,
            include_local_variables=False,
            max_request_body_size="never",
            attach_stacktrace=True,
            before_send=scrub_event,
        )
        _base_tags = {
            "sdk.language": "python",
            "sdk.version": version,
            "sdk.os": platform.system().lower(),
            "sdk.arch": platform.machine().lower(),
            "sdk.python": f"{sys.version_info.major}.{sys.version_info.minor}",
        }
        atexit.register(_flush_on_exit)
    except Exception:
        _client = None
        return False

    return True


def _merge_tags(tags: Optional[Dict[str, str]]) -> Dict[str, str]:
    merged = dict(_base_tags)
    if tags:
        merged.update(tags)
    return merged


def capture_exception(
    exc: BaseException, *, tags: Optional[Dict[str, str]] = None
) -> None:
    """Report an SDK-originated exception. Best-effort; never raises.

    Only call this for errors that originate in Deepgram SDK code (API errors,
    transport failures) — never for arbitrary host-application exceptions.
    """
    if _custom_handler is not None:
        try:
            _custom_handler(exc, tags or {})
        except Exception:
            pass
        return

    if _client is None:
        return

    try:
        from sentry_sdk.utils import event_from_exception  # type: ignore[import-not-found]

        event, hint = event_from_exception(exc, client_options=_client.options)
        event["tags"] = _merge_tags(tags)
        _client.capture_event(event, hint=hint)
    except Exception:
        pass


def capture_message(
    message: str, *, level: str = "error", tags: Optional[Dict[str, str]] = None
) -> None:
    """Report a non-exception signal (e.g. an HTTP 5xx). Best-effort; never raises.

    Custom handlers are exception-oriented, so messages only go to Sentry; with
    a handler (and no Sentry client) this is a no-op.
    """
    if _client is None:
        return
    try:
        event = {"message": message, "level": level, "tags": _merge_tags(tags)}
        _client.capture_event(event)
    except Exception:
        pass


def _flush_on_exit() -> None:
    """Flush queued events before process exit (best-effort, 2s budget)."""
    try:
        if _client is not None:
            _client.flush(timeout=2.0)
    except Exception:
        pass


def _reset_for_tests() -> None:
    """Reset module state. Test-only."""
    global _client, _base_tags, _custom_handler, _initialized
    _client = None
    _base_tags = {}
    _custom_handler = None
    _initialized = False
