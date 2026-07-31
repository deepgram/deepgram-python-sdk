"""Opt-out, isolated Sentry telemetry for the Deepgram Python SDK.

Hand-written module (not Fern-generated). Wired into ``DeepgramClient`` /
``AsyncDeepgramClient`` via the ``telemetry_opt_out`` and ``telemetry_handler``
constructor parameters.
"""

from .client import (
    TelemetryHandler,
    capture_exception,
    capture_message,
    init_telemetry,
    is_enabled,
)
from .http_hooks import install_response_capture

__all__ = [
    "TelemetryHandler",
    "capture_exception",
    "capture_message",
    "init_telemetry",
    "install_response_capture",
    "is_enabled",
]
