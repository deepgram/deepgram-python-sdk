from __future__ import annotations

import time
import typing

import httpx
from ...core.file import File
from ...core.http_client import AsyncHttpClient as GeneratedAsyncHttpClient
from ...core.http_client import HttpClient as GeneratedHttpClient
from ...core.request_options import RequestOptions


class HttpEvents(typing.Protocol):
    def on_http_request(
        self,
        *,
        method: str,
        url: str,
        headers: typing.Mapping[str, str] | None,
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...

    def on_http_response(
        self,
        *,
        method: str,
        url: str,
        status_code: int,
        duration_ms: float,
        headers: typing.Mapping[str, str] | None,
        extras: typing.Mapping[str, str] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...

    def on_http_error(
        self,
        *,
        method: str,
        url: str,
        error: BaseException,
        duration_ms: float,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None: ...


def _compose_url(base_url: typing.Optional[str], path: typing.Optional[str]) -> str:
    if base_url is None or path is None:
        return ""
    return f"{base_url}/{path}" if not str(base_url).endswith("/") else f"{base_url}{path}"


class InstrumentedHttpClient(GeneratedHttpClient):
    def __init__(self, *, delegate: GeneratedHttpClient, events: HttpEvents | None):
        super().__init__(
            httpx_client=delegate.httpx_client,
            base_timeout=delegate.base_timeout,
            base_headers=delegate.base_headers,
            base_url=delegate.base_url,
        )
        self._delegate = delegate
        self._events = events

    def request(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[
            typing.Union[
                typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]],
                typing.List[typing.Tuple[str, File]],
            ]
        ] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 2,
        omit: typing.Optional[typing.Any] = None,
        force_multipart: typing.Optional[bool] = None,
    ) -> httpx.Response:
        url = _compose_url(base_url, path)

        start = time.perf_counter()
        try:
            if self._events is not None:
                # Filter request headers for telemetry extras
                try:
                    from .telemetry_events import (
                        capture_request_details,
                        # filter_sensitive_headers,  # No longer needed - using privacy-focused capture
                    )
                    # No longer filter headers - use privacy-focused request_details instead
                    extras = None
                    request_details = capture_request_details(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        json=json,
                        data=data,
                        files=files,
                        request_options=request_options,
                        retries=retries,
                        omit=omit,
                        force_multipart=force_multipart,
                    )
                except Exception:
                    extras = None
                    request_details = None
                
                self._events.on_http_request(
                    method=method, 
                    url=url or "", 
                    headers=headers, 
                    extras=extras,
                    request_details=request_details,
                )
        except Exception:
            pass
        try:
            resp = super().request(
                path=path,
                method=method,
                base_url=base_url,
                params=params,
                json=json,
                data=data,
                content=content,
                files=files,
                headers=headers,
                request_options=request_options,
                retries=retries,
                omit=omit,
                force_multipart=force_multipart,
            )
            duration_ms = (time.perf_counter() - start) * 1000.0
            try:
                if self._events is not None:
                    response_headers = typing.cast(typing.Mapping[str, str] | None, getattr(resp, "headers", None))
                    # Filter response headers for telemetry extras
                    try:
                        from .telemetry_events import (
                            capture_response_details,
                            # filter_sensitive_headers,  # No longer needed - using privacy-focused capture
                        )
                        # No longer filter response headers - use privacy-focused response_details instead
                        extras = None
                        response_details = capture_response_details(resp)
                    except Exception:
                        extras = None
                        response_details = None
                    
                    self._events.on_http_response(
                        method=method,
                        url=url or "",
                        status_code=resp.status_code,
                        duration_ms=duration_ms,
                        headers=response_headers,
                        extras=extras,
                        response_details=response_details,
                    )
            except Exception:
                pass
            return resp
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000.0
            try:
                if self._events is not None:
                    # Capture comprehensive error details
                    try:
                        from .telemetry_events import (
                            capture_request_details,
                            capture_response_details,
                        )
                        
                        # Capture full request details
                        request_details = capture_request_details(
                            method=method,
                            url=url,
                            headers=headers,
                            params=params,
                            json=json,
                            data=data,
                            files=files,
                            request_options=request_options,
                            retries=retries,
                            omit=omit,
                            force_multipart=force_multipart,
                        )
                        
                        # Try to capture response details from exception
                        response_details = {}
                        if hasattr(exc, 'response'):
                            response_details = capture_response_details(exc.response)
                        elif hasattr(exc, 'status_code'):
                            response_details['status_code'] = getattr(exc, 'status_code', None)
                        if hasattr(exc, 'headers'):
                            response_details['headers'] = dict(getattr(exc, 'headers', {}))
                            
                    except Exception:
                        request_details = None
                        response_details = None
                    
                    self._events.on_http_error(
                        method=method, 
                        url=url or "", 
                        error=exc, 
                        duration_ms=duration_ms,
                        request_details=request_details,
                        response_details=response_details,
                    )
            except Exception:
                pass
            raise

    # Inherit stream() from base class without modification


class InstrumentedAsyncHttpClient(GeneratedAsyncHttpClient):
    def __init__(self, *, delegate: GeneratedAsyncHttpClient, events: HttpEvents | None):
        super().__init__(
            httpx_client=delegate.httpx_client,
            base_timeout=delegate.base_timeout,
            base_headers=delegate.base_headers,
            base_url=delegate.base_url,
        )
        self._delegate = delegate
        self._events = events

    async def request(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[
            typing.Union[
                typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]],
                typing.List[typing.Tuple[str, File]],
            ]
        ] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 2,
        omit: typing.Optional[typing.Any] = None,
        force_multipart: typing.Optional[bool] = None,
    ) -> httpx.Response:
        url = _compose_url(base_url, path)

        start = time.perf_counter()
        try:
            if self._events is not None:
                # Filter request headers for telemetry extras
                try:
                    from .telemetry_events import (
                        capture_request_details,
                        # filter_sensitive_headers,  # No longer needed - using privacy-focused capture
                    )
                    # No longer filter headers - use privacy-focused request_details instead
                    extras = None
                    request_details = capture_request_details(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        json=json,
                        data=data,
                        files=files,
                        request_options=request_options,
                        retries=retries,
                        omit=omit,
                        force_multipart=force_multipart,
                    )
                except Exception:
                    extras = None
                    request_details = None
                
                self._events.on_http_request(
                    method=method, 
                    url=url or "", 
                    headers=headers, 
                    extras=extras,
                    request_details=request_details,
                )
        except Exception:
            pass
        try:
            resp = await super().request(
                path=path,
                method=method,
                base_url=base_url,
                params=params,
                json=json,
                data=data,
                content=content,
                files=files,
                headers=headers,
                request_options=request_options,
                retries=retries,
                omit=omit,
                force_multipart=force_multipart,
            )
            duration_ms = (time.perf_counter() - start) * 1000.0
            try:
                if self._events is not None:
                    response_headers = typing.cast(typing.Mapping[str, str] | None, getattr(resp, "headers", None))
                    # Filter response headers for telemetry extras
                    try:
                        from .telemetry_events import (
                            capture_response_details,
                            # filter_sensitive_headers,  # No longer needed - using privacy-focused capture
                        )
                        # No longer filter response headers - use privacy-focused response_details instead
                        extras = None
                        response_details = capture_response_details(resp)
                    except Exception:
                        extras = None
                        response_details = None
                    
                    self._events.on_http_response(
                        method=method,
                        url=url or "",
                        status_code=resp.status_code,
                        duration_ms=duration_ms,
                        headers=response_headers,
                        extras=extras,
                        response_details=response_details,
                    )
            except Exception:
                pass
            return resp
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000.0
            try:
                if self._events is not None:
                    # Capture comprehensive error details
                    try:
                        from .telemetry_events import (
                            capture_request_details,
                            capture_response_details,
                        )
                        
                        # Capture full request details
                        request_details = capture_request_details(
                            method=method,
                            url=url,
                            headers=headers,
                            params=params,
                            json=json,
                            data=data,
                            files=files,
                            request_options=request_options,
                            retries=retries,
                            omit=omit,
                            force_multipart=force_multipart,
                        )
                        
                        # Try to capture response details from exception
                        response_details = {}
                        if hasattr(exc, 'response'):
                            response_details = capture_response_details(exc.response)
                        elif hasattr(exc, 'status_code'):
                            response_details['status_code'] = getattr(exc, 'status_code', None)
                        if hasattr(exc, 'headers'):
                            response_details['headers'] = dict(getattr(exc, 'headers', {}))
                            
                    except Exception:
                        request_details = None
                        response_details = None
                    
                    self._events.on_http_error(
                        method=method, 
                        url=url or "", 
                        error=exc, 
                        duration_ms=duration_ms,
                        request_details=request_details,
                        response_details=response_details,
                    )
            except Exception:
                pass
            raise

    # Inherit stream() from base class without modification


