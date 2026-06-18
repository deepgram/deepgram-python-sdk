"""Redaction of credentials from third-party ``websockets`` debug logs.

The ``websockets`` library logs the full opening handshake at ``DEBUG`` level,
one record per header, via ``logger.debug("> %s: %s", name, value)`` (and
``"< %s: %s"`` for the response). That includes the ``Authorization`` header —
i.e. the Deepgram API key or access token in clear text. Any application that
enables ``DEBUG`` logging (common during development/troubleshooting) would then
write the credential into its logs, from where it is easily committed to a repo
or shipped to a log aggregator.

This module installs a :class:`logging.Filter` on the ``websockets`` client and
server loggers that masks the value of sensitive headers *before* the record
reaches any handler/formatter, so the credential is never emitted regardless of
the application's log level. The filter only rewrites the value of known
credential headers; it suppresses nothing and changes no other output.

This is a hand-written security utility with no Fern-generated counterpart and
is frozen in ``.fernignore``.
"""

import logging
import typing

# Header names (lower-cased) whose values must never be logged in clear text.
_SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization"})

# Replacement for the credential portion of a sensitive header value.
_REDACTED = "[REDACTED]"

# websockets >= 12 emits handshake header records directly on these loggers
# (no per-connection child loggers), so a filter attached here sees every
# header record before it propagates to the application's handlers.
_TARGET_LOGGERS = ("websockets.client", "websockets.server")


def _mask_value(value: typing.Any) -> str:
    """Mask a credential while preserving the auth scheme for debuggability.

    ``"Token abc123"`` -> ``"Token [REDACTED]"`` and ``"bearer xyz"`` ->
    ``"bearer [REDACTED]"``. A value with no scheme prefix is fully masked.
    """
    text = str(value)
    scheme, sep, _ = text.partition(" ")
    if sep and scheme:
        return f"{scheme} {_REDACTED}"
    return _REDACTED


class RedactCredentialsFilter(logging.Filter):
    """Masks sensitive header values in ``websockets`` handshake debug records.

    websockets logs each handshake header as ``logger.debug("> %s: %s", name,
    value)``. We rewrite ``record.args`` in place when the header name is a known
    credential header, so the secret never reaches a handler or formatter. The
    record is mutated before propagation, so every downstream handler sees the
    redacted value. The filter always returns ``True`` (it never drops records).
    """

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.msg
        args = record.args
        if (
            isinstance(msg, str)
            and "%s: %s" in msg
            and isinstance(args, tuple)
            and len(args) == 2
        ):
            name, value = args
            if isinstance(name, str) and name.lower() in _SENSITIVE_HEADERS:
                record.args = (name, _mask_value(value))
        return True


def install_websocket_log_redaction() -> None:
    """Attach :class:`RedactCredentialsFilter` to the websockets loggers.

    Idempotent: a logger never accumulates more than one redaction filter, so it
    is safe to call from every client constructor.
    """
    for name in _TARGET_LOGGERS:
        logger = logging.getLogger(name)
        if not any(isinstance(f, RedactCredentialsFilter) for f in logger.filters):
            logger.addFilter(RedactCredentialsFilter())


def uninstall_websocket_log_redaction() -> None:
    """Remove the redaction filter from the websockets loggers.

    Provided as an opt-out for applications that manage credential redaction
    themselves and want the raw websockets debug output back.
    """
    for name in _TARGET_LOGGERS:
        logger = logging.getLogger(name)
        for f in [f for f in logger.filters if isinstance(f, RedactCredentialsFilter)]:
            logger.removeFilter(f)
