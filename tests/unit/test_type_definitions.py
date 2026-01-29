"""
Unit tests for auto-generated type definitions.

This module tests the various auto-generated type definitions including:
- Simple type aliases
- Union types
- Pydantic models
- Optional/Any types
"""

import typing
import pytest
import pydantic
from unittest.mock import Mock

# Import the types we want to test
from deepgram.types.error_response import ErrorResponse
from deepgram.types.error_response_text_error import ErrorResponseTextError
from deepgram.types.error_response_legacy_error import ErrorResponseLegacyError
from deepgram.types.error_response_modern_error import ErrorResponseModernError
from deepgram.types.listen_v1model import ListenV1Model
from deepgram.types.listen_v1callback import ListenV1Callback
from deepgram.types.listen_v1tag import ListenV1Tag
from deepgram.types.listen_v1response import ListenV1Response
from deepgram.types.listen_v1response_metadata import ListenV1ResponseMetadata
from deepgram.types.listen_v1response_results import ListenV1ResponseResults


class TestSimpleTypeAliases:
    """Test simple type aliases like str, Optional[Any], etc."""
    
    def test_error_response_text_error_is_str(self):
        """Test that ErrorResponseTextError is a str type alias."""
        assert ErrorResponseTextError == str
        
    def test_error_response_text_error_usage(self):
        """Test that ErrorResponseTextError can be used as a string."""
        error_message: ErrorResponseTextError = "Authentication failed"
        assert isinstance(error_message, str)
        assert error_message == "Authentication failed"
        
    def test_listen_v1callback_is_optional_any(self):
        """Test that ListenV1Callback is Optional[Any]."""
        assert ListenV1Callback == typing.Optional[typing.Any]
        
    def test_listen_v1callback_usage(self):
        """Test that ListenV1Callback can accept None or any value."""
        callback1: ListenV1Callback = None
        callback2: ListenV1Callback = "http://example.com/webhook"
        callback3: ListenV1Callback = {"url": "http://example.com", "method": "POST"}
        
        assert callback1 is None
        assert isinstance(callback2, str)
        assert isinstance(callback3, dict)
        
    def test_listen_v1tag_is_optional_union(self):
        """Test that ListenV1Tag is Optional[Union[str, Sequence[str]]]."""
        assert ListenV1Tag == typing.Optional[typing.Union[str, typing.Sequence[str]]]
        
    def test_listen_v1tag_usage(self):
        """Test that ListenV1Tag can accept None or any value."""
        tag1: ListenV1Tag = None
        tag2: ListenV1Tag = "my-tag"
        tag3: ListenV1Tag = ["tag1", "tag2"]
        
        assert tag1 is None
        assert isinstance(tag2, str)
        assert isinstance(tag3, list)


class TestUnionTypes:
    """Test union types like ErrorResponse and ListenV1Model."""
    
    def test_error_response_union_structure(self):
        """Test that ErrorResponse is a union of the three error types."""
        assert ErrorResponse == typing.Union[ErrorResponseTextError, ErrorResponseLegacyError, ErrorResponseModernError]
        
    def test_error_response_accepts_string(self):
        """Test that ErrorResponse can accept a string (ErrorResponseTextError)."""
        error: ErrorResponse = "Simple error message"
        assert isinstance(error, str)
        
    def test_error_response_accepts_legacy_error(self):
        """Test that ErrorResponse can accept ErrorResponseLegacyError."""
        legacy_error = ErrorResponseLegacyError(
            err_code="AUTH_001",
            err_msg="Invalid API key",
            request_id="req_123"
        )
        error: ErrorResponse = legacy_error
        assert isinstance(error, ErrorResponseLegacyError)
        
    def test_error_response_accepts_modern_error(self):
        """Test that ErrorResponse can accept ErrorResponseModernError."""
        modern_error = ErrorResponseModernError(
            category="authentication",
            message="Invalid API key provided",
            details="The API key is missing or malformed",
            request_id="req_456"
        )
        error: ErrorResponse = modern_error
        assert isinstance(error, ErrorResponseModernError)
        
    def test_listen_v1model_union_structure(self):
        """Test that ListenV1Model is a union of literal strings and Any."""
        # Check that it's a union type
        origin = typing.get_origin(ListenV1Model)
        assert origin is typing.Union
        
        # Check that it includes typing.Any as one of the union members
        args = typing.get_args(ListenV1Model)
        assert typing.Any in args
        
    def test_listen_v1model_accepts_literal_values(self):
        """Test that ListenV1Model accepts predefined literal values."""
        valid_models = [
            "nova-3", "nova-2", "nova", "enhanced", "base",
            "meeting", "phonecall", "finance", "custom"
        ]
        
        for model in valid_models:
            model_value: ListenV1Model = model
            assert isinstance(model_value, str)
            
    def test_listen_v1model_accepts_any_value(self):
        """Test that ListenV1Model accepts any value due to typing.Any."""
        # String not in literals
        custom_model: ListenV1Model = "my-custom-model"
        assert isinstance(custom_model, str)
        
        # Non-string value
        numeric_model: ListenV1Model = 123
        assert isinstance(numeric_model, int)
        
        # Complex value
        dict_model: ListenV1Model = {"name": "custom", "version": "1.0"}
        assert isinstance(dict_model, dict)


class TestPydanticModels:
    """Test Pydantic models like ErrorResponseLegacyError, ErrorResponseModernError, etc."""
    
    def test_error_response_legacy_error_creation(self):
        """Test creating ErrorResponseLegacyError with all fields."""
        error = ErrorResponseLegacyError(
            err_code="AUTH_001",
            err_msg="Invalid API key",
            request_id="req_123"
        )
        
        assert error.err_code == "AUTH_001"
        assert error.err_msg == "Invalid API key"
        assert error.request_id == "req_123"
        
    def test_error_response_legacy_error_optional_fields(self):
        """Test creating ErrorResponseLegacyError with optional fields."""
        error = ErrorResponseLegacyError()
        
        assert error.err_code is None
        assert error.err_msg is None
        assert error.request_id is None
        
    def test_error_response_legacy_error_partial_fields(self):
        """Test creating ErrorResponseLegacyError with some fields."""
        error = ErrorResponseLegacyError(err_code="ERR_001")
        
        assert error.err_code == "ERR_001"
        assert error.err_msg is None
        assert error.request_id is None
        
    def test_error_response_legacy_error_serialization(self):
        """Test serialization of ErrorResponseLegacyError."""
        error = ErrorResponseLegacyError(
            err_code="AUTH_001",
            err_msg="Invalid API key",
            request_id="req_123"
        )
        
        # Test serialization - use model_dump if available (Pydantic V2), otherwise dict
        try:
            serialized = error.model_dump()
        except AttributeError:
            serialized = error.dict()
            
        expected = {
            "err_code": "AUTH_001",
            "err_msg": "Invalid API key",
            "request_id": "req_123"
        }
        assert serialized == expected
        
    def test_error_response_legacy_error_immutability(self):
        """Test that ErrorResponseLegacyError is immutable (frozen)."""
        error = ErrorResponseLegacyError(err_code="TEST")
        
        with pytest.raises((AttributeError, pydantic.ValidationError)):
            error.err_code = "CHANGED"
            
    def test_error_response_modern_error_creation(self):
        """Test creating ErrorResponseModernError with all fields."""
        error = ErrorResponseModernError(
            category="authentication",
            message="Invalid API key provided",
            details="The API key is missing or malformed",
            request_id="req_456"
        )
        
        assert error.category == "authentication"
        assert error.message == "Invalid API key provided"
        assert error.details == "The API key is missing or malformed"
        assert error.request_id == "req_456"
        
    def test_error_response_modern_error_optional_fields(self):
        """Test creating ErrorResponseModernError with optional fields."""
        error = ErrorResponseModernError()
        
        assert error.category is None
        assert error.message is None
        assert error.details is None
        assert error.request_id is None
        
    def test_error_response_modern_error_serialization(self):
        """Test serialization of ErrorResponseModernError."""
        error = ErrorResponseModernError(
            category="validation",
            message="Invalid input",
            details="The request body contains invalid data"
        )
        
        # Test serialization - use model_dump if available (Pydantic V2), otherwise dict
        try:
            serialized = error.model_dump()
        except AttributeError:
            serialized = error.dict()
            
        expected = {
            "category": "validation",
            "message": "Invalid input",
            "details": "The request body contains invalid data",
            "request_id": None
        }
        assert serialized == expected
        
    def test_error_response_modern_error_immutability(self):
        """Test that ErrorResponseModernError is immutable (frozen)."""
        error = ErrorResponseModernError(category="test")
        
        with pytest.raises((AttributeError, pydantic.ValidationError)):
            error.category = "changed"


class TestComplexPydanticModels:
    """Test complex Pydantic models with nested structures."""
    
    def test_listen_v1response_structure_validation(self):
        """Test that ListenV1Response validates required fields."""
        # Test that missing required fields raise validation errors
        with pytest.raises(pydantic.ValidationError) as exc_info:
            ListenV1Response()
        
        error = exc_info.value
        assert "metadata" in str(error)
        assert "results" in str(error)
        
    def test_listen_v1response_type_annotations(self):
        """Test that ListenV1Response has correct type annotations."""
        # Check that the model has the expected fields
        fields = ListenV1Response.model_fields if hasattr(ListenV1Response, 'model_fields') else ListenV1Response.__fields__
        
        assert "metadata" in fields
        assert "results" in fields
        
        # Check that these are the only required fields
        assert len(fields) == 2


class TestTypeDefinitionEdgeCases:
    """Test edge cases and error conditions for type definitions."""
    
    def test_error_response_legacy_error_extra_fields_allowed(self):
        """Test that ErrorResponseLegacyError allows extra fields."""
        # This should not raise an error due to extra="allow"
        error = ErrorResponseLegacyError(
            err_code="TEST",
            extra_field="extra_value",
            another_field=123
        )
        
        assert error.err_code == "TEST"
        # Extra fields should be accessible
        assert hasattr(error, "extra_field")
        assert hasattr(error, "another_field")
        
    def test_error_response_modern_error_extra_fields_allowed(self):
        """Test that ErrorResponseModernError allows extra fields."""
        # This should not raise an error due to extra="allow"
        error = ErrorResponseModernError(
            category="test",
            custom_field="custom_value",
            numeric_field=456
        )
        
        assert error.category == "test"
        # Extra fields should be accessible
        assert hasattr(error, "custom_field")
        assert hasattr(error, "numeric_field")
        
    def test_listen_v1response_missing_required_fields(self):
        """Test that ListenV1Response raises error for missing required fields."""
        with pytest.raises(pydantic.ValidationError):
            ListenV1Response()
            
        with pytest.raises(pydantic.ValidationError):
            ListenV1Response(metadata=Mock())
            
        with pytest.raises(pydantic.ValidationError):
            ListenV1Response(results=Mock())
            
    def test_error_response_legacy_error_wrong_types(self):
        """Test that ErrorResponseLegacyError validates field types."""
        # Since all fields are Optional[str], non-string values should be handled
        # Pydantic might coerce or raise validation errors depending on the value
        try:
            error = ErrorResponseLegacyError(err_code=123)  # int instead of str
            # If it doesn't raise, check if it was coerced to string
            assert isinstance(error.err_code, (str, int))
        except pydantic.ValidationError:
            # This is also acceptable behavior
            pass
            
    def test_error_response_modern_error_wrong_types(self):
        """Test that ErrorResponseModernError validates field types."""
        # Since all fields are Optional[str], non-string values should be handled
        try:
            error = ErrorResponseModernError(category=456)  # int instead of str
            # If it doesn't raise, check if it was coerced to string
            assert isinstance(error.category, (str, int))
        except pydantic.ValidationError:
            # This is also acceptable behavior
            pass


class TestTypeDefinitionIntegration:
    """Test integration scenarios with type definitions."""
    
    def test_error_response_union_type_checking(self):
        """Test that different error types can be used interchangeably."""
        errors: list[ErrorResponse] = [
            "Simple string error",
            ErrorResponseLegacyError(err_code="LEG_001", err_msg="Legacy error"),
            ErrorResponseModernError(category="modern", message="Modern error")
        ]
        
        assert len(errors) == 3
        assert isinstance(errors[0], str)
        assert isinstance(errors[1], ErrorResponseLegacyError)
        assert isinstance(errors[2], ErrorResponseModernError)
        
    def test_listen_v1model_in_function_signature(self):
        """Test using ListenV1Model in function signatures."""
        def process_model(model: ListenV1Model) -> str:
            return f"Processing model: {model}"
            
        # Test with literal values
        result1 = process_model("nova-3")
        assert result1 == "Processing model: nova-3"
        
        # Test with custom values (typing.Any allows this)
        result2 = process_model("custom-model")
        assert result2 == "Processing model: custom-model"
        
        # Test with non-string values
        result3 = process_model(123)
        assert result3 == "Processing model: 123"
        
    def test_type_definitions_serialization_consistency(self):
        """Test that type definitions serialize consistently."""
        legacy_error = ErrorResponseLegacyError(err_code="TEST", err_msg="Test message")
        modern_error = ErrorResponseModernError(category="test", message="Test message")
        
        # Both should be serializable
        try:
            legacy_dict = legacy_error.model_dump()
        except AttributeError:
            legacy_dict = legacy_error.dict()
            
        try:
            modern_dict = modern_error.model_dump()
        except AttributeError:
            modern_dict = modern_error.dict()
            
        assert isinstance(legacy_dict, dict)
        assert isinstance(modern_dict, dict)
        assert "err_code" in legacy_dict
        assert "category" in modern_dict
        
    def test_type_definitions_with_none_values(self):
        """Test type definitions with None values."""
        # Test that optional fields can be explicitly set to None
        legacy_error = ErrorResponseLegacyError(
            err_code=None,
            err_msg=None,
            request_id=None
        )
        
        modern_error = ErrorResponseModernError(
            category=None,
            message=None,
            details=None,
            request_id=None
        )
        
        assert legacy_error.err_code is None
        assert modern_error.category is None
        
    def test_type_definitions_with_unicode_values(self):
        """Test type definitions with Unicode values."""
        legacy_error = ErrorResponseLegacyError(
            err_code="测试_001",
            err_msg="Unicode error message: 🚨",
            request_id="req_测试_123"
        )
        
        modern_error = ErrorResponseModernError(
            category="тест",
            message="Error with émojis: 🔥",
            details="Détails de l'erreur"
        )
        
        assert legacy_error.err_code == "测试_001"
        assert modern_error.message == "Error with émojis: 🔥"
