"""
Instrumented WebSocket clients for telemetry.

This module provides WebSocket client wrappers that automatically capture
telemetry events, following the same pattern as instrumented_http.py.
"""

import functools
import time
import typing
from contextlib import asynccontextmanager, contextmanager

import websockets.exceptions
import websockets.sync.client as websockets_sync_client

try:
    from websockets.legacy.client import connect as websockets_client_connect  # type: ignore
except ImportError:
    from websockets import connect as websockets_client_connect  # type: ignore

try:
    import websockets.sync.connection as websockets_sync_connection
    from websockets.legacy.client import WebSocketClientProtocol  # type: ignore
except ImportError:
    try:
        import websockets.sync.connection as websockets_sync_connection
        from websockets import WebSocketClientProtocol  # type: ignore
    except ImportError:
        # Fallback types
        WebSocketClientProtocol = typing.Any
        websockets_sync_connection = typing.Any


class SocketEvents(typing.Protocol):
    """Protocol for WebSocket telemetry events."""
    
    def on_ws_connect(
        self,
        *,
        url: str,
        headers: typing.Mapping[str, str] | None = None,
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...
    
    def on_ws_error(
        self,
        *,
        url: str,
        error: BaseException,
        duration_ms: float,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...
    
    def on_ws_close(
        self,
        *,
        url: str,
        duration_ms: float,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...


def _capture_request_details(method: str, url: str, headers: typing.Dict[str, str] | None = None, **kwargs) -> typing.Dict[str, typing.Any]:
    """Capture request details for telemetry (avoiding circular import)."""
    details = {
        "method": method,
        "url": url,
    }
    if headers:
        details["headers"] = dict(headers)
    
    # Add connection parameters for WebSocket requests
    for key, value in kwargs.items():
        if value is not None:
            details[key] = value
    
    return details


def _capture_response_details(**kwargs) -> typing.Dict[str, typing.Any]:
    """Capture response details for telemetry (avoiding circular import)."""
    details = {}
    for key, value in kwargs.items():
        if value is not None:
            details[key] = value
    return details


def _instrument_sync_connect(original_connect, events: SocketEvents | None = None):
    """Wrap sync websockets.sync.client.connect to add telemetry."""
    
    @functools.wraps(original_connect)
    def instrumented_connect(uri, *args, additional_headers: typing.Dict[str, str] | None = None, **kwargs):
        start_time = time.perf_counter()
        
        # Capture detailed request information including all connection parameters
        request_details = _capture_request_details(
            method="WS_CONNECT",
            url=str(uri),
            headers=additional_headers,
            function_name="websockets.sync.client.connect",
            connection_args=args,
            connection_kwargs=kwargs,
        )
        
        # Emit connect event
        if events:
            try:
                events.on_ws_connect(
                    url=str(uri),
                    headers=additional_headers,
                    request_details=request_details,
                )
            except Exception:
                pass
        
        try:
            # Call original connect
            connection = original_connect(uri, *args, additional_headers=additional_headers, **kwargs)
            
            # Wrap the connection to capture close event
            if events:
                original_close = connection.close
                
                def instrumented_close(*close_args, **close_kwargs):
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    response_details = _capture_response_details(
                        status_code=1000,  # Normal close
                        duration_ms=duration_ms
                    )
                    
                    try:
                        events.on_ws_close(
                            url=str(uri),
                            duration_ms=duration_ms,
                            request_details=request_details,
                            response_details=response_details,
                        )
                    except Exception:
                        pass
                    
                    return original_close(*close_args, **close_kwargs)
                
                connection.close = instrumented_close
            
            return connection
            
        except Exception as error:
            import traceback
            
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Capture detailed error information
            response_details = _capture_response_details(
                error=error,
                duration_ms=duration_ms,
                error_type=type(error).__name__,
                error_message=str(error),
                stack_trace=traceback.format_exc(),
                function_name="websockets.sync.client.connect",
                timeout_occurred="timeout" in str(error).lower() or "timed out" in str(error).lower(),
            )
            
            # Capture WebSocket handshake response headers if available
            try:
                # Handle InvalidStatusCode exceptions (handshake failures)
                if error.__class__.__name__ == 'InvalidStatusCode':
                    # Status code is directly available
                    if hasattr(error, 'status_code'):
                        response_details["handshake_status_code"] = error.status_code
                    
                    # Headers are directly available as e.headers
                    if hasattr(error, 'headers') and error.headers:
                        response_details["handshake_response_headers"] = dict(error.headers)
                    
                    # Some versions might have response_headers
                    elif hasattr(error, 'response_headers') and error.response_headers:
                        response_details["handshake_response_headers"] = dict(error.response_headers)
                
                # Handle InvalidHandshake exceptions (protocol-level failures)
                elif error.__class__.__name__ == 'InvalidHandshake':
                    response_details["handshake_error_type"] = "InvalidHandshake"
                    if hasattr(error, 'headers') and error.headers:
                        response_details["handshake_response_headers"] = dict(error.headers)
                
                # Generic fallback for any exception with headers
                elif hasattr(error, 'headers') and error.headers:
                    response_details["handshake_response_headers"] = dict(error.headers)
                elif hasattr(error, 'response_headers') and error.response_headers:
                    response_details["handshake_response_headers"] = dict(error.response_headers)
                
                # Capture status code if available (for any exception type)
                if hasattr(error, 'status_code') and not response_details.get("handshake_status_code"):
                    response_details["handshake_status_code"] = error.status_code
                    
            except Exception:
                # Don't let header extraction fail the error handling
                pass
            
            if events:
                try:
                    events.on_ws_error(
                        url=str(uri),
                        error=error,
                        duration_ms=duration_ms,
                        request_details=request_details,
                        response_details=response_details,
                    )
                except Exception:
                    pass
            raise
    
    return instrumented_connect


def _instrument_async_connect(original_connect, events: SocketEvents | None = None):
    """Wrap async websockets.connect to add telemetry."""
    
    @functools.wraps(original_connect)
    def instrumented_connect(uri, *args, extra_headers: typing.Dict[str, str] | None = None, **kwargs):
        start_time = time.perf_counter()
        
        # Capture detailed request information including all connection parameters
        request_details = _capture_request_details(
            method="WS_CONNECT",
            url=str(uri),
            headers=extra_headers,
            function_name="websockets.client.connect",
            connection_args=args,
            connection_kwargs=kwargs,
        )
        
        # Emit connect event
        if events:
            try:
                events.on_ws_connect(
                    url=str(uri),
                    headers=extra_headers,
                    request_details=request_details,
                )
            except Exception:
                pass
        
        # Return an async context manager
        @asynccontextmanager
        async def instrumented_context():
            try:
                # Call original connect
                async with original_connect(uri, *args, extra_headers=extra_headers, **kwargs) as connection:
                    # Wrap the connection to capture close event
                    if events:
                        original_close = connection.close
                        
                        async def instrumented_close(*close_args, **close_kwargs):
                            duration_ms = (time.perf_counter() - start_time) * 1000
                            response_details = _capture_response_details(
                                status_code=1000,  # Normal close
                                duration_ms=duration_ms
                            )
                            
                            try:
                                events.on_ws_close(
                                    url=str(uri),
                                    duration_ms=duration_ms,
                                    request_details=request_details,
                                    response_details=response_details,
                                )
                            except Exception:
                                pass
                            
                            return await original_close(*close_args, **close_kwargs)
                        
                        connection.close = instrumented_close
                    
                    yield connection
                    
                    # Also emit close event when context exits (if connection wasn't manually closed)
                    if events:
                        try:
                            duration_ms = (time.perf_counter() - start_time) * 1000
                            response_details = _capture_response_details(
                                status_code=1000,  # Normal close
                                duration_ms=duration_ms
                            )
                            events.on_ws_close(
                                url=str(uri),
                                duration_ms=duration_ms,
                                request_details=request_details,
                                response_details=response_details,
                            )
                        except Exception:
                            pass
                            
            except Exception as error:
                import traceback
                
                duration_ms = (time.perf_counter() - start_time) * 1000
                
                # Capture detailed error information
                response_details = _capture_response_details(
                    error=error,
                    duration_ms=duration_ms,
                    error_type=type(error).__name__,
                    error_message=str(error),
                    stack_trace=traceback.format_exc(),
                    function_name="websockets.client.connect",
                    timeout_occurred="timeout" in str(error).lower() or "timed out" in str(error).lower(),
                )
                
                # Capture WebSocket handshake response headers if available
                try:
                    # Handle InvalidStatusCode exceptions (handshake failures)
                    if error.__class__.__name__ == 'InvalidStatusCode':
                        # Status code is directly available
                        if hasattr(error, 'status_code'):
                            response_details["handshake_status_code"] = error.status_code
                        
                        # Headers are directly available as e.headers
                        if hasattr(error, 'headers') and error.headers:
                            response_details["handshake_response_headers"] = dict(error.headers)
                        
                        # Some versions might have response_headers
                        elif hasattr(error, 'response_headers') and error.response_headers:
                            response_details["handshake_response_headers"] = dict(error.response_headers)
                    
                    # Handle InvalidHandshake exceptions (protocol-level failures)
                    elif error.__class__.__name__ == 'InvalidHandshake':
                        response_details["handshake_error_type"] = "InvalidHandshake"
                        if hasattr(error, 'headers') and error.headers:
                            response_details["handshake_response_headers"] = dict(error.headers)
                    
                    # Generic fallback for any exception with headers
                    elif hasattr(error, 'headers') and error.headers:
                        response_details["handshake_response_headers"] = dict(error.headers)
                    elif hasattr(error, 'response_headers') and error.response_headers:
                        response_details["handshake_response_headers"] = dict(error.response_headers)
                    
                    # Capture status code if available (for any exception type)
                    if hasattr(error, 'status_code') and not response_details.get("handshake_status_code"):
                        response_details["handshake_status_code"] = error.status_code
                        
                except Exception:
                    # Don't let header extraction fail the error handling
                    pass
                
                if events:
                    try:
                        events.on_ws_error(
                            url=str(uri),
                            error=error,
                            duration_ms=duration_ms,
                            request_details=request_details,
                            response_details=response_details,
                        )
                    except Exception:
                        pass
                raise
        
        return instrumented_context()
    
    return instrumented_connect


def apply_websocket_instrumentation(socket_events: SocketEvents | None = None):
    """Apply WebSocket instrumentation globally using monkey-patching."""
    try:
        # Patch sync websockets
        if not hasattr(websockets_sync_client.connect, '_deepgram_instrumented'):
            original_sync_connect = websockets_sync_client.connect
            websockets_sync_client.connect = _instrument_sync_connect(original_sync_connect, socket_events)
            websockets_sync_client.connect._deepgram_instrumented = True
    except Exception:
        pass
    
    try:
        # Patch async websockets (legacy)
        try:
            from websockets.legacy.client import connect as legacy_connect
            if not hasattr(legacy_connect, '_deepgram_instrumented'):
                instrumented_legacy = _instrument_async_connect(legacy_connect, socket_events)
                
                # Replace in the module
                import websockets.legacy.client as legacy_client
                legacy_client.connect = instrumented_legacy
                instrumented_legacy._deepgram_instrumented = True
        except ImportError:
            pass
        
        # Patch async websockets (current)
        try:
            from websockets import connect as current_connect
            if not hasattr(current_connect, '_deepgram_instrumented'):
                instrumented_current = _instrument_async_connect(current_connect, socket_events)
                
                # Replace in the module  
                import websockets
                websockets.connect = instrumented_current
                instrumented_current._deepgram_instrumented = True
        except ImportError:
            pass
            
    except Exception:
        pass
