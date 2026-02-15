"""
Custom client entrypoints that extend the generated BaseClient/AsyncBaseClient.

Adds support for:
- `access_token` as an alternative to `api_key` with the following rules:
  - If `access_token` is provided, it takes precedence and sets `Authorization: bearer <token>`
  - When `access_token` is used, `api_key` is forced to "token" to satisfy the generator,
    but the Authorization header is overridden for all HTTP and WebSocket requests.
- `session_id` as a header sent with every request and websocket connection:
  - If `session_id` is provided, it will be used; otherwise, a UUID is auto-generated
  - The session_id is sent as the `x-deepgram-session-id` header
"""

import types
import uuid
from typing import Any, Dict, Optional

from .base_client import AsyncBaseClient, BaseClient

from deepgram.core.client_wrapper import BaseClientWrapper


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


class DeepgramClient(BaseClient):
    """
    Custom Deepgram client that extends the generated BaseClient.

    Supports:
    - `session_id`: Optional session identifier. If not provided, a UUID is auto-generated.
                     Sent as `x-deepgram-session-id` header in all requests and websocket connections.
    - `access_token`: Alternative to `api_key`. If provided, uses Bearer token authentication.
    - `telemetry_opt_out`: Telemetry opt-out flag (maintained for backwards compatibility, no-op).
    - `telemetry_handler`: Telemetry handler (maintained for backwards compatibility, no-op).
    """

    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        session_id: Optional[str] = kwargs.pop("session_id", None)
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[Any] = kwargs.pop("telemetry_handler", None)

        # Use provided session_id or generate one
        final_session_id = session_id if session_id is not None else str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = final_session_id

        # Handle access_token: if provided, it takes precedence over api_key
        # The base client requires api_key, so we set a placeholder if needed
        # The Authorization header will be overridden to use Bearer token
        if access_token is not None:
            # Set a placeholder api_key if none provided (base client requires it)
            if kwargs.get("api_key") is None:
                kwargs["api_key"] = "token"

        super().__init__(*args, **kwargs)
        self.session_id = final_session_id

        # Override Authorization header to use Bearer token if access_token was provided
        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)

        # Store telemetry handler for backwards compatibility (no-op, telemetry not implemented)
        self._telemetry_handler = None


class AsyncDeepgramClient(AsyncBaseClient):
    """
    Custom async Deepgram client that extends the generated AsyncBaseClient.

    Supports:
    - `session_id`: Optional session identifier. If not provided, a UUID is auto-generated.
                     Sent as `x-deepgram-session-id` header in all requests and websocket connections.
    - `access_token`: Alternative to `api_key`. If provided, uses Bearer token authentication.
    - `telemetry_opt_out`: Telemetry opt-out flag (maintained for backwards compatibility, no-op).
    - `telemetry_handler`: Telemetry handler (maintained for backwards compatibility, no-op).
    """

    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        session_id: Optional[str] = kwargs.pop("session_id", None)
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[Any] = kwargs.pop("telemetry_handler", None)

        # Use provided session_id or generate one
        final_session_id = session_id if session_id is not None else str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = final_session_id

        # Handle access_token: if provided, it takes precedence over api_key
        # The base client requires api_key, so we set a placeholder if needed
        # The Authorization header will be overridden to use Bearer token
        if access_token is not None:
            # Set a placeholder api_key if none provided (base client requires it)
            if kwargs.get("api_key") is None:
                kwargs["api_key"] = "token"

        super().__init__(*args, **kwargs)
        self.session_id = final_session_id

        # Override Authorization header to use Bearer token if access_token was provided
        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)

        # Store telemetry handler for backwards compatibility (no-op, telemetry not implemented)
        self._telemetry_handler = None
