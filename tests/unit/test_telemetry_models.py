"""
Unit tests for telemetry models.
Tests the Pydantic models used for telemetry data structures.
"""

import pytest
import typing
from datetime import datetime, timezone
from enum import Enum
import pydantic

from deepgram.extensions.telemetry.models import (
    ErrorSeverity,
    TelemetryContext,
    TelemetryEvent,
    ErrorEvent
)


class TestErrorSeverity:
    """Test ErrorSeverity enum."""
    
    def test_error_severity_values(self):
        """Test that all error severity values are defined correctly."""
        assert ErrorSeverity.UNSPECIFIED == "ERROR_SEVERITY_UNSPECIFIED"
        assert ErrorSeverity.INFO == "ERROR_SEVERITY_INFO"
        assert ErrorSeverity.WARNING == "ERROR_SEVERITY_WARNING"
        assert ErrorSeverity.ERROR == "ERROR_SEVERITY_ERROR"
        assert ErrorSeverity.CRITICAL == "ERROR_SEVERITY_CRITICAL"
    
    def test_error_severity_is_string_enum(self):
        """Test that ErrorSeverity is a string enum."""
        assert issubclass(ErrorSeverity, str)
        assert issubclass(ErrorSeverity, Enum)
    
    def test_error_severity_string_representation(self):
        """Test string representation of error severity values."""
        # In Python, string enums return their value when converted to string
        assert ErrorSeverity.ERROR.value == "ERROR_SEVERITY_ERROR"
        assert ErrorSeverity.WARNING.value == "ERROR_SEVERITY_WARNING"
    
    def test_error_severity_comparison(self):
        """Test error severity comparison."""
        # String comparison should work
        assert ErrorSeverity.ERROR == "ERROR_SEVERITY_ERROR"
        assert ErrorSeverity.WARNING != "ERROR_SEVERITY_ERROR"
        
        # Enum comparison should work
        assert ErrorSeverity.ERROR == ErrorSeverity.ERROR
        assert ErrorSeverity.ERROR != ErrorSeverity.WARNING
    
    def test_error_severity_iteration(self):
        """Test that all error severity values can be iterated."""
        severities = list(ErrorSeverity)
        assert len(severities) == 5
        assert ErrorSeverity.UNSPECIFIED in severities
        assert ErrorSeverity.INFO in severities
        assert ErrorSeverity.WARNING in severities
        assert ErrorSeverity.ERROR in severities
        assert ErrorSeverity.CRITICAL in severities


class TestTelemetryContext:
    """Test TelemetryContext model."""
    
    def test_telemetry_context_creation_empty(self):
        """Test creating empty TelemetryContext."""
        context = TelemetryContext()
        
        assert context.package_name is None
        assert context.package_version is None
        assert context.language is None
        assert context.runtime_version is None
        assert context.os is None
        assert context.arch is None
        assert context.app_name is None
        assert context.app_version is None
        assert context.environment is None
        assert context.session_id is None
        assert context.installation_id is None
        assert context.project_id is None
    
    def test_telemetry_context_creation_full(self):
        """Test creating TelemetryContext with all fields."""
        context = TelemetryContext(
            package_name="python-sdk",
            package_version="3.2.1",
            language="python",
            runtime_version="python 3.11.6",
            os="darwin",
            arch="arm64",
            app_name="test_app",
            app_version="1.0.0",
            environment="test",
            session_id="session-123",
            installation_id="install-456",
            project_id="project-789"
        )
        
        assert context.package_name == "python-sdk"
        assert context.package_version == "3.2.1"
        assert context.language == "python"
        assert context.runtime_version == "python 3.11.6"
        assert context.os == "darwin"
        assert context.arch == "arm64"
        assert context.app_name == "test_app"
        assert context.app_version == "1.0.0"
        assert context.environment == "test"
        assert context.session_id == "session-123"
        assert context.installation_id == "install-456"
        assert context.project_id == "project-789"
    
    def test_telemetry_context_partial_fields(self):
        """Test creating TelemetryContext with partial fields."""
        context = TelemetryContext(
            package_name="python-sdk",
            package_version="3.2.1",
            language="python",
            environment="production"
        )
        
        assert context.package_name == "python-sdk"
        assert context.package_version == "3.2.1"
        assert context.language == "python"
        assert context.environment == "production"
        # Unspecified fields should be None
        assert context.runtime_version is None
        assert context.os is None
        assert context.arch is None
        assert context.app_name is None
        assert context.app_version is None
        assert context.session_id is None
        assert context.installation_id is None
        assert context.project_id is None
    
    def test_telemetry_context_serialization(self):
        """Test TelemetryContext serialization."""
        context = TelemetryContext(
            package_name="python-sdk",
            package_version="3.2.1",
            language="python",
            os="linux",
            arch="x86_64"
        )
        
        # Test model_dump (Pydantic v2) or dict (Pydantic v1)
        try:
            data = context.model_dump()
        except AttributeError:
            data = context.dict()
        
        assert data["package_name"] == "python-sdk"
        assert data["package_version"] == "3.2.1"
        assert data["language"] == "python"
        assert data["os"] == "linux"
        assert data["arch"] == "x86_64"
        assert data["runtime_version"] is None
    
    def test_telemetry_context_deserialization(self):
        """Test TelemetryContext deserialization."""
        data = {
            "package_name": "node-sdk",
            "package_version": "2.1.0",
            "language": "node",
            "runtime_version": "node 18.17.0",
            "os": "windows",
            "arch": "x64"
        }
        
        context = TelemetryContext(**data)
        
        assert context.package_name == "node-sdk"
        assert context.package_version == "2.1.0"
        assert context.language == "node"
        assert context.runtime_version == "node 18.17.0"
        assert context.os == "windows"
        assert context.arch == "x64"
    
    def test_telemetry_context_extra_fields_allowed(self):
        """Test that TelemetryContext allows extra fields."""
        # This should not raise due to extra="allow"
        context = TelemetryContext(
            package_name="python-sdk",
            custom_field="custom_value",
            another_field=123
        )
        
        assert context.package_name == "python-sdk"
        # Extra fields should be accessible (depending on Pydantic version)
        try:
            data = context.model_dump()
        except AttributeError:
            data = context.dict()
        
        assert "custom_field" in data or hasattr(context, 'custom_field')
    
    def test_telemetry_context_immutability(self):
        """Test that TelemetryContext is immutable (frozen=True)."""
        context = TelemetryContext(
            package_name="python-sdk",
            package_version="3.2.1"
        )
        
        # Should not be able to modify fields
        with pytest.raises((pydantic.ValidationError, AttributeError, TypeError)):
            context.package_name = "modified-sdk"
    
    def test_telemetry_context_unicode_values(self):
        """Test TelemetryContext with Unicode values."""
        context = TelemetryContext(
            package_name="python-sdk",
            app_name="测试应用",
            environment="тест",
            session_id="🚀session-123"
        )
        
        assert context.package_name == "python-sdk"
        assert context.app_name == "测试应用"
        assert context.environment == "тест"
        assert context.session_id == "🚀session-123"


class TestTelemetryEvent:
    """Test TelemetryEvent model."""
    
    def test_telemetry_event_creation_minimal(self):
        """Test creating minimal TelemetryEvent."""
        event_time = datetime.now(timezone.utc)
        event = TelemetryEvent(
            name="test.event",
            time=event_time
        )
        
        assert event.name == "test.event"
        assert event.time == event_time
        assert event.attributes is None
        assert event.metrics is None
    
    def test_telemetry_event_creation_full(self):
        """Test creating TelemetryEvent with all fields."""
        event_time = datetime.now(timezone.utc)
        attributes = {"service": "deepgram", "version": "3.2.1", "region": "us-east-1"}
        metrics = {"duration_ms": 150.5, "payload_size": 1024.0, "response_size": 2048.0}
        
        event = TelemetryEvent(
            name="http.request.completed",
            time=event_time,
            attributes=attributes,
            metrics=metrics
        )
        
        assert event.name == "http.request.completed"
        assert event.time == event_time
        assert event.attributes == attributes
        assert event.metrics == metrics
    
    def test_telemetry_event_missing_required_fields(self):
        """Test TelemetryEvent validation with missing required fields."""
        # Missing name
        with pytest.raises(pydantic.ValidationError) as exc_info:
            TelemetryEvent(time=datetime.now(timezone.utc))
        
        errors = exc_info.value.errors()
        field_names = [error["loc"][0] for error in errors]
        assert "name" in field_names
        
        # Missing time
        with pytest.raises(pydantic.ValidationError) as exc_info:
            TelemetryEvent(name="test.event")
        
        errors = exc_info.value.errors()
        field_names = [error["loc"][0] for error in errors]
        assert "time" in field_names
    
    def test_telemetry_event_wrong_types(self):
        """Test TelemetryEvent validation with wrong types."""
        # Wrong name type
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name=123,  # Should be string
                time=datetime.now(timezone.utc)
            )
        
        # Wrong time type
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name="test.event",
                time="not_a_datetime"  # Should be datetime
            )
        
        # Wrong attributes type
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name="test.event",
                time=datetime.now(timezone.utc),
                attributes="not_a_dict"  # Should be dict
            )
        
        # Wrong metrics type
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name="test.event",
                time=datetime.now(timezone.utc),
                metrics="not_a_dict"  # Should be dict
            )
    
    def test_telemetry_event_attributes_validation(self):
        """Test TelemetryEvent attributes validation."""
        event_time = datetime.now(timezone.utc)
        
        # Valid string attributes
        event = TelemetryEvent(
            name="test.event",
            time=event_time,
            attributes={"key1": "value1", "key2": "value2"}
        )
        assert event.attributes == {"key1": "value1", "key2": "value2"}
        
        # Invalid attributes (non-string values)
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name="test.event",
                time=event_time,
                attributes={"key1": "value1", "key2": 123}  # 123 is not string
            )
    
    def test_telemetry_event_metrics_validation(self):
        """Test TelemetryEvent metrics validation."""
        event_time = datetime.now(timezone.utc)
        
        # Valid float metrics
        event = TelemetryEvent(
            name="test.event",
            time=event_time,
            metrics={"metric1": 123.45, "metric2": 67.89}
        )
        assert event.metrics == {"metric1": 123.45, "metric2": 67.89}
        
        # Invalid metrics (non-float values)
        with pytest.raises(pydantic.ValidationError):
            TelemetryEvent(
                name="test.event",
                time=event_time,
                metrics={"metric1": 123.45, "metric2": "not_a_float"}
            )
    
    def test_telemetry_event_serialization(self):
        """Test TelemetryEvent serialization."""
        event_time = datetime(2023, 12, 1, 12, 0, 0, tzinfo=timezone.utc)
        event = TelemetryEvent(
            name="api.request",
            time=event_time,
            attributes={"method": "POST", "endpoint": "/v1/listen"},
            metrics={"duration_ms": 250.0, "size_bytes": 1024.0}
        )
        
        try:
            data = event.model_dump()
        except AttributeError:
            data = event.dict()
        
        assert data["name"] == "api.request"
        assert data["attributes"]["method"] == "POST"
        assert data["metrics"]["duration_ms"] == 250.0
    
    def test_telemetry_event_deserialization(self):
        """Test TelemetryEvent deserialization."""
        data = {
            "name": "websocket.error",
            "time": "2023-12-01T12:00:00Z",
            "attributes": {"url": "wss://api.deepgram.com", "error_type": "ConnectionError"},
            "metrics": {"reconnect_attempts": 3.0, "downtime_ms": 5000.0}
        }
        
        event = TelemetryEvent(**data)
        
        assert event.name == "websocket.error"
        assert event.attributes["url"] == "wss://api.deepgram.com"
        assert event.metrics["reconnect_attempts"] == 3.0
    
    def test_telemetry_event_immutability(self):
        """Test that TelemetryEvent is immutable."""
        event_time = datetime.now(timezone.utc)
        event = TelemetryEvent(
            name="test.event",
            time=event_time
        )
        
        # Should not be able to modify fields
        with pytest.raises((pydantic.ValidationError, AttributeError, TypeError)):
            event.name = "modified.event"
    
    def test_telemetry_event_extra_fields_allowed(self):
        """Test that TelemetryEvent allows extra fields."""
        event_time = datetime.now(timezone.utc)
        
        # This should not raise due to extra="allow"
        event = TelemetryEvent(
            name="test.event",
            time=event_time,
            custom_field="custom_value",
            another_field=123
        )
        
        assert event.name == "test.event"
        assert event.time == event_time
    
    def test_telemetry_event_unicode_values(self):
        """Test TelemetryEvent with Unicode values."""
        event_time = datetime.now(timezone.utc)
        event = TelemetryEvent(
            name="测试.事件",
            time=event_time,
            attributes={"描述": "тест", "emoji": "🚀"},
            metrics={"метрика": 123.45}
        )
        
        assert event.name == "测试.事件"
        assert event.attributes["描述"] == "тест"
        assert event.attributes["emoji"] == "🚀"
        assert event.metrics["метрика"] == 123.45


class TestErrorEvent:
    """Test ErrorEvent model."""
    
    def test_error_event_creation_minimal(self):
        """Test creating minimal ErrorEvent."""
        event_time = datetime.now(timezone.utc)
        event = ErrorEvent(
            type="ConnectionError",
            message="Connection failed",
            severity=ErrorSeverity.ERROR,
            time=event_time
        )
        
        assert event.type == "ConnectionError"
        assert event.message == "Connection failed"
        assert event.severity == ErrorSeverity.ERROR
        assert event.time == event_time
        assert event.stack_trace is None
        assert event.handled is False  # Default value
    
    def test_error_event_creation_full(self):
        """Test creating ErrorEvent with all fields."""
        event_time = datetime.now(timezone.utc)
        stack_trace = "Traceback (most recent call last):\n  File ...\nConnectionError: Connection failed"
        
        event = ErrorEvent(
            type="ConnectionError",
            message="Network timeout occurred",
            severity=ErrorSeverity.CRITICAL,
            time=event_time,
            stack_trace=stack_trace,
            handled=False
        )
        
        assert event.type == "ConnectionError"
        assert event.message == "Network timeout occurred"
        assert event.severity == ErrorSeverity.CRITICAL
        assert event.time == event_time
        assert event.stack_trace == stack_trace
        assert event.handled is False
    
    def test_error_event_missing_required_fields(self):
        """Test ErrorEvent validation with missing required fields."""
        event_time = datetime.now(timezone.utc)
        
        # All fields are optional except time, so we test missing time
        # Missing time (required field)
        with pytest.raises(pydantic.ValidationError) as exc_info:
            ErrorEvent(
                type="ConnectionError",
                message="Connection failed",
                severity=ErrorSeverity.ERROR
            )
        errors = exc_info.value.errors()
        field_names = [error["loc"][0] for error in errors]
        assert "time" in field_names
        
        # Since most fields are optional, let's just test that we can create
        # a minimal valid ErrorEvent
        minimal_event = ErrorEvent(time=event_time)
        assert minimal_event.time == event_time
        assert minimal_event.type is None
        assert minimal_event.message is None
        assert minimal_event.severity == ErrorSeverity.UNSPECIFIED  # Default value
    
    def test_error_event_wrong_types(self):
        """Test ErrorEvent validation with wrong types."""
        event_time = datetime.now(timezone.utc)
        
        # Wrong type field
        with pytest.raises(pydantic.ValidationError):
            ErrorEvent(
                type=123,  # Should be string
                message="Connection failed",
                severity=ErrorSeverity.ERROR,
                time=event_time
            )
        
        # Since most fields are optional and have default values,
        # let's test that the model accepts valid values
        valid_event = ErrorEvent(
            type="ConnectionError",
            message="Connection failed",
            severity=ErrorSeverity.ERROR,
            time=event_time,
            handled=True
        )
        
        assert valid_event.type == "ConnectionError"
        assert valid_event.message == "Connection failed"
        assert valid_event.severity == ErrorSeverity.ERROR
        assert valid_event.handled is True
    
    def test_error_event_severity_enum_values(self):
        """Test ErrorEvent with different severity values."""
        event_time = datetime.now(timezone.utc)
        
        for severity in ErrorSeverity:
            event = ErrorEvent(
                type="TestError",
                message="Test message",
                severity=severity,
                time=event_time
            )
            assert event.severity == severity
    
    def test_error_event_serialization(self):
        """Test ErrorEvent serialization."""
        event_time = datetime(2023, 12, 1, 12, 0, 0, tzinfo=timezone.utc)
        event = ErrorEvent(
            type="ValidationError",
            message="Invalid input data",
            severity=ErrorSeverity.WARNING,
            time=event_time,
            stack_trace="Stack trace here",
            handled=True
        )
        
        try:
            data = event.model_dump()
        except AttributeError:
            data = event.dict()
        
        assert data["type"] == "ValidationError"
        assert data["message"] == "Invalid input data"
        assert data["severity"] == "ERROR_SEVERITY_WARNING"
        assert data["stack_trace"] == "Stack trace here"
        assert data["handled"] is True
    
    def test_error_event_deserialization(self):
        """Test ErrorEvent deserialization."""
        data = {
            "type": "TimeoutError",
            "message": "Request timed out",
            "severity": "ERROR_SEVERITY_ERROR",
            "time": "2023-12-01T12:00:00Z",
            "stack_trace": "Traceback...",
            "handled": False
        }
        
        event = ErrorEvent(**data)
        
        assert event.type == "TimeoutError"
        assert event.message == "Request timed out"
        assert event.severity == ErrorSeverity.ERROR
        assert event.stack_trace == "Traceback..."
        assert event.handled is False
    
    def test_error_event_immutability(self):
        """Test that ErrorEvent is immutable."""
        event_time = datetime.now(timezone.utc)
        event = ErrorEvent(
            type="TestError",
            message="Test message",
            severity=ErrorSeverity.ERROR,
            time=event_time
        )
        
        # Should not be able to modify fields
        with pytest.raises((pydantic.ValidationError, AttributeError, TypeError)):
            event.type = "ModifiedError"
    
    def test_error_event_unicode_values(self):
        """Test ErrorEvent with Unicode values."""
        event_time = datetime.now(timezone.utc)
        event = ErrorEvent(
            type="УникодОшибка",
            message="测试错误消息 🚨",
            severity=ErrorSeverity.CRITICAL,
            time=event_time,
            stack_trace="Stack trace with тест unicode"
        )
        
        assert event.type == "УникодОшибка"
        assert event.message == "测试错误消息 🚨"
        assert "тест" in event.stack_trace
    
    def test_error_event_large_stack_trace(self):
        """Test ErrorEvent with large stack trace."""
        event_time = datetime.now(timezone.utc)
        large_stack_trace = "Traceback (most recent call last):\n" + "  Line of stack trace\n" * 1000
        
        event = ErrorEvent(
            type="LargeStackError",
            message="Error with large stack trace",
            severity=ErrorSeverity.ERROR,
            time=event_time,
            stack_trace=large_stack_trace
        )
        
        assert event.type == "LargeStackError"
        assert len(event.stack_trace) > 10000
        assert event.stack_trace.startswith("Traceback")


class TestTelemetryModelIntegration:
    """Test integration scenarios with telemetry models."""
    
    def test_complete_telemetry_scenario(self):
        """Test a complete telemetry scenario with all models."""
        # Create context
        context = TelemetryContext(
            package_name="python-sdk",
            package_version="3.2.1",
            language="python",
            runtime_version="python 3.11.6",
            os="darwin",
            arch="arm64",
            environment="production"
        )
        
        # Create telemetry event
        event_time = datetime.now(timezone.utc)
        telemetry_event = TelemetryEvent(
            name="http.request.completed",
            time=event_time,
            attributes={"method": "POST", "endpoint": "/v1/listen", "status": "success"},
            metrics={"duration_ms": 245.5, "payload_size": 1024.0, "response_size": 2048.0}
        )
        
        # Create error event
        error_event = ErrorEvent(
            type="ConnectionError",
            message="Network timeout during request",
            severity=ErrorSeverity.WARNING,
            time=event_time,
            handled=True
        )
        
        # Verify all models are properly created
        assert context.package_name == "python-sdk"
        assert telemetry_event.name == "http.request.completed"
        assert error_event.type == "ConnectionError"
        assert error_event.severity == ErrorSeverity.WARNING
    
    def test_model_serialization_consistency(self):
        """Test that all models serialize consistently."""
        event_time = datetime(2023, 12, 1, 12, 0, 0, tzinfo=timezone.utc)
        
        context = TelemetryContext(package_name="test-sdk", package_version="1.0.0")
        telemetry_event = TelemetryEvent(name="test.event", time=event_time)
        error_event = ErrorEvent(
            type="TestError",
            message="Test message",
            severity=ErrorSeverity.INFO,
            time=event_time
        )
        
        # All models should serialize without errors
        try:
            context_data = context.model_dump()
            telemetry_data = telemetry_event.model_dump()
            error_data = error_event.model_dump()
        except AttributeError:
            context_data = context.dict()
            telemetry_data = telemetry_event.dict()
            error_data = error_event.dict()
        
        # Verify basic structure
        assert isinstance(context_data, dict)
        assert isinstance(telemetry_data, dict)
        assert isinstance(error_data, dict)
        
        assert "package_name" in context_data
        assert "name" in telemetry_data
        assert "type" in error_data
    
    def test_model_validation_edge_cases(self):
        """Test model validation with edge cases."""
        event_time = datetime.now(timezone.utc)
        
        # Empty string values
        context = TelemetryContext(package_name="", package_version="")
        assert context.package_name == ""
        assert context.package_version == ""
        
        # Empty attributes and metrics
        telemetry_event = TelemetryEvent(
            name="test.event",
            time=event_time,
            attributes={},
            metrics={}
        )
        assert telemetry_event.attributes == {}
        assert telemetry_event.metrics == {}
        
        # Empty stack trace
        error_event = ErrorEvent(
            type="TestError",
            message="",
            severity=ErrorSeverity.UNSPECIFIED,
            time=event_time,
            stack_trace=""
        )
        assert error_event.message == ""
        assert error_event.stack_trace == ""
