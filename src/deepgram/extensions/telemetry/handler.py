from __future__ import annotations

import typing
from datetime import datetime

from .models import ErrorEvent, ErrorSeverity, TelemetryEvent


class TelemetryHandler:
    """
    Interface for SDK telemetry. Users can supply a custom implementation.
    All methods are optional to implement.
    """

    def on_http_request(
        self,
        *,
        method: str,
        url: str,
        headers: typing.Mapping[str, str] | None,
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        pass

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
    ) -> None:
        pass

    def on_http_error(
        self,
        *,
        method: str,
        url: str,
        error: BaseException,
        duration_ms: float,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        pass

    # WebSocket telemetry methods
    def on_ws_connect(
        self, 
        *, 
        url: str, 
        headers: typing.Mapping[str, str] | None, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        pass

    def on_ws_error(
        self, 
        *, 
        url: str, 
        error: BaseException, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        pass

    def on_ws_close(
        self, 
        *, 
        url: str,
    ) -> None:
        pass

    # Optional: global uncaught errors from sys/threading hooks
    def on_uncaught_error(self, *, error: BaseException) -> None:
        pass


class NoOpTelemetryHandler(TelemetryHandler):
    pass


