"""
Unit tests for telemetry handler infrastructure.
Tests the base TelemetryHandler interface and custom implementations.
"""

import pytest
import typing
import time
from unittest.mock import Mock, patch

from deepgram.extensions.telemetry.handler import TelemetryHandler


class TestTelemetryHandler:
    """Test the base TelemetryHandler interface."""
    
    def test_handler_interface_methods_exist(self):
        """Test that all interface methods exist and are callable."""
        handler = TelemetryHandler()
        
        # HTTP methods
        assert callable(handler.on_http_request)
        assert callable(handler.on_http_response)
        assert callable(handler.on_http_error)
        
        # WebSocket methods
        assert callable(handler.on_ws_connect)
        assert callable(handler.on_ws_error)
        assert callable(handler.on_ws_close)
        
        # Uncaught error method
        assert callable(handler.on_uncaught_error)
    
    def test_handler_methods_do_nothing_by_default(self):
        """Test that default implementation methods do nothing (no exceptions)."""
        handler = TelemetryHandler()
        
        # HTTP methods should not raise
        handler.on_http_request(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            headers={"Authorization": "Token test"},
            extras={"client": "python-sdk"},
            request_details={"request_id": "test-123"}
        )
        
        handler.on_http_response(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            status_code=200,
            duration_ms=150.5,
            headers={"content-type": "application/json"},
            extras={"client": "python-sdk"},
            response_details={"request_id": "test-123"}
        )
        
        handler.on_http_error(
            method="POST",
            url="https://api.deepgram.com/v1/test",
            error=Exception("Test error"),
            duration_ms=1000.0,
            request_details={"request_id": "test-456"},
            response_details={"status_code": 500}
        )
        
        # WebSocket methods should not raise
        handler.on_ws_connect(
            url="wss://api.deepgram.com/v1/listen",
            headers={"Authorization": "Token test"},
            extras={"version": "v1"},
            request_details={"session_id": "ws-123"}
        )
        
        handler.on_ws_error(
            url="wss://api.deepgram.com/v1/listen",
            error=ConnectionError("Connection lost"),
            extras={"reconnect": "true"},
            request_details={"session_id": "ws-123"},
            response_details={"code": 1006}
        )
        
        handler.on_ws_close(url="wss://api.deepgram.com/v1/listen")
        
        # Uncaught error method should not raise
        handler.on_uncaught_error(error=RuntimeError("Uncaught error"))


class CustomTelemetryHandler(TelemetryHandler):
    """Custom implementation for testing inheritance."""
    
    def __init__(self):
        self.events = []
    
    def on_http_request(
        self,
        *,
        method: str,
        url: str,
        headers: typing.Mapping[str, str] | None,
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        self.events.append({
            "type": "http_request",
            "method": method,
            "url": url,
            "headers": dict(headers) if headers is not None else None,
            "extras": dict(extras) if extras is not None else None,
            "request_details": dict(request_details) if request_details is not None else None,
        })
    
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
        self.events.append({
            "type": "http_response",
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "headers": dict(headers) if headers else None,
            "extras": dict(extras) if extras else None,
            "response_details": dict(response_details) if response_details else None,
        })
    
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
        self.events.append({
            "type": "http_error",
            "method": method,
            "url": url,
            "error": str(error),
            "error_type": type(error).__name__,
            "duration_ms": duration_ms,
            "request_details": dict(request_details) if request_details else None,
            "response_details": dict(response_details) if response_details else None,
        })
    
    def on_ws_connect(
        self, 
        *, 
        url: str, 
        headers: typing.Mapping[str, str] | None, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        self.events.append({
            "type": "ws_connect",
            "url": url,
            "headers": dict(headers) if headers else None,
            "extras": dict(extras) if extras else None,
            "request_details": dict(request_details) if request_details else None,
        })
    
    def on_ws_error(
        self, 
        *, 
        url: str, 
        error: BaseException, 
        extras: typing.Mapping[str, str] | None = None,
        request_details: typing.Mapping[str, typing.Any] | None = None,
        response_details: typing.Mapping[str, typing.Any] | None = None,
    ) -> None:
        self.events.append({
            "type": "ws_error",
            "url": url,
            "error": str(error),
            "error_type": type(error).__name__,
            "extras": dict(extras) if extras else None,
            "request_details": dict(request_details) if request_details else None,
            "response_details": dict(response_details) if response_details else None,
        })
    
    def on_ws_close(
        self, 
        *, 
        url: str,
    ) -> None:
        self.events.append({
            "type": "ws_close",
            "url": url,
        })
    
    def on_uncaught_error(self, *, error: BaseException) -> None:
        self.events.append({
            "type": "uncaught_error",
            "error": str(error),
            "error_type": type(error).__name__,
        })


class TestCustomTelemetryHandler:
    """Test custom telemetry handler implementation."""
    
    def test_custom_handler_inheritance(self):
        """Test that custom handler properly inherits from base."""
        handler = CustomTelemetryHandler()
        assert isinstance(handler, TelemetryHandler)
    
    def test_http_request_tracking(self):
        """Test HTTP request event tracking."""
        handler = CustomTelemetryHandler()
        
        handler.on_http_request(
            method="POST",
            url="https://api.deepgram.com/v1/listen",
            headers={"Authorization": "Token abc123", "Content-Type": "application/json"},
            extras={"sdk": "python", "version": "3.2.1"},
            request_details={"request_id": "req-456", "payload_size": 1024}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "http_request"
        assert event["method"] == "POST"
        assert event["url"] == "https://api.deepgram.com/v1/listen"
        assert event["headers"]["Authorization"] == "Token abc123"
        assert event["extras"]["sdk"] == "python"
        assert event["request_details"]["request_id"] == "req-456"
    
    def test_http_response_tracking(self):
        """Test HTTP response event tracking."""
        handler = CustomTelemetryHandler()
        
        handler.on_http_response(
            method="GET",
            url="https://api.deepgram.com/v1/projects",
            status_code=200,
            duration_ms=245.7,
            headers={"content-type": "application/json"},
            extras={"region": "us-east-1"},
            response_details={"request_id": "req-789", "response_size": 2048}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "http_response"
        assert event["method"] == "GET"
        assert event["status_code"] == 200
        assert event["duration_ms"] == 245.7
        assert event["headers"]["content-type"] == "application/json"
        assert event["extras"]["region"] == "us-east-1"
        assert event["response_details"]["response_size"] == 2048
    
    def test_http_error_tracking(self):
        """Test HTTP error event tracking."""
        handler = CustomTelemetryHandler()
        
        test_error = ConnectionError("Network timeout")
        handler.on_http_error(
            method="PUT",
            url="https://api.deepgram.com/v1/models",
            error=test_error,
            duration_ms=5000.0,
            request_details={"request_id": "req-error", "retry_count": 2},
            response_details={"status_code": 503, "server_error": "Service Unavailable"}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "http_error"
        assert event["method"] == "PUT"
        assert event["error"] == "Network timeout"
        assert event["error_type"] == "ConnectionError"
        assert event["duration_ms"] == 5000.0
        assert event["request_details"]["retry_count"] == 2
        assert event["response_details"]["status_code"] == 503
    
    def test_websocket_connect_tracking(self):
        """Test WebSocket connection event tracking."""
        handler = CustomTelemetryHandler()
        
        handler.on_ws_connect(
            url="wss://api.deepgram.com/v1/speak",
            headers={"Authorization": "Token xyz789"},
            extras={"protocol": "websocket", "version": "v1"},
            request_details={"session_id": "ws-connect-123"}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "ws_connect"
        assert event["url"] == "wss://api.deepgram.com/v1/speak"
        assert event["headers"]["Authorization"] == "Token xyz789"
        assert event["extras"]["protocol"] == "websocket"
        assert event["request_details"]["session_id"] == "ws-connect-123"
    
    def test_websocket_error_tracking(self):
        """Test WebSocket error event tracking."""
        handler = CustomTelemetryHandler()
        
        ws_error = ConnectionError("WebSocket connection closed unexpectedly")
        handler.on_ws_error(
            url="wss://api.deepgram.com/v1/agent",
            error=ws_error,
            extras={"reconnect_attempt": "3"},
            request_details={"session_id": "ws-error-456"},
            response_details={"close_code": 1006, "close_reason": "Abnormal closure"}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "ws_error"
        assert event["url"] == "wss://api.deepgram.com/v1/agent"
        assert event["error"] == "WebSocket connection closed unexpectedly"
        assert event["error_type"] == "ConnectionError"
        assert event["extras"]["reconnect_attempt"] == "3"
        assert event["response_details"]["close_code"] == 1006
    
    def test_websocket_close_tracking(self):
        """Test WebSocket close event tracking."""
        handler = CustomTelemetryHandler()
        
        handler.on_ws_close(url="wss://api.deepgram.com/v1/listen")
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "ws_close"
        assert event["url"] == "wss://api.deepgram.com/v1/listen"
    
    def test_uncaught_error_tracking(self):
        """Test uncaught error event tracking."""
        handler = CustomTelemetryHandler()
        
        uncaught_error = RuntimeError("Unexpected application error")
        handler.on_uncaught_error(error=uncaught_error)
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["type"] == "uncaught_error"
        assert event["error"] == "Unexpected application error"
        assert event["error_type"] == "RuntimeError"
    
    def test_multiple_events_tracking(self):
        """Test tracking multiple events in sequence."""
        handler = CustomTelemetryHandler()
        
        # HTTP request
        handler.on_http_request(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            headers={"Authorization": "Token test"},
        )
        
        # HTTP response
        handler.on_http_response(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            status_code=200,
            duration_ms=100.0,
            headers={"content-type": "application/json"},
        )
        
        # WebSocket connect
        handler.on_ws_connect(
            url="wss://api.deepgram.com/v1/listen",
            headers={"Authorization": "Token test"},
        )
        
        # WebSocket close
        handler.on_ws_close(url="wss://api.deepgram.com/v1/listen")
        
        assert len(handler.events) == 4
        assert handler.events[0]["type"] == "http_request"
        assert handler.events[1]["type"] == "http_response"
        assert handler.events[2]["type"] == "ws_connect"
        assert handler.events[3]["type"] == "ws_close"
    
    def test_handler_with_none_values(self):
        """Test handler methods with None optional parameters."""
        handler = CustomTelemetryHandler()
        
        # Test with minimal parameters (None optionals)
        handler.on_http_request(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            headers=None,
            extras=None,
            request_details=None
        )
        
        handler.on_ws_connect(
            url="wss://api.deepgram.com/v1/listen",
            headers=None,
            extras=None,
            request_details=None
        )
        
        assert len(handler.events) == 2
        assert handler.events[0]["headers"] is None
        assert handler.events[0]["extras"] is None
        assert handler.events[0]["request_details"] is None
        assert handler.events[1]["headers"] is None
        assert handler.events[1]["extras"] is None
        assert handler.events[1]["request_details"] is None


class TestTelemetryHandlerEdgeCases:
    """Test edge cases and error scenarios for telemetry handlers."""
    
    def test_handler_with_empty_collections(self):
        """Test handler with empty dictionaries."""
        handler = CustomTelemetryHandler()
        
        handler.on_http_request(
            method="GET",
            url="https://api.deepgram.com/v1/test",
            headers={},
            extras={},
            request_details={}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        # Empty dicts are converted to empty dicts, not None
        assert event["headers"] == {}
        assert event["extras"] == {}
        assert event["request_details"] == {}
    
    def test_handler_with_unicode_data(self):
        """Test handler with Unicode strings."""
        handler = CustomTelemetryHandler()
        
        handler.on_http_request(
            method="POST",
            url="https://api.deepgram.com/v1/测试",
            headers={"User-Agent": "SDK测试"},
            extras={"description": "тест"},
            request_details={"message": "🚀 Test"}
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert "测试" in event["url"]
        assert event["headers"]["User-Agent"] == "SDK测试"
        assert event["extras"]["description"] == "тест"
        assert event["request_details"]["message"] == "🚀 Test"
    
    def test_handler_with_large_data(self):
        """Test handler with large data structures."""
        handler = CustomTelemetryHandler()
        
        large_headers = {f"header_{i}": f"value_{i}" for i in range(100)}
        large_extras = {f"extra_{i}": f"data_{i}" for i in range(50)}
        
        handler.on_http_response(
            method="POST",
            url="https://api.deepgram.com/v1/large",
            status_code=200,
            duration_ms=2500.0,
            headers=large_headers,
            extras=large_extras,
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert len(event["headers"]) == 100
        assert len(event["extras"]) == 50
        assert event["headers"]["header_50"] == "value_50"
        assert event["extras"]["extra_25"] == "data_25"
    
    def test_handler_with_nested_error_details(self):
        """Test handler with complex nested error details."""
        handler = CustomTelemetryHandler()
        
        complex_error = ValueError("Complex validation error")
        nested_details = {
            "error_context": {
                "validation_errors": [
                    {"field": "audio", "message": "Invalid format"},
                    {"field": "model", "message": "Not supported"}
                ],
                "request_metadata": {
                    "timestamp": time.time(),
                    "client_version": "3.2.1",
                    "feature_flags": {"new_models": True, "beta_features": False}
                }
            }
        }
        
        handler.on_http_error(
            method="POST",
            url="https://api.deepgram.com/v1/validate",
            error=complex_error,
            duration_ms=150.0,
            response_details=nested_details
        )
        
        assert len(handler.events) == 1
        event = handler.events[0]
        assert event["error_type"] == "ValueError"
        assert event["response_details"]["error_context"]["validation_errors"][0]["field"] == "audio"
        assert event["response_details"]["error_context"]["request_metadata"]["client_version"] == "3.2.1"
        assert event["response_details"]["error_context"]["request_metadata"]["feature_flags"]["new_models"] is True
