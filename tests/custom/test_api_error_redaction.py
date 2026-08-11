"""
The SDK's error types must never carry a credential.

Every websocket ``connect()`` path raises ``ApiError(headers=dict(headers), ...)``
with the *full* request headers, and both error types stringify their headers
dict. Before this was fixed, a failed connect produced:

    headers: {'Authorization': 'Token ba06ae87...', ...}, status_code: 400, ...

so any application that logged the exception — ``print(e)``, a traceback, a log
aggregator, an error tracker — wrote the customer's API key in clear text. This
is the same threat ``_secure_logging.py`` already covers for the ``websockets``
DEBUG handshake logs; the exception path is the other route to it.

Redaction happens at construction rather than only in ``__str__`` so it also
covers ``repr()`` and attribute serialisation (an error tracker sends both).
Non-sensitive headers are deliberately preserved: ``dg-request-id`` is the main
reason to inspect them at all.

Hand-written and frozen in ``.fernignore`` alongside the two patched files.
"""

import pytest

from deepgram.core.api_error import ApiError
from deepgram.core.parse_error import ParsingError

_SECRET = "abcd1234abcd1234abcd1234abcd1234abcd1234"

_HEADERS = {
    "Authorization": f"Token {_SECRET}",
    "Proxy-Authorization": f"bearer {_SECRET}",
    "dg-request-id": "req-abc-123",
    "User-Agent": "deepgram-sdk/9.9.9",
}


def _build(cls):
    kwargs = {"cause": ValueError("boom")} if cls is ParsingError else {}
    return cls(
        headers=dict(_HEADERS),
        status_code=400,
        body="Unexpected error when initializing websocket connection.",
        **kwargs,
    )


@pytest.mark.parametrize("cls", [ApiError, ParsingError])
class TestCredentialRedaction:
    def test_secret_absent_from_str(self, cls):
        assert _SECRET not in str(_build(cls))

    def test_secret_absent_from_repr(self, cls):
        # An error tracker serialises repr/attributes, not just the message.
        assert _SECRET not in repr(_build(cls))

    def test_secret_absent_from_headers_attribute(self, cls):
        err = _build(cls)
        assert not any(_SECRET in str(v) for v in (err.headers or {}).values())

    def test_auth_scheme_is_preserved(self, cls):
        # Keep the scheme so "was I sending a Token or a bearer?" stays answerable.
        err = _build(cls)
        assert err.headers["Authorization"] == "Token [REDACTED]"
        assert err.headers["Proxy-Authorization"] == "bearer [REDACTED]"

    def test_non_sensitive_headers_survive(self, cls):
        err = _build(cls)
        assert err.headers["dg-request-id"] == "req-abc-123"
        assert err.headers["User-Agent"] == "deepgram-sdk/9.9.9"

    def test_none_headers_stay_none(self, cls):
        kwargs = {"cause": None} if cls is ParsingError else {}
        assert cls(headers=None, status_code=500, body="x", **kwargs).headers is None

    def test_redaction_never_raises_on_odd_headers(self, cls):
        # Redaction must not be the reason an error path fails.
        kwargs = {"cause": None} if cls is ParsingError else {}
        err = cls(headers="not-a-mapping", status_code=500, body="x", **kwargs)  # type: ignore[arg-type]
        assert err.headers is None
