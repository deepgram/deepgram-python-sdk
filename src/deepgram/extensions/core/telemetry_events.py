from __future__ import annotations

from typing import Any, Mapping

from ..telemetry.handler import TelemetryHandler
from .instrumented_http import HttpEvents
from .instrumented_socket import SocketEvents


class TelemetryHttpEvents(HttpEvents):
    def __init__(self, handler: TelemetryHandler):
        self._handler = handler

    def on_http_request(
        self, 
        *, 
        method: str, 
        url: str, 
        headers: Mapping[str, str] | None, 
        extras: Mapping[str, str] | None = None,
        request_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_http_request(
                method=method, 
                url=url, 
                headers=headers, 
                extras=extras,
                request_details=request_details,
            )
        except Exception:
            pass

    def on_http_response(
        self,
        *,
        method: str,
        url: str,
        status_code: int,
        duration_ms: float,
        headers: Mapping[str, str] | None,
        extras: Mapping[str, str] | None = None,
        response_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_http_response(
                method=method,
                url=url,
                status_code=status_code,
                duration_ms=duration_ms,
                headers=headers,
                extras=extras,
                response_details=response_details,
            )
        except Exception:
            pass

    def on_http_error(
        self, 
        *, 
        method: str, 
        url: str, 
        error: BaseException, 
        duration_ms: float,
        request_details: Mapping[str, Any] | None = None,
        response_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_http_error(
                method=method, 
                url=url, 
                error=error, 
                duration_ms=duration_ms,
                request_details=request_details,
                response_details=response_details,
            )
        except Exception:
            pass


class TelemetrySocketEvents(SocketEvents):
    """Implementation of WebSocket events that forwards to a telemetry handler."""
    
    def __init__(self, handler: TelemetryHandler):
        self._handler = handler
    
    def on_ws_connect(
        self,
        *,
        url: str,
        headers: Mapping[str, str] | None = None,
        extras: Mapping[str, str] | None = None,
        request_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_ws_connect(
                url=url,
                headers=headers,
                extras=extras,
                request_details=request_details,
            )
        except Exception:
            pass
    
    def on_ws_error(
        self,
        *,
        url: str,
        error: BaseException,
        duration_ms: float,
        request_details: Mapping[str, Any] | None = None,
        response_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_ws_error(
                url=url,
                error=error,
                extras=None,
                request_details=request_details,
                response_details=response_details,
            )
        except Exception:
            pass
    
    def on_ws_close(
        self,
        *,
        url: str,
        duration_ms: float,
        request_details: Mapping[str, Any] | None = None,
        response_details: Mapping[str, Any] | None = None,
    ) -> None:
        try:
            self._handler.on_ws_close(
                url=url,
                extras=None,
            )
        except Exception:
            pass


def filter_sensitive_headers(headers: Mapping[str, str] | None) -> dict[str, str] | None:
    """Filter out sensitive headers from telemetry, keeping all safe headers."""
    if not headers:
        return None
    
    # Headers to exclude from telemetry for security
    sensitive_prefixes = ('authorization', 'sec-', 'cookie', 'x-api-key', 'x-auth')
    sensitive_headers = {'authorization', 'cookie', 'set-cookie', 'x-api-key', 'x-auth-token', 'bearer'}
    
    filtered_headers = {}
    for key, value in headers.items():
        key_lower = key.lower()
        
        # Skip sensitive headers
        if key_lower in sensitive_headers:
            continue
        if any(key_lower.startswith(prefix) for prefix in sensitive_prefixes):
            continue
            
        filtered_headers[key] = str(value)
    
    return filtered_headers if filtered_headers else None


def extract_deepgram_headers(headers: Mapping[str, str] | None) -> dict[str, str] | None:
    """Extract x-dg-* headers from response headers."""
    if not headers:
        return None
    
    dg_headers = {}
    for key, value in headers.items():
        if key.lower().startswith('x-dg-'):
            dg_headers[key.lower()] = str(value)
    
    return dg_headers if dg_headers else None


def capture_request_details(
    method: str | None = None,
    url: str | None = None, 
    headers: Mapping[str, str] | None = None,
    params: Mapping[str, Any] | None = None,
    **kwargs
) -> dict[str, Any]:
    """Capture comprehensive request details for telemetry (keys only for privacy)."""
    details = {}
    
    if method:
        details['method'] = method
    
    # For URL, capture the structure but not query parameters with values
    if url:
        details['url_structure'] = _extract_url_structure(url)
    
    # For headers, capture only the keys (not values) for privacy
    if headers:
        details['header_keys'] = sorted(list(headers.keys()))
        details['header_count'] = len(headers)
    
    # For query parameters, capture only the keys (not values) for privacy  
    if params:
        details['param_keys'] = sorted(list(params.keys()))
        details['param_count'] = len(params)
    
    # For body content, capture type information but not actual content
    if 'json' in kwargs and kwargs['json'] is not None:
        details['has_json_body'] = True
        details['json_body_type'] = type(kwargs['json']).__name__
    
    if 'data' in kwargs and kwargs['data'] is not None:
        details['has_data_body'] = True
        details['data_body_type'] = type(kwargs['data']).__name__
        
    if 'content' in kwargs and kwargs['content'] is not None:
        details['has_content_body'] = True
        details['content_body_type'] = type(kwargs['content']).__name__
        
    if 'files' in kwargs and kwargs['files'] is not None:
        details['has_files'] = True
        details['files_type'] = type(kwargs['files']).__name__
    
    # Capture any additional request context (excluding sensitive data)
    safe_kwargs = ['timeout', 'follow_redirects', 'max_redirects']
    for key in safe_kwargs:
        if key in kwargs and kwargs[key] is not None:
            details[key] = kwargs[key]
    
    return details


def _extract_url_structure(url: str) -> dict[str, Any]:
    """Extract URL structure without exposing sensitive query parameter values."""
    try:
        from urllib.parse import parse_qs, urlparse
        
        parsed = urlparse(url)
        structure = {
            'scheme': parsed.scheme,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path,
        }
        
        # For query string, only capture the parameter keys, not values
        if parsed.query:
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            structure['query_param_keys'] = sorted(list(query_params.keys()))
            structure['query_param_count'] = len(query_params)
        
        return structure
    except Exception:
        # If URL parsing fails, just return a safe representation
        return {'url_parse_error': True, 'url_length': len(url)}


def capture_response_details(response: Any = None, **kwargs) -> dict[str, Any]:
    """Capture comprehensive response details for telemetry (keys only for privacy)."""
    details = {}
    
    if response is not None:
        # Try to extract common response attributes
        try:
            if hasattr(response, 'status_code'):
                details['status_code'] = response.status_code
            if hasattr(response, 'headers'):
                # For response headers, capture only keys (not values) for privacy
                headers = response.headers
                details['response_header_keys'] = sorted(list(headers.keys()))
                details['response_header_count'] = len(headers)
                
                # Extract request_id for server-side correlation (this is safe to log)
                request_id = (headers.get('x-request-id') or 
                            headers.get('X-Request-Id') or 
                            headers.get('x-dg-request-id') or 
                             headers.get('X-DG-Request-Id') or 
                             headers.get('request-id') or
                             headers.get('Request-Id'))
                if request_id:
                    details['request_id'] = request_id
                    
            if hasattr(response, 'reason_phrase'):
                details['reason_phrase'] = response.reason_phrase
            if hasattr(response, 'url'):
                # For response URL, capture structure but not full URL
                details['response_url_structure'] = _extract_url_structure(str(response.url))
        except Exception:
            pass
    
    # Capture any additional response context (excluding sensitive data)
    safe_kwargs = ['duration_ms', 'error', 'error_type', 'error_message', 'stack_trace', 
                   'timeout_occurred', 'function_name']
    for key in safe_kwargs:
        if key in kwargs and kwargs[key] is not None:
            details[key] = kwargs[key]
    
    # Also capture any other non-sensitive context
    for key, value in kwargs.items():
        if (key not in safe_kwargs and 
            value is not None and 
            key not in ['headers', 'params', 'json', 'data', 'content']):  # Exclude potentially sensitive data
            details[key] = value
            
    return details



