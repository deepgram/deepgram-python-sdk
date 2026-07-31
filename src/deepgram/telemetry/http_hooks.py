"""Attach error telemetry to the SDK's httpx client without touching generated code.

The Fern-generated wrapper builds its own httpx client and stores it at
``client_wrapper.httpx_client.httpx_client``. Rather than replace that client
(which would risk changing timeout/pool/proxy behaviour), we append a
``response`` event hook to the instance the wrapper already built. The hook
reports server-side failures (HTTP 5xx) with the request id and session id.

Transport-level exceptions (connection resets, timeouts) are not visible to a
response hook and are a deliberate follow-up (they need a transport/send wrap).
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional

import httpx
from .client import capture_message

# Server-side / SDK-actionable failures. 4xx (bad key, bad params) are user
# errors and are intentionally not reported to avoid noise.
HTTP_CAPTURE_MIN_STATUS = 500

# Deepgram returns a request id under one of these response headers.
_REQUEST_ID_HEADERS = ("dg-request-id", "x-dg-request-id", "request-id", "x-request-id")


def _extract_request_id(headers: Mapping[str, str]) -> Optional[str]:
    for name in _REQUEST_ID_HEADERS:
        value = headers.get(name)
        if value:
            return value
    return None


def _make_recorder(session_id: str) -> Callable[[httpx.Response], None]:
    def record(response: httpx.Response) -> None:
        status = response.status_code
        if status < HTTP_CAPTURE_MIN_STATUS:
            return
        tags = {"http.status": str(status), "session_id": session_id}
        request_id = _extract_request_id(response.headers)
        if request_id:
            tags["request_id"] = request_id
        try:
            # Path only — the query string can carry keys/params.
            tags["http.path"] = response.request.url.path
        except Exception:
            pass
        capture_message(f"HTTP {status} from Deepgram API", tags=tags)

    return record


def install_response_capture(client_wrapper: Any, session_id: str) -> bool:
    """Append the response hook to the wrapper's raw httpx client.

    Sync vs async is detected from the client type. Idempotent and total:
    returns whether a hook was installed, and never raises.
    """
    try:
        wrapper = getattr(client_wrapper, "httpx_client", None)
        raw = getattr(wrapper, "httpx_client", None)
        if not isinstance(raw, (httpx.Client, httpx.AsyncClient)):
            return False

        record = _make_recorder(session_id)

        if isinstance(raw, httpx.AsyncClient):

            async def hook(response: httpx.Response) -> None:
                try:
                    record(response)
                except Exception:
                    pass
        else:

            def hook(response: httpx.Response) -> None:  # type: ignore[misc]
                try:
                    record(response)
                except Exception:
                    pass

        hooks = raw.event_hooks
        hooks.setdefault("response", [])
        hooks["response"].append(hook)
        return True
    except Exception:
        return False
