"""
Custom client entrypoints that extend the generated BaseClient/AsyncBaseClient.

Adds support for:
- `access_token` as an alternative to `api_key` with the following rules:
  - If `access_token` is provided, it takes precedence and sets `Authorization: bearer <token>`
  - When `access_token` is used, `api_key` is forced to "token" to satisfy the generator,
    but the Authorization header is overridden for all HTTP and WebSocket requests.
- `auth=False` for self-hosted or local Deepgram servers that don't require authentication:
  - No API key is needed, and no Authorization header is sent on HTTP or WebSocket requests.
  - When no key is available and the environment is not a Deepgram host, the missing-key
    error suggests `auth=False`.
- `session_id` as a header sent with every request and websocket connection:
  - If `session_id` is provided, it will be used; otherwise, a UUID is auto-generated
  - The session_id is sent as the `x-deepgram-session-id` header
- `transport_factory` to replace the default `websockets` transport with a custom one:
  - A callable: ``factory(url, headers) -> transport`` returning an object with
    ``send()``, ``recv()``, iteration, and ``close()`` support.
- `reconnect` flag (default `True`) declaring whether the SDK is expected to
  manage WebSocket reconnects for this client. When a custom
  ``transport_factory`` is set, ``reconnect`` is auto-disabled because the
  custom transport owns its own retry/reconnect lifecycle; double-stacking
  retries on top would cause storm-on-storm under burst load. The Python
  SDK has no wrapper reconnect layer today, so this flag is declarative
  only -- it documents intent and is reserved for any future SDK-side
  reconnect logic.
"""

import os
import types
import urllib.parse
import uuid
from typing import Any, Callable, Dict, Optional

import httpx
from ._secure_logging import install_websocket_log_redaction
from .base_client import AsyncBaseClient, BaseClient
from .core.api_error import ApiError
from .transport import install_transport

from deepgram.core.client_wrapper import BaseClientWrapper


class _NoAuthorizationHeaders(Dict[str, str]):
    """A header map that permanently drops case-insensitive Authorization keys."""

    def __init__(self, headers: Dict[str, str]) -> None:
        super().__init__()
        self.update(headers)

    def __setitem__(self, key: str, value: str) -> None:
        if key.lower() != "authorization":
            super().__setitem__(key, value)

    def update(self, *args: Any, **kwargs: str) -> None:
        for key, value in dict(*args, **kwargs).items():
            self[key] = value


def _apply_bearer_authorization_override(client_wrapper: BaseClientWrapper, bearer_token: str) -> None:
    """Override header providers to always use a Bearer authorization token.

    This updates both:
    - client_wrapper.get_headers() used by WebSocket clients
    - client_wrapper.httpx_client.base_headers used by HTTP clients
    """
    original_get_headers = client_wrapper.get_headers

    def _get_headers_with_bearer(_self: Any) -> Dict[str, str]:
        headers = original_get_headers()
        headers["Authorization"] = f"bearer {bearer_token}"
        return headers

    # Override on wrapper for WebSockets
    client_wrapper.get_headers = types.MethodType(_get_headers_with_bearer, client_wrapper)  # type: ignore[method-assign]

    # Override on HTTP client for REST requests
    if hasattr(client_wrapper, "httpx_client") and hasattr(client_wrapper.httpx_client, "base_headers"):
        client_wrapper.httpx_client.base_headers = client_wrapper.get_headers


def _origin(url: str) -> Optional[tuple[str, str, Optional[int]]]:
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or parsed.hostname is None:
            return None
        scheme = parsed.scheme.lower()
        port = parsed.port
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
            port = None
        return scheme, parsed.hostname.lower(), port
    except ValueError:
        return None


def _environment_origins(environment: Any) -> set[tuple[str, str, Optional[int]]]:
    return {
        origin
        for name in ("base", "agent_rest")
        if isinstance(url := getattr(environment, name, None), str)
        if (origin := _origin(url)) is not None
    }


def _remove_authorization_from_request(
    request: httpx.Request, target_origins: set[tuple[str, str, Optional[int]]], session_id: str
) -> None:
    # Normalize the request URL with the same helper used for the environment so an
    # explicit default port survives httpx's scheme-case-sensitive port handling.
    request_origin = _origin(str(request.url))
    if request_origin not in target_origins or request.headers.get("x-deepgram-session-id") != session_id:
        return

    for header in list(request.headers):
        if header.lower() == "authorization":
            del request.headers[header]


def _install_no_authorization_request_hook(
    httpx_client: Any, target_origins: set[tuple[str, str, Optional[int]]], session_id: str
) -> None:
    """Strip Authorization only from this client's requests to its Deepgram origins."""

    def sync_request_hook(request: httpx.Request) -> None:
        _remove_authorization_from_request(request, target_origins, session_id)

    if isinstance(httpx_client, httpx.AsyncClient):

        async def async_request_hook(request: httpx.Request) -> None:
            _remove_authorization_from_request(request, target_origins, session_id)

        httpx_client.event_hooks.setdefault("request", []).append(async_request_hook)
    else:
        httpx_client.event_hooks.setdefault("request", []).append(sync_request_hook)


def _apply_no_authorization_override(client_wrapper: BaseClientWrapper, session_id: str) -> None:
    """Drop the Authorization header from every HTTP and WebSocket request (``auth=False``)."""
    original_get_headers = client_wrapper.get_headers

    def _get_headers_without_auth(_self: Any) -> Dict[str, str]:
        # Generated WebSocket clients append their per-call ``authorization`` and
        # ``additional_headers`` after invoking this provider. Return a mapping
        # that keeps suppressing the header through those later mutations.
        return _NoAuthorizationHeaders(original_get_headers())

    client_wrapper.get_headers = types.MethodType(_get_headers_without_auth, client_wrapper)  # type: ignore[method-assign]

    if hasattr(client_wrapper, "httpx_client") and hasattr(client_wrapper.httpx_client, "base_headers"):
        client_wrapper.httpx_client.base_headers = client_wrapper.get_headers
        _install_no_authorization_request_hook(
            client_wrapper.httpx_client.httpx_client,
            _environment_origins(client_wrapper.get_environment()),
            session_id,
        )


_MISSING_KEY_MESSAGE = "The client must be instantiated by either passing in api_key or setting DEEPGRAM_API_KEY"
_SELF_HOSTED_NO_AUTH_HINT = (
    "If you are connecting to a self-hosted or local Deepgram server that does not require "
    "authentication, pass auth=False when initializing the client."
)


def _is_deepgram_hosted(environment: Any) -> bool:
    """Whether the environment's REST base is Deepgram's hosted API.

    Only an unset environment counts as hosted, because the client then uses
    ``DeepgramClientEnvironment.PRODUCTION``. A base that can't be parsed or has no host (for
    example ``"127.0.0.1:8000"``, with the scheme left off) can never be Deepgram's host.
    """
    if environment is None:
        return True
    base = getattr(environment, "base", None)
    if not isinstance(base, str):
        return False
    try:
        host = (urllib.parse.urlparse(base).hostname or "").lower()
    except ValueError:
        return False
    return host == "deepgram.com" or host.endswith(".deepgram.com")


def _missing_key_error(environment: Any) -> ApiError:
    body = _MISSING_KEY_MESSAGE
    if not _is_deepgram_hosted(environment):
        body = f"{body}. {_SELF_HOSTED_NO_AUTH_HINT}"
    return ApiError(body=body)


def _resolve_credentials(kwargs: Dict[str, Any], access_token: Optional[str], auth: Any) -> None:
    """Fill ``kwargs["api_key"]`` for the generated base client, or raise if no credential is available.

    Shared by the sync and async clients. The generated base client requires an api_key, so
    ``access_token`` and ``auth=False`` set a placeholder; the Authorization header is then
    replaced (Bearer) or removed after construction.
    """
    if auth is not None and auth is not False:
        raise ValueError(
            "auth only accepts False, which disables authentication for self-hosted servers. "
            "To authenticate, omit auth and pass api_key or access_token."
        )

    environment = kwargs.get("environment")
    if auth is False:
        if access_token is not None or kwargs.get("api_key") is not None:
            raise ValueError("auth=False cannot be combined with api_key or access_token")
        kwargs["api_key"] = ""
    elif access_token is not None:
        # access_token takes precedence over api_key; the header becomes Bearer after construction.
        if kwargs.get("api_key") is None:
            kwargs["api_key"] = "token"
    elif "api_key" in kwargs and kwargs["api_key"] is None:
        # Fern now resolves None to DEEPGRAM_API_KEY in the base client. Preserve the SDK
        # contract that an explicit None disables ambient lookup.
        raise _missing_key_error(environment)
    elif "api_key" not in kwargs:
        # The generated base client takes os.getenv("DEEPGRAM_API_KEY") as a default argument, so
        # it is read once at import. Re-read it here so a key set after import (load_dotenv below
        # the imports) is still picked up.
        kwargs["api_key"] = os.getenv("DEEPGRAM_API_KEY")
        if kwargs["api_key"] is None:
            raise _missing_key_error(environment)


class DeepgramClient(BaseClient):
    """
    Custom Deepgram client that extends the generated BaseClient.

    Supports:
    - `session_id`: Optional session identifier. If not provided, a UUID is auto-generated.
                     Sent as `x-deepgram-session-id` header in all requests and websocket connections.
    - `access_token`: Alternative to `api_key`. If provided, uses Bearer token authentication.
    - `auth`: Pass ``False`` for a self-hosted or local Deepgram server that doesn't require
              authentication. No API key is needed and no Authorization header is sent.
    - `transport_factory`: Custom sync WebSocket transport factory. A callable
                           ``factory(url, headers) -> transport`` whose return value must support
                           ``send()``, ``recv()``, iteration, and ``close()``.
    - `reconnect`: Declarative flag (default ``True``) signalling whether the SDK is
                    expected to manage WebSocket reconnects for this client. Auto-disabled
                    when ``transport_factory`` is set, since the custom transport owns its
                    retry/reconnect lifecycle. The Python SDK has no wrapper reconnect layer
                    today, so this flag is declarative only -- it documents intent and is
                    reserved for any future SDK-side reconnect logic.
    - `redact_credentials_in_logs`: Mask the `Authorization` header (API key / access token)
                    in the `websockets` library's DEBUG handshake logs. Defaults to `True`; set
                    to `False` to opt out and manage credential redaction yourself.
    - `telemetry_opt_out`: Telemetry opt-out flag (maintained for backwards compatibility, no-op).
    - `telemetry_handler`: Telemetry handler (maintained for backwards compatibility, no-op).
    """

    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        auth: Any = kwargs.pop("auth", None)
        session_id: Optional[str] = kwargs.pop("session_id", None)
        transport_factory: Optional[Callable] = kwargs.pop("transport_factory", None)
        reconnect: bool = bool(kwargs.pop("reconnect", True))
        redact_credentials_in_logs: bool = bool(kwargs.pop("redact_credentials_in_logs", True))
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[Any] = kwargs.pop("telemetry_handler", None)

        # Mask the Authorization header (API key / access token) in the
        # third-party `websockets` library's DEBUG handshake logs so the
        # credential is never written to application logs. On by default;
        # pass `redact_credentials_in_logs=False` to manage redaction yourself.
        if redact_credentials_in_logs:
            install_websocket_log_redaction()

        # Use provided session_id or generate one
        final_session_id = session_id if session_id is not None else str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = final_session_id

        _resolve_credentials(kwargs, access_token, auth)

        super().__init__(*args, **kwargs)
        self.session_id = final_session_id

        # Override Authorization header to use Bearer token if access_token was provided,
        # or drop it entirely for auth=False
        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)
        elif auth is False:
            _apply_no_authorization_override(self._client_wrapper, final_session_id)

        # Install custom WebSocket transport if provided. Auto-disable
        # `reconnect`: a custom transport owns its retry lifecycle, so flip
        # the flag off even if the caller left it at the default.
        if transport_factory is not None:
            install_transport(sync_factory=transport_factory)
            reconnect = False
        self.reconnect = reconnect

        # Store telemetry handler for backwards compatibility (no-op, telemetry not implemented)
        self._telemetry_handler = None


class AsyncDeepgramClient(AsyncBaseClient):
    """
    Custom async Deepgram client that extends the generated AsyncBaseClient.

    Supports:
    - `session_id`: Optional session identifier. If not provided, a UUID is auto-generated.
                     Sent as `x-deepgram-session-id` header in all requests and websocket connections.
    - `access_token`: Alternative to `api_key`. If provided, uses Bearer token authentication.
    - `auth`: Pass ``False`` for a self-hosted or local Deepgram server that doesn't require
              authentication. No API key is needed and no Authorization header is sent.
    - `transport_factory`: Custom async WebSocket transport factory. A callable
                           ``factory(url, headers) -> transport`` whose return value must support
                           ``send()``, ``recv()``, async iteration, and ``close()``.
    - `reconnect`: Declarative flag (default ``True``) signalling whether the SDK is
                    expected to manage WebSocket reconnects for this client. Auto-disabled
                    when ``transport_factory`` is set, since the custom transport owns its
                    retry/reconnect lifecycle. The Python SDK has no wrapper reconnect layer
                    today, so this flag is declarative only -- it documents intent and is
                    reserved for any future SDK-side reconnect logic.
    - `redact_credentials_in_logs`: Mask the `Authorization` header (API key / access token)
                    in the `websockets` library's DEBUG handshake logs. Defaults to `True`; set
                    to `False` to opt out and manage credential redaction yourself.
    - `telemetry_opt_out`: Telemetry opt-out flag (maintained for backwards compatibility, no-op).
    - `telemetry_handler`: Telemetry handler (maintained for backwards compatibility, no-op).
    """

    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        auth: Any = kwargs.pop("auth", None)
        session_id: Optional[str] = kwargs.pop("session_id", None)
        transport_factory: Optional[Callable] = kwargs.pop("transport_factory", None)
        reconnect: bool = bool(kwargs.pop("reconnect", True))
        redact_credentials_in_logs: bool = bool(kwargs.pop("redact_credentials_in_logs", True))
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[Any] = kwargs.pop("telemetry_handler", None)

        # Mask the Authorization header (API key / access token) in the
        # third-party `websockets` library's DEBUG handshake logs so the
        # credential is never written to application logs. On by default;
        # pass `redact_credentials_in_logs=False` to manage redaction yourself.
        if redact_credentials_in_logs:
            install_websocket_log_redaction()

        # Use provided session_id or generate one
        final_session_id = session_id if session_id is not None else str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = final_session_id

        _resolve_credentials(kwargs, access_token, auth)

        super().__init__(*args, **kwargs)
        self.session_id = final_session_id

        # Override Authorization header to use Bearer token if access_token was provided,
        # or drop it entirely for auth=False
        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)
        elif auth is False:
            _apply_no_authorization_override(self._client_wrapper, final_session_id)

        # Install custom WebSocket transport if provided. Auto-disable
        # `reconnect`: a custom transport owns its retry lifecycle, so flip
        # the flag off even if the caller left it at the default.
        if transport_factory is not None:
            install_transport(async_factory=transport_factory)
            reconnect = False
        self.reconnect = reconnect

        # Store telemetry handler for backwards compatibility (no-op, telemetry not implemented)
        self._telemetry_handler = None
