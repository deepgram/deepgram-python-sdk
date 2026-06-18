"""Tests for credential redaction in third-party ``websockets`` debug logs.

Regression coverage for the security report that the SDK leaked the API key /
access token into application logs: ``websockets`` logs the opening handshake at
DEBUG, including ``Authorization: Token <key>``. The SDK installs a redaction
filter on the websockets loggers so the credential is masked regardless of the
application's log level.
"""

import logging

import pytest

from deepgram._secure_logging import (
    RedactCredentialsFilter,
    _mask_value,
    install_websocket_log_redaction,
    uninstall_websocket_log_redaction,
)

_WS_LOGGERS = ("websockets.client", "websockets.server")


@pytest.fixture(autouse=True)
def _clean_filters():
    """Ensure each test starts and ends with no redaction filter installed."""
    uninstall_websocket_log_redaction()
    yield
    uninstall_websocket_log_redaction()


def _emit_header(caplog, logger_name, name, value):
    """Emit a record exactly like websockets' handshake header logging."""
    logger = logging.getLogger(logger_name)
    with caplog.at_level(logging.DEBUG, logger=logger_name):
        # websockets/client.py: self.logger.debug("> %s: %s", key, value)
        logger.debug("> %s: %s", name, value)
    return caplog.records[-1].getMessage()


def test_authorization_token_is_redacted(caplog):
    install_websocket_log_redaction()
    msg = _emit_header(caplog, "websockets.client", "Authorization", "Token 3f10254bSECRETKEY")
    assert "3f10254bSECRETKEY" not in msg
    assert "Token" in msg  # scheme preserved for debuggability
    assert "[REDACTED]" in msg


def test_bearer_access_token_is_redacted(caplog):
    install_websocket_log_redaction()
    msg = _emit_header(caplog, "websockets.client", "Authorization", "bearer eyJ.SECRET.sig")
    assert "SECRET" not in msg
    assert msg.endswith("bearer [REDACTED]")


def test_proxy_authorization_is_redacted(caplog):
    install_websocket_log_redaction()
    msg = _emit_header(caplog, "websockets.server", "Proxy-Authorization", "Basic c2VjcmV0")
    assert "c2VjcmV0" not in msg
    assert "[REDACTED]" in msg


def test_non_sensitive_headers_are_untouched(caplog):
    install_websocket_log_redaction()
    msg = _emit_header(caplog, "websockets.client", "Sec-WebSocket-Version", "13")
    assert msg == "> Sec-WebSocket-Version: 13"


def test_redaction_is_case_insensitive_on_header_name(caplog):
    install_websocket_log_redaction()
    msg = _emit_header(caplog, "websockets.client", "authorization", "Token abc123")
    assert "abc123" not in msg


def test_without_install_secret_is_present(caplog):
    """Sanity check: the secret IS logged when redaction is not installed."""
    msg = _emit_header(caplog, "websockets.client", "Authorization", "Token VISIBLE123")
    assert "VISIBLE123" in msg


def test_install_is_idempotent():
    install_websocket_log_redaction()
    install_websocket_log_redaction()
    for name in _WS_LOGGERS:
        filters = [f for f in logging.getLogger(name).filters if isinstance(f, RedactCredentialsFilter)]
        assert len(filters) == 1


def test_uninstall_removes_filter():
    install_websocket_log_redaction()
    uninstall_websocket_log_redaction()
    for name in _WS_LOGGERS:
        filters = [f for f in logging.getLogger(name).filters if isinstance(f, RedactCredentialsFilter)]
        assert filters == []


def test_mask_value_preserves_scheme():
    assert _mask_value("Token abc") == "Token [REDACTED]"
    assert _mask_value("bearer xyz") == "bearer [REDACTED]"


def test_mask_value_without_scheme_is_fully_masked():
    assert _mask_value("rawsecret") == "[REDACTED]"


def test_constructing_client_installs_redaction(caplog):
    """The client constructor installs redaction by default."""
    from deepgram import DeepgramClient

    uninstall_websocket_log_redaction()
    DeepgramClient(api_key="dummy-key")
    msg = _emit_header(caplog, "websockets.client", "Authorization", "Token CTORSECRET")
    assert "CTORSECRET" not in msg


def test_opt_out_disables_redaction_at_construction(caplog):
    """`redact_credentials_in_logs=False` leaves the websockets logs untouched."""
    from deepgram import DeepgramClient

    uninstall_websocket_log_redaction()
    DeepgramClient(api_key="dummy-key", redact_credentials_in_logs=False)
    # Constructor must not have installed the filter.
    for name in _WS_LOGGERS:
        filters = [f for f in logging.getLogger(name).filters if isinstance(f, RedactCredentialsFilter)]
        assert filters == []
