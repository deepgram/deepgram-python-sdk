"""
Unit tests for core data models and utilities.
"""
import pytest
from pydantic import ValidationError

# Import core utility models
from deepgram.extensions.telemetry.models import TelemetryEvent, TelemetryContext
from deepgram.core.api_error import ApiError
from deepgram.environment import DeepgramClientEnvironment


class TestTelemetryModels:
    """Test telemetry-related models."""
    
    def test_valid_telemetry_event(self):
        """Test creating a valid telemetry event."""
        from datetime import datetime
        event = TelemetryEvent(
            name="connection_started",
            time=datetime.now(),
            attributes={"connection_type": "websocket"},
            metrics={}
        )
        
        assert event.name == "connection_started"
        assert event.time is not None
        assert event.attributes["connection_type"] == "websocket"
        assert event.metrics == {}
    
    def test_telemetry_event_serialization(self):
        """Test telemetry event serialization."""
        from datetime import datetime
        event = TelemetryEvent(
            name="audio_sent",
            time=datetime.now(),
            attributes={"bytes_sent": "1024"},
            metrics={"latency": 50.5}
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["name"] == "audio_sent"
        assert event_dict["attributes"]["bytes_sent"] == "1024"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"name":"audio_sent"' in json_str
        assert '"bytes_sent":"1024"' in json_str
    
    def test_telemetry_event_missing_required_fields(self):
        """Test telemetry event with missing required fields."""
        # Missing name
        from datetime import datetime
        with pytest.raises(ValidationError) as exc_info:
            TelemetryEvent(
                time=datetime.now(),
                attributes={},
                metrics={}
            )
        assert "name" in str(exc_info.value)
        
        # Missing time
        from datetime import datetime
        with pytest.raises(ValidationError) as exc_info:
            TelemetryEvent(
                name="connection_started",
                attributes={},
                metrics={}
            )
        assert "time" in str(exc_info.value)
    
    def test_telemetry_event_optional_metadata(self):
        """Test telemetry event with optional metadata."""
        from datetime import datetime
        # Event without attributes/metrics
        event = TelemetryEvent(
            name="connection_closed",
            time=datetime.now(),
            attributes={},
            metrics={}
        )
        
        assert event.attributes == {}
        assert event.metrics == {}
        
        # Event with complex attributes and metrics
        complex_attributes = {
            "connection_type": "websocket",
            "bytes_sent": "1024",
            "bytes_received": "2048",
            "error_count": "0",
            "model_name": "nova-2-general",
            "model_version": "1.0"
        }
        
        complex_metrics = {
            "connection_duration": 30.5,
            "latency": 150.0
        }
        
        event_with_data = TelemetryEvent(
            name="connection_summary",
            time=datetime.now(),
            attributes=complex_attributes,
            metrics=complex_metrics
        )
        
        assert event_with_data.attributes["bytes_sent"] == "1024"
        assert event_with_data.attributes["model_name"] == "nova-2-general"
        assert event_with_data.metrics["connection_duration"] == 30.5
    
    def test_telemetry_context_model(self):
        """Test telemetry context model."""
        context = TelemetryContext(
            session_id="session-123",
            request_id="req-456"
        )
        
        assert context.session_id == "session-123"
        assert context.request_id == "req-456"
    
    def test_telemetry_context_serialization(self):
        """Test telemetry context serialization."""
        context = TelemetryContext(
            session_id="session-123",
            request_id="req-456"
        )
        
        # Test dict conversion
        context_dict = context.model_dump()
        assert context_dict["session_id"] == "session-123"
        assert context_dict["request_id"] == "req-456"
        
        # Test JSON serialization
        json_str = context.model_dump_json()
        assert '"session_id":"session-123"' in json_str
        assert '"request_id":"req-456"' in json_str


class TestApiError:
    """Test ApiError model."""
    
    def test_api_error_creation(self):
        """Test creating an API error."""
        error = ApiError(
            status_code=401,
            body="Unauthorized: Invalid API key"
        )
        
        assert error.status_code == 401
        assert error.body == "Unauthorized: Invalid API key"
        assert "401" in str(error)
        assert "Unauthorized" in str(error)
    
    def test_api_error_with_headers(self):
        """Test API error with headers."""
        headers = {
            "Content-Type": "application/json",
            "X-RateLimit-Remaining": "0"
        }
        
        error = ApiError(
            status_code=429,
            body="Rate limit exceeded",
            headers=headers
        )
        
        assert error.status_code == 429
        assert error.headers["Content-Type"] == "application/json"
        assert error.headers["X-RateLimit-Remaining"] == "0"
    
    def test_api_error_common_scenarios(self):
        """Test common API error scenarios."""
        # 400 Bad Request
        bad_request = ApiError(
            status_code=400,
            body="Bad Request: Invalid parameters"
        )
        assert bad_request.status_code == 400
        
        # 401 Unauthorized
        unauthorized = ApiError(
            status_code=401,
            body="Unauthorized: Invalid API key"
        )
        assert unauthorized.status_code == 401
        
        # 403 Forbidden
        forbidden = ApiError(
            status_code=403,
            body="Forbidden: Insufficient permissions"
        )
        assert forbidden.status_code == 403
        
        # 404 Not Found
        not_found = ApiError(
            status_code=404,
            body="Not Found: Resource does not exist"
        )
        assert not_found.status_code == 404
        
        # 429 Too Many Requests
        rate_limit = ApiError(
            status_code=429,
            body="Too Many Requests: Rate limit exceeded"
        )
        assert rate_limit.status_code == 429
        
        # 500 Internal Server Error
        server_error = ApiError(
            status_code=500,
            body="Internal Server Error"
        )
        assert server_error.status_code == 500
    
    def test_api_error_json_body(self):
        """Test API error with JSON body."""
        json_body = '{"error": {"message": "Invalid model", "type": "validation_error"}}'
        
        error = ApiError(
            status_code=400,
            body=json_body
        )
        
        assert error.status_code == 400
        assert "validation_error" in error.body
        assert "Invalid model" in error.body
    
    def test_api_error_empty_body(self):
        """Test API error with empty body."""
        error = ApiError(
            status_code=500,
            body=""
        )
        
        assert error.status_code == 500
        assert error.body == ""


class TestDeepgramClientEnvironment:
    """Test DeepgramClientEnvironment enum."""
    
    def test_environment_values(self):
        """Test environment enum values."""
        # Test production environment
        prod_env = DeepgramClientEnvironment.PRODUCTION
        assert prod_env is not None
        
        # Test that we can access the production URL
        assert hasattr(prod_env, 'production') or str(prod_env) == "https://api.deepgram.com"
    
    def test_environment_string_representation(self):
        """Test environment string representation."""
        prod_env = DeepgramClientEnvironment.PRODUCTION
        env_str = str(prod_env)
        
        # Should contain a valid URL
        assert "https://" in env_str or "deepgram" in env_str.lower()
    
    def test_environment_comparison(self):
        """Test environment comparison."""
        env1 = DeepgramClientEnvironment.PRODUCTION
        env2 = DeepgramClientEnvironment.PRODUCTION
        
        # Same environments should be equal
        assert env1 == env2
        assert env1 is env2  # Enum instances should be the same object


class TestCoreModelIntegration:
    """Integration tests for core models."""
    
    def test_telemetry_event_comprehensive_scenarios(self):
        """Test comprehensive telemetry event scenarios."""
        # Connection lifecycle events
        connection_events = [
            {
                "event_type": "connection_started",
                "metadata": {"connection_type": "websocket", "url": "wss://api.deepgram.com"}
            },
            {
                "event_type": "audio_sent",
                "metadata": {"bytes_sent": "1024", "chunk_count": "1"}
            },
            {
                "event_type": "transcription_received",
                "metadata": {"transcript_length": "50", "confidence": "0.95"}
            },
            {
                "event_type": "connection_closed",
                "metadata": {"duration": "30.5", "reason": "client_disconnect"}
            }
        ]
        
        from datetime import datetime, timedelta
        for i, event_data in enumerate(connection_events):
            event = TelemetryEvent(
                name=event_data["event_type"],
                time=datetime.now() + timedelta(seconds=i),
                attributes=event_data["metadata"],
                metrics={}
            )
            
            assert event.name == event_data["event_type"]
            assert event.time is not None
            assert event.attributes == event_data["metadata"]
    
    def test_api_error_with_telemetry_context(self):
        """Test API error in the context of telemetry."""
        # Simulate an error that would generate telemetry
        error = ApiError(
            status_code=429,
            body="Rate limit exceeded",
            headers={"X-RateLimit-Reset": "1609459200"}
        )
        
        # Create a telemetry event for this error
        from datetime import datetime
        error_event = TelemetryEvent(
            name="api_error",
            time=datetime.now(),
            attributes={
                "status_code": str(error.status_code),
                "error_body": error.body,
                "rate_limit_reset": error.headers.get("X-RateLimit-Reset") if error.headers else None
            },
            metrics={}
        )
        
        assert error_event.attributes["status_code"] == "429"
        assert error_event.attributes["error_body"] == "Rate limit exceeded"
        assert error_event.attributes["rate_limit_reset"] == "1609459200"
    
    def test_telemetry_headers_structure(self):
        """Test telemetry-related headers structure."""
        telemetry_headers = {
            "X-Deepgram-Session-ID": "session-123",
            "X-Deepgram-Request-ID": "req-456",
            "X-Deepgram-SDK-Version": "1.0.0",
            "X-Deepgram-Platform": "python"
        }
        
        # Test that we can create and validate header structures
        assert telemetry_headers["X-Deepgram-Session-ID"] == "session-123"
        assert telemetry_headers["X-Deepgram-Request-ID"] == "req-456"
        assert telemetry_headers["X-Deepgram-SDK-Version"] == "1.0.0"
        assert telemetry_headers["X-Deepgram-Platform"] == "python"
    
    def test_model_serialization_consistency(self):
        """Test that all models serialize consistently."""
        # Test telemetry event
        from datetime import datetime
        event = TelemetryEvent(
            name="test_event",
            time=datetime.now(),
            attributes={"test": "True"},
            metrics={"value": 42.0}
        )
        
        # Serialize and deserialize
        json_str = event.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_event = TelemetryEvent(**parsed_data)
        
        assert event.name == reconstructed_event.name
        # Compare timestamps allowing for timezone differences during serialization
        assert event.time.replace(tzinfo=None) == reconstructed_event.time.replace(tzinfo=None)
        assert event.attributes == reconstructed_event.attributes
        assert event.metrics == reconstructed_event.metrics
    
    def test_model_validation_edge_cases(self):
        """Test model validation edge cases."""
        # Test with very long strings
        from datetime import datetime
        long_name = "test_event_" + "x" * 10000
        event = TelemetryEvent(
            name=long_name,
            time=datetime.now(),
            attributes={},
            metrics={}
        )
        assert len(event.name) > 10000
        
        # Test with complex string attributes (since attributes must be Dict[str, str])
        complex_attributes = {
            "connection_type": "websocket",
            "bytes_sent": "1024",
            "bytes_received": "2048",
            "error_count": "0",
            "model_name": "nova-2-general",
            "model_version": "1.0"
        }
        
        event_with_complex_attributes = TelemetryEvent(
            name="complex_test",
            time=datetime.now(),
            attributes=complex_attributes,
            metrics={}
        )
        
        assert event_with_complex_attributes.attributes["bytes_sent"] == "1024"
        assert event_with_complex_attributes.attributes["model_name"] == "nova-2-general"
    
    def test_error_handling_comprehensive(self):
        """Test comprehensive error handling scenarios."""
        # Test various error status codes with realistic bodies
        error_scenarios = [
            (400, '{"error": "Invalid request format"}'),
            (401, '{"error": "Authentication failed", "code": "AUTH_001"}'),
            (403, '{"error": "Access denied", "resource": "/v1/listen"}'),
            (404, '{"error": "Model not found", "model": "invalid-model"}'),
            (422, '{"error": "Validation failed", "fields": ["model", "language"]}'),
            (429, '{"error": "Rate limit exceeded", "retry_after": 60}'),
            (500, '{"error": "Internal server error", "incident_id": "inc-123"}'),
            (502, '{"error": "Bad gateway", "upstream": "transcription-service"}'),
            (503, '{"error": "Service unavailable", "maintenance": true}')
        ]
        
        for status_code, body in error_scenarios:
            error = ApiError(
                status_code=status_code,
                body=body,
                headers={"Content-Type": "application/json"}
            )
            
            assert error.status_code == status_code
            assert "error" in error.body
            assert error.headers["Content-Type"] == "application/json"
