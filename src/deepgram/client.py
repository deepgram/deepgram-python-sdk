"""
Custom client entrypoints that extend the generated BaseClient/AsyncBaseClient.

Adds support for `access_token` alongside `api_key` with the following rules:
- If `access_token` is provided, it takes precedence and sets `Authorization: bearer <token>`
- When `access_token` is used, `api_key` is forced to "token" to satisfy the generator,
  but the Authorization header is overridden for all HTTP and WebSocket requests.
"""

import os
import platform
import sys
import types
import uuid
from typing import Any, Dict, Optional

from .base_client import AsyncBaseClient, BaseClient

from deepgram.core.client_wrapper import AsyncClientWrapper, BaseClientWrapper, SyncClientWrapper
from deepgram.core.websocket_client import WebSocketFactory
from deepgram.extensions.core.instrumented_http import InstrumentedAsyncHttpClient, InstrumentedHttpClient
from deepgram.extensions.core.instrumented_socket import apply_websocket_instrumentation
from deepgram.extensions.core.telemetry_events import TelemetryHttpEvents, TelemetrySocketEvents
from deepgram.extensions.telemetry.batching_handler import BatchingTelemetryHandler
from deepgram.extensions.telemetry.handler import TelemetryHandler
from deepgram.extensions.telemetry.proto_encoder import encode_telemetry_batch


def _create_telemetry_context(session_id: str) -> Dict[str, Any]:
    """Create telemetry context with SDK and environment information."""
    try:
        # Get package version
        try:
            from . import version

            package_version = version.__version__
        except ImportError:
            package_version = "unknown"

        return {
            "package_name": "python-sdk",
            "package_version": package_version,
            "language": "python",
            "runtime_version": f"python {sys.version.split()[0]}",
            "os": platform.system().lower(),
            "arch": platform.machine(),
            "session_id": session_id,
            "environment": os.getenv("DEEPGRAM_ENV", "prod"),
        }
    except Exception:
        # Fallback minimal context
        return {
            "package_name": "python-sdk",
            "language": "python",
            "session_id": session_id,
        }


def _setup_telemetry(
    session_id: str,
    telemetry_opt_out: bool,
    telemetry_handler: Optional[TelemetryHandler],
    client_wrapper: BaseClientWrapper,
) -> Optional[TelemetryHandler]:
    """Setup telemetry for the client."""
    if telemetry_opt_out:
        return None

    # Use provided handler or create default batching handler
    if telemetry_handler is None:
        try:
            context = _create_telemetry_context(session_id)
            telemetry_handler = BatchingTelemetryHandler(
                endpoint="https://telemetry.dx.deepgram.com/v1/telemetry",
                api_key=client_wrapper.api_key,
                context_provider=lambda: context,
                synchronous=True,  # Use synchronous mode for reliability in short-lived scripts
                batch_size=1,  # Send immediately for short-lived scripts
                encode_batch=encode_telemetry_batch,  # Add proto encoder
            )
        except Exception:
            # If we can't create the handler, disable telemetry
            return None

    # Setup HTTP instrumentation
    try:
        http_events = TelemetryHttpEvents(telemetry_handler)

        # Replace the HTTP client with instrumented version
        if hasattr(client_wrapper, "httpx_client"):
            original_client = client_wrapper.httpx_client
            if hasattr(original_client, "httpx_client"):  # It's already our HttpClient
                instrumented_client = InstrumentedHttpClient(
                    delegate=original_client,
                    events=http_events,
                )
                client_wrapper.httpx_client = instrumented_client
    except Exception:
        # If instrumentation fails, continue without it
        pass

    # Setup WebSocket instrumentation
    try:
        socket_events = TelemetrySocketEvents(telemetry_handler)
        # Apply WebSocket instrumentation to capture connections in generated code
        apply_websocket_instrumentation(socket_events)
    except Exception:
        # If WebSocket instrumentation fails, continue without it
        pass

    return telemetry_handler


def _setup_async_telemetry(
    session_id: str,
    telemetry_opt_out: bool,
    telemetry_handler: Optional[TelemetryHandler],
    client_wrapper: BaseClientWrapper,
) -> Optional[TelemetryHandler]:
    """Setup telemetry for the async client."""
    if telemetry_opt_out:
        return None

    # Use provided handler or create default batching handler
    if telemetry_handler is None:
        try:
            context = _create_telemetry_context(session_id)
            telemetry_handler = BatchingTelemetryHandler(
                endpoint="https://telemetry.dx.deepgram.com/v1/telemetry",
                api_key=client_wrapper.api_key,
                context_provider=lambda: context,
                synchronous=True,  # Use synchronous mode for reliability in short-lived scripts
                batch_size=1,  # Send immediately for short-lived scripts
                encode_batch=encode_telemetry_batch,  # Add proto encoder
            )
        except Exception:
            # If we can't create the handler, disable telemetry
            return None

    # Setup HTTP instrumentation
    try:
        http_events = TelemetryHttpEvents(telemetry_handler)

        # Replace the HTTP client with instrumented version
        if hasattr(client_wrapper, "httpx_client"):
            original_client = client_wrapper.httpx_client
            if hasattr(original_client, "httpx_client"):  # It's already our AsyncHttpClient
                instrumented_client = InstrumentedAsyncHttpClient(
                    delegate=original_client,
                    events=http_events,
                )
                client_wrapper.httpx_client = instrumented_client
    except Exception:
        # If instrumentation fails, continue without it
        pass

    # Setup WebSocket instrumentation
    try:
        socket_events = TelemetrySocketEvents(telemetry_handler)
        # Apply WebSocket instrumentation to capture connections in generated code
        apply_websocket_instrumentation(socket_events)
    except Exception:
        # If WebSocket instrumentation fails, continue without it
        pass

    return telemetry_handler


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
    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[TelemetryHandler] = kwargs.pop("telemetry_handler", None)
        websocket_client: Optional[WebSocketFactory] = kwargs.pop("websocket_client", None)

        # Generate a session id up-front so it can be placed into headers for all transports
        generated_session_id = str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = generated_session_id

        # If an access_token is provided, force api_key to a placeholder that will be overridden
        if access_token is not None:
            kwargs["api_key"] = "token"

        super().__init__(*args, **kwargs)
        self.session_id = generated_session_id

        # If a custom websocket_client is provided, recreate the client wrapper with it
        if websocket_client is not None:
            original_wrapper = self._client_wrapper
            self._client_wrapper = SyncClientWrapper(
                api_key=original_wrapper.api_key,
                headers=original_wrapper.get_custom_headers(),
                environment=original_wrapper.get_environment(),
                timeout=original_wrapper.get_timeout(),
                httpx_client=original_wrapper.httpx_client.httpx_client,
                websocket_client=websocket_client,
            )

        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)

        # Setup telemetry
        self._telemetry_handler = _setup_telemetry(
            session_id=generated_session_id,
            telemetry_opt_out=telemetry_opt_out,
            telemetry_handler=telemetry_handler,
            client_wrapper=self._client_wrapper,
        )


class AsyncDeepgramClient(AsyncBaseClient):
    def __init__(self, *args, **kwargs) -> None:
        access_token: Optional[str] = kwargs.pop("access_token", None)
        telemetry_opt_out: bool = bool(kwargs.pop("telemetry_opt_out", True))
        telemetry_handler: Optional[TelemetryHandler] = kwargs.pop("telemetry_handler", None)
        websocket_client: Optional[WebSocketFactory] = kwargs.pop("websocket_client", None)

        # Generate a session id up-front so it can be placed into headers for all transports
        generated_session_id = str(uuid.uuid4())

        # Ensure headers object exists for pass-through custom headers
        headers: Optional[Dict[str, str]] = kwargs.get("headers")
        if headers is None:
            headers = {}
            kwargs["headers"] = headers

        # Ensure every request has a session identifier header
        headers["x-deepgram-session-id"] = generated_session_id

        # If an access_token is provided, force api_key to a placeholder that will be overridden
        if access_token is not None:
            kwargs["api_key"] = "token"

        super().__init__(*args, **kwargs)
        self.session_id = generated_session_id

        # If a custom websocket_client is provided, recreate the client wrapper with it
        if websocket_client is not None:
            original_wrapper = self._client_wrapper
            self._client_wrapper = AsyncClientWrapper(
                api_key=original_wrapper.api_key,
                headers=original_wrapper.get_custom_headers(),
                environment=original_wrapper.get_environment(),
                timeout=original_wrapper.get_timeout(),
                httpx_client=original_wrapper.httpx_client.httpx_client,
                websocket_client=websocket_client,
            )

        if access_token is not None:
            _apply_bearer_authorization_override(self._client_wrapper, access_token)

        # Setup telemetry
        self._telemetry_handler = _setup_async_telemetry(
            session_id=generated_session_id,
            telemetry_opt_out=telemetry_opt_out,
            telemetry_handler=telemetry_handler,
            client_wrapper=self._client_wrapper,
        )
