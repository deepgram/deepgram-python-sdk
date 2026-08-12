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

Capture is routed through a per-client :class:`TelemetrySink`, not module
globals. Each ``DeepgramClient`` / ``AsyncDeepgramClient`` owns its own sink, so
one client's opt-out never suppresses (or arms) another's, and a custom handler
set on one client never receives another client's events. The heavyweight
Sentry ``Client`` *is* shared per-DSN across sinks in a process — that is a
genuine process resource, not per-client policy.

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
#   DEEPGRAM_TELEMETRY_DISABLED=1     -> hard off, wins over everything
#   DEEPGRAM_SDK_TELEMETRY_DSN        -> supply/override the Sentry DSN
#   DEEPGRAM_TELEMETRY_ENVIRONMENT    -> tag events with a deployment environment
DISABLE_ENV_VAR = "DEEPGRAM_TELEMETRY_DISABLED"
DSN_ENV_VAR = "DEEPGRAM_SDK_TELEMETRY_DSN"
ENVIRONMENT_ENV_VAR = "DEEPGRAM_TELEMETRY_ENVIRONMENT"

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

# Process-wide resources (NOT per-client policy):
#   _client_cache: one Sentry Client per DSN, reused across sinks in a process.
#   _live_clients: every built client, for a single atexit flush.
_client_cache: Dict[str, Any] = {}
_live_clients: list = []
_flush_registered = False


def _resolve_dsn() -> Optional[str]:
    dsn = os.environ.get(DSN_ENV_VAR) or _EMBEDDED_DSN
    if not dsn or "PLACEHOLDER" in dsn:
        return None
    return dsn


def _resolve_environment() -> Optional[str]:
    """The Sentry ``environment`` tag, or ``None`` to leave it unset.

    Deliberately not hard-coded to ``"production"``: this SDK runs inside
    customer applications — dev boxes, CI, staging — so a fixed "production"
    tag mislabels every event. We honour an explicit
    ``DEEPGRAM_TELEMETRY_ENVIRONMENT`` override and otherwise assert nothing.
    """
    return os.environ.get(ENVIRONMENT_ENV_VAR) or None


def is_enabled(opt_out: bool) -> bool:
    """Whether Sentry phone-home should run for a client with this opt-out.

    Order: env kill-switch, then the caller's opt-out flag, then whether a real
    DSN is resolvable. A custom handler is considered "enabled" separately (it
    doesn't need a DSN) and is wired up in ``init_telemetry``.
    """
    if os.environ.get(DISABLE_ENV_VAR, "").lower() in {"1", "true", "yes"}:
        return False
    if opt_out:
        return False
    return _resolve_dsn() is not None


def _build_base_tags(version: str) -> Dict[str, str]:
    return {
        "sdk.language": "python",
        "sdk.version": version,
        "sdk.os": platform.system().lower(),
        "sdk.arch": platform.machine().lower(),
        "sdk.python": f"{sys.version_info.major}.{sys.version_info.minor}",
    }


def _get_or_build_client(dsn: str, version: str) -> Any:
    """Return the process's Sentry client for ``dsn``, building it once.

    Returns ``None`` if ``sentry-sdk`` is not installed or construction fails.
    Never raises.
    """
    global _flush_registered

    if dsn in _client_cache:
        return _client_cache[dsn]

    try:
        from sentry_sdk import Client  # type: ignore[import-not-found]
    except ImportError:
        # `sentry-sdk` is an optional extra; absence just means no phone-home.
        return None

    try:
        client = Client(
            dsn=dsn,
            release=f"deepgram-sdk@{version}",
            environment=_resolve_environment(),
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
    except Exception:
        return None

    _client_cache[dsn] = client
    _live_clients.append(client)
    if not _flush_registered:
        atexit.register(_flush_on_exit)
        _flush_registered = True
    return client


class TelemetrySink:
    """A single client's capture target: either a Sentry client or a handler.

    Owned by the ``DeepgramClient`` that created it. Keeping capture state here
    rather than in module globals is what isolates clients from each other: a
    handler bound to this sink only ever sees this client's events, and a sink
    that was never armed (no client, no handler) is a total no-op.
    """

    def __init__(
        self,
        *,
        client: Any = None,
        handler: Optional[TelemetryHandler] = None,
        base_tags: Optional[Dict[str, str]] = None,
    ) -> None:
        self._client = client
        self._handler = handler
        self._base_tags = base_tags or {}

    def _merge_tags(self, tags: Optional[Dict[str, str]]) -> Dict[str, str]:
        merged = dict(self._base_tags)
        if tags:
            merged.update(tags)
        return merged

    def capture_exception(
        self, exc: BaseException, *, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Report an SDK-originated exception. Best-effort; never raises.

        Only call this for errors that originate in Deepgram SDK code (API
        errors, transport failures) — never arbitrary host-application errors.
        """
        if self._handler is not None:
            try:
                self._handler(exc, tags or {})
            except Exception:
                pass
            return

        if self._client is None:
            return

        try:
            from sentry_sdk.utils import (  # type: ignore[import-not-found]
                event_from_exception,
            )

            event, hint = event_from_exception(exc, client_options=self._client.options)
            event["tags"] = self._merge_tags(tags)
            self._client.capture_event(event, hint=hint)
        except Exception:
            pass

    def capture_message(
        self, message: str, *, level: str = "error", tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Report a non-exception signal (e.g. an HTTP 5xx). Never raises.

        Custom handlers are exception-oriented, so messages only go to Sentry;
        a handler-backed sink (no Sentry client) drops these silently.
        """
        if self._client is None:
            return
        try:
            event = {"message": message, "level": level, "tags": self._merge_tags(tags)}
            self._client.capture_event(event)
        except Exception:
            pass


def init_telemetry(
    *,
    opt_out: bool,
    handler: Optional[TelemetryHandler] = None,
    version: str = "unknown",
) -> Optional[TelemetrySink]:
    """Build this client's telemetry sink, or ``None`` if telemetry is inert.

    Per-client by construction: the returned sink is owned by the caller, so a
    handler set on one client never receives another client's events, and one
    client's opt-out never suppresses (or arms) another's. Never raises.
    """
    base_tags = _build_base_tags(version)

    # A custom handler fully replaces Sentry, needs no DSN, and is scoped to
    # this sink alone. Checked before opt-out/DSN because it is the caller's
    # explicit request to receive their own SDK's errors in-process.
    if handler is not None:
        return TelemetrySink(handler=handler, base_tags=base_tags)

    if not is_enabled(opt_out):
        return None

    dsn = _resolve_dsn()
    if dsn is None:  # pragma: no cover - is_enabled already guaranteed this
        return None

    client = _get_or_build_client(dsn, version)
    if client is None:
        return None
    return TelemetrySink(client=client, base_tags=base_tags)


def _flush_on_exit() -> None:
    """Flush queued events before process exit (best-effort, 2s per client)."""
    for client in list(_live_clients):
        try:
            client.flush(timeout=2.0)
        except Exception:
            pass


def _reset_for_tests() -> None:
    """Reset process-wide telemetry state. Test-only."""
    global _flush_registered
    _client_cache.clear()
    _live_clients.clear()
    _flush_registered = False
