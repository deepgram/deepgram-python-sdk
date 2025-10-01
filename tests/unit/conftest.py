"""
Shared fixtures and configuration for unit tests.
"""
from typing import Any, Dict

import pytest


@pytest.fixture
def sample_timestamp():
    """Sample timestamp for testing."""
    return "2023-01-01T00:00:00Z"


@pytest.fixture
def sample_request_id():
    """Sample request ID for testing."""
    return "test-request-123"


@pytest.fixture
def sample_channel_data():
    """Sample channel data for testing."""
    return [0, 1]


@pytest.fixture
def sample_audio_data():
    """Sample binary audio data for testing."""
    return b"\x00\x01\x02\x03\x04\x05" * 100


@pytest.fixture
def sample_transcription_text():
    """Sample transcription text."""
    return "Hello, this is a test transcription."


@pytest.fixture
def sample_metadata():
    """Sample metadata for various events."""
    return {
        "request_id": "test-request-123",
        "sha256": "abc123def456",
        "created": "2023-01-01T00:00:00Z",
        "duration": 1.5,
        "channels": 1
    }


@pytest.fixture
def sample_function_call():
    """Sample function call data for Agent testing."""
    return {
        "id": "func-123",
        "name": "get_weather",
        "arguments": '{"location": "New York"}',
        "client_side": False
    }


@pytest.fixture
def valid_model_data():
    """Factory for creating valid model test data."""
    def _create_data(model_type: str, **overrides) -> Dict[str, Any]:
        """Create valid data for different model types."""
        base_data = {
            "listen_v1_metadata": {
                "type": "Metadata",
                "request_id": "test-123",
                "sha256": "abc123",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.0,
                "channels": 1
            },
            "listen_v1_results": {
                "type": "Results",
                "channel_index": [0],
                "duration": 1.0,
                "start": 0.0,
                "is_final": True,
                "channel": {
                    "alternatives": [
                        {
                            "transcript": "Hello world",
                            "confidence": 0.95,
                            "words": []
                        }
                    ]
                },
                "metadata": {
                    "request_id": "test-123",
                    "model_info": {
                        "name": "nova-2-general",
                        "version": "1.0",
                        "arch": "nova"
                    },
                    "model_uuid": "model-uuid-123"
                }
            },
            "speak_v1_metadata": {
                "type": "Metadata",
                "request_id": "speak-123",
                "model_name": "aura-asteria-en",
                "model_version": "1.0",
                "model_uuid": "uuid-123"
            },
            "agent_v1_welcome": {
                "type": "Welcome",
                "request_id": "req-123"
            },
            "agent_v1_conversation_text": {
                "type": "ConversationText",
                "role": "assistant",
                "content": "Hello!"
            },
            "agent_v1_function_call_request": {
                "type": "FunctionCallRequest",
                "functions": [
                    {
                        "id": "func-123",
                        "name": "get_weather",
                        "arguments": "{}",
                        "client_side": False
                    }
                ]
            }
        }
        
        data = base_data.get(model_type, {})
        data.update(overrides)
        return data
    
    return _create_data


@pytest.fixture
def invalid_model_data():
    """Factory for creating invalid model test data."""
    def _create_invalid_data(model_type: str, field_to_break: str) -> Dict[str, Any]:
        """Create invalid data by removing or corrupting specific fields."""
        valid_data = {
            "listen_v1_metadata": {
                "type": "Metadata",
                "request_id": "test-123",
                "sha256": "abc123",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.0,
                "channels": 1
            }
        }
        
        data = valid_data.get(model_type, {}).copy()
        
        # Remove or corrupt the specified field
        if field_to_break in data:
            if field_to_break == "type":
                data[field_to_break] = "InvalidType"
            elif field_to_break in ["duration", "channels"]:
                data[field_to_break] = "not_a_number"
            else:
                del data[field_to_break]
        
        return data
    
    return _create_invalid_data
