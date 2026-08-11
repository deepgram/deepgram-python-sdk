"""PII/secret scrubbing for SDK telemetry events.

An SDK runs inside customer applications, so the scrubbing bar is far higher
than for a first-party CLI: audio bytes, API keys / access tokens, request and
response bodies, and file paths must never leave the customer's process. This
module is a defense-in-depth ``before_send`` hook layered on top of the Sentry
client options set in ``client.py`` (``send_default_pii=False``,
``include_local_variables=False``, ``max_request_body_size="never"``).

Mirrors the redaction discipline already established in ``_secure_logging.py``.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from sentry_sdk.types import Event, Hint

# Header names that may carry credentials or identifying data. Compared
# case-insensitively.
_SENSITIVE_HEADERS = frozenset(
    {
        "authorization",
        "x-api-key",
        "api-key",
        "cookie",
        "set-cookie",
        "proxy-authorization",
    }
)

# The user-identifying home-directory segment of a filesystem path:
#   /Users/<name>/...   (macOS)
#   /home/<name>/...    (Linux)
#   C:\Users\<name>\... (Windows)
# We keep the rest of the path (useful for debugging and for Sentry code
# mappings, which key off the in-package suffix) and redact only the username,
# which is the personal-data bit.
_HOME_DIR_RE = re.compile(r"([\\/](?:Users|home)[\\/])[^\\/]+", re.IGNORECASE)


def _redact_path(path: Any) -> Any:
    if not isinstance(path, str):
        return path
    return _HOME_DIR_RE.sub(r"\1<redacted>", path)


def _scrub_frame_paths(event: "Event") -> None:
    """Redact the home-dir username from every stack-frame path in the event.

    Stack frames carry ``abs_path``/``filename`` like
    ``/Users/jane.doe/src/acme/main.py``. Client-level scrubbing
    (``include_local_variables=False``) does nothing about these, because the
    path is part of the frame metadata, not a local variable.
    """
    stacktraces = []
    for group in ("exception", "threads"):
        container = event.get(group)
        if isinstance(container, dict):
            for value in container.get("values") or []:
                if isinstance(value, dict) and isinstance(value.get("stacktrace"), dict):
                    stacktraces.append(value["stacktrace"])
    if isinstance(event.get("stacktrace"), dict):
        stacktraces.append(event["stacktrace"])

    for stacktrace in stacktraces:
        for frame in stacktrace.get("frames") or []:
            if not isinstance(frame, dict):
                continue
            for key in ("abs_path", "filename"):
                if key in frame:
                    frame[key] = _redact_path(frame[key])


def scrub_event(event: "Event", _hint: "Hint") -> "Event | None":
    """Strip request bodies, headers, query strings, and user-identifying data.

    Returns the mutated event, or ``None`` to drop it entirely. Kept total and
    exception-free: a scrubber that raises would take telemetry (and any code
    path that flushes it) down with it, so callers must never see an error here.
    """
    try:
        request: Dict[str, Any] = event.get("request") or {}
        # Bodies and query strings can contain audio, transcripts, keys, or URLs.
        if "data" in request:
            request["data"] = "[Filtered]"
        if "query_string" in request:
            request["query_string"] = "[Filtered]"
        if "cookies" in request:
            request["cookies"] = {}
        # Drop credential-bearing headers; keep the rest for debugging value.
        headers = request.get("headers")
        if isinstance(headers, dict):
            request["headers"] = {
                k: ("[Filtered]" if k.lower() in _SENSITIVE_HEADERS else v)
                for k, v in headers.items()
            }

        # Never attribute events to an end user. Drop geo too — it is inferred
        # from the sending IP and identifies the customer's location.
        user: Dict[str, Any] = event.get("user") or {}
        for key in ("email", "ip_address", "username", "id", "geo"):
            user.pop(key, None)

        # Sentry auto-attaches the machine hostname; on a customer's machine
        # that leaks their host/developer name, so strip it.
        event.pop("server_name", None)

        # Extra/context blobs are developer-controlled and may echo payloads.
        event.pop("extra", None)

        # Stack-frame paths embed the OS home directory, which carries the
        # developer's username (e.g. /Users/jane.doe/...). Redact that segment.
        _scrub_frame_paths(event)
    except Exception:
        # If scrubbing itself fails, drop the event rather than risk a leak.
        return None

    return event
