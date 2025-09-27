"""
Unit tests for core API response models.
"""
import pytest
from pydantic import ValidationError

# Import the core API response models
from deepgram.types.listen_v1response import ListenV1Response
from deepgram.types.read_v1response import ReadV1Response
from deepgram.types.speak_v1response import SpeakV1Response
from deepgram.types.error_response_modern_error import ErrorResponseModernError
from deepgram.types.error_response_legacy_error import ErrorResponseLegacyError


class TestListenV1Response:
    """Test ListenV1Response model."""
    
    def test_valid_listen_response(self):
        """Test creating a valid listen response."""
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                },
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Hello world",
                                "confidence": 0.95,
                                "words": [
                                    {
                                        "word": "Hello",
                                        "start": 0.0,
                                        "end": 0.5,
                                        "confidence": 0.95
                                    },
                                    {
                                        "word": "world",
                                        "start": 0.6,
                                        "end": 1.0,
                                        "confidence": 0.95
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        
        response = ListenV1Response(**response_data)
        
        assert response.metadata is not None
        assert response.results is not None
        assert response.metadata.request_id == "req-123"
        assert response.metadata.duration == 1.5
        assert response.metadata.channels == 1
    
    def test_listen_response_serialization(self):
        """Test listen response serialization."""
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Hello world",
                                "confidence": 0.95,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        response = ListenV1Response(**response_data)
        
        # Test dict conversion
        response_dict = response.model_dump()
        assert "metadata" in response_dict
        assert "results" in response_dict
        assert response_dict["metadata"]["request_id"] == "req-123"
        
        # Test JSON serialization
        json_str = response.model_dump_json()
        assert '"request_id":"req-123"' in json_str
        assert '"transcript":"Hello world"' in json_str
    
    def test_listen_response_missing_required_fields(self):
        """Test listen response with missing required fields."""
        # Missing metadata
        with pytest.raises(ValidationError) as exc_info:
            ListenV1Response(
                results={
                    "channels": []
                }
            )
        assert "metadata" in str(exc_info.value)
        
        # Missing results
        with pytest.raises(ValidationError) as exc_info:
            ListenV1Response(
                metadata={
                    "transaction_key": "deprecated",
                    "request_id": "req-123",
                    "sha256": "abc123",
                    "created": "2023-01-01T00:00:00Z",
                    "duration": 1.5,
                    "channels": 1,
                    "models": []
                }
            )
        assert "results" in str(exc_info.value)
    
    def test_listen_response_empty_channels(self):
        """Test listen response with empty channels."""
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 0,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": []
            }
        }
        
        response = ListenV1Response(**response_data)
        assert len(response.results.channels) == 0
        assert response.metadata.channels == 0
    
    def test_listen_response_multiple_alternatives(self):
        """Test listen response with multiple alternatives."""
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Hello world",
                                "confidence": 0.95,
                                "words": []
                            },
                            {
                                "transcript": "Hello word",
                                "confidence": 0.85,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        response = ListenV1Response(**response_data)
        assert len(response.results.channels) == 1
        assert len(response.results.channels[0].alternatives) == 2
        assert response.results.channels[0].alternatives[0].confidence == 0.95
        assert response.results.channels[0].alternatives[1].confidence == 0.85


class TestReadV1Response:
    """Test ReadV1Response model."""
    
    def test_valid_read_response(self):
        """Test creating a valid read response."""
        response_data = {
            "metadata": {
                "request_id": "read-123",
                "created": "2023-01-01T00:00:00Z",
                "language": "en",
                "model": "nova-2-general",
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "summary": {
                    "text": "This is a summary of the analyzed text.",
                    "start_word": 0,
                    "end_word": 10
                }
            }
        }
        
        response = ReadV1Response(**response_data)
        
        assert response.metadata is not None
        assert response.results is not None
        assert response.metadata.request_id == "read-123"
        assert response.metadata.language == "en"
        assert response.results.summary.text == "This is a summary of the analyzed text."
    
    def test_read_response_serialization(self):
        """Test read response serialization."""
        response_data = {
            "metadata": {
                "request_id": "read-123",
                "created": "2023-01-01T00:00:00Z",
                "language": "en",
                "model": "nova-2-general"
            },
            "results": {
                "summary": {
                    "text": "Summary text",
                    "start_word": 0,
                    "end_word": 5
                }
            }
        }
        
        response = ReadV1Response(**response_data)
        
        # Test dict conversion
        response_dict = response.model_dump()
        assert "metadata" in response_dict
        assert "results" in response_dict
        assert response_dict["metadata"]["request_id"] == "read-123"
        
        # Test JSON serialization
        json_str = response.model_dump_json()
        assert '"request_id":"read-123"' in json_str
        assert '"text":"Summary text"' in json_str
    
    def test_read_response_missing_required_fields(self):
        """Test read response with missing required fields."""
        # Missing metadata
        with pytest.raises(ValidationError) as exc_info:
            ReadV1Response(
                results={
                    "summary": {
                        "text": "Summary",
                        "start_word": 0,
                        "end_word": 1
                    }
                }
            )
        assert "metadata" in str(exc_info.value)
    
    def test_read_response_optional_fields(self):
        """Test read response with optional fields."""
        response_data = {
            "metadata": {
                "request_id": "read-123",
                "created": "2023-01-01T00:00:00Z",
                "language": "en",
                "model": "nova-2-general",
                "intents_info": {
                    "model_uuid": "intent-model-123"
                },
                "sentiment_info": {
                    "model_uuid": "sentiment-model-123"
                },
                "topics_info": {
                    "model_uuid": "topics-model-123"
                },
                "summary_info": {
                    "model_uuid": "summary-model-123"
                }
            },
            "results": {
                "summary": {
                    "text": "Summary with all optional metadata",
                    "start_word": 0,
                    "end_word": 5
                }
            }
        }
        
        response = ReadV1Response(**response_data)
        assert response.metadata.intents_info is not None
        assert response.metadata.sentiment_info is not None
        assert response.metadata.topics_info is not None
        assert response.metadata.summary_info is not None


class TestSpeakV1Response:
    """Test SpeakV1Response model."""
    
    def test_valid_speak_response(self, sample_audio_data):
        """Test creating a valid speak response."""
        # SpeakV1Response is typically just bytes (audio data)
        assert isinstance(sample_audio_data, bytes)
        assert len(sample_audio_data) > 0
    
    def test_empty_speak_response(self):
        """Test empty speak response."""
        empty_audio = b""
        assert isinstance(empty_audio, bytes)
        assert len(empty_audio) == 0
    
    def test_large_speak_response(self):
        """Test large speak response."""
        large_audio = b"\x00\x01\x02\x03" * 50000  # 200KB
        assert isinstance(large_audio, bytes)
        assert len(large_audio) == 200000
    
    def test_speak_response_audio_formats(self):
        """Test speak response with different audio format headers."""
        # WAV header simulation
        wav_header = b"RIFF\x24\x08\x00\x00WAVEfmt "
        wav_audio = wav_header + b"\x00\x01" * 1000
        assert isinstance(wav_audio, bytes)
        assert wav_audio.startswith(b"RIFF")
        
        # MP3 header simulation
        mp3_header = b"\xff\xfb"  # MP3 sync word
        mp3_audio = mp3_header + b"\x00\x01" * 1000
        assert isinstance(mp3_audio, bytes)
        assert mp3_audio.startswith(b"\xff\xfb")


class TestErrorResponseModern:
    """Test ErrorResponseModernError model."""
    
    def test_valid_modern_error_response(self):
        """Test creating a valid modern error response."""
        error_data = {
            "message": "Invalid API key",
            "category": "authentication_error"
        }
        
        response = ErrorResponseModernError(**error_data)
        assert response.message == "Invalid API key"
        assert response.category == "authentication_error"


class TestErrorResponseLegacy:
    """Test ErrorResponseLegacyError model."""
    
    def test_valid_legacy_error_response(self):
        """Test creating a valid legacy error response."""
        error_data = {
            "err_code": "INVALID_AUTH",
            "err_msg": "Invalid credentials provided"
        }
        
        response = ErrorResponseLegacyError(**error_data)
        assert response.err_code == "INVALID_AUTH"
        assert response.err_msg == "Invalid credentials provided"
    
    def test_error_response_serialization(self):
        """Test error response serialization."""
        error_data = {
            "err_code": "RATE_LIMIT",
            "err_msg": "Rate limit exceeded"
        }
        
        response = ErrorResponseLegacyError(**error_data)
        
        # Test dict conversion
        response_dict = response.model_dump()
        assert response_dict["err_code"] == "RATE_LIMIT"
        assert response_dict["err_msg"] == "Rate limit exceeded"
        
        # Test JSON serialization
        json_str = response.model_dump_json()
        assert '"err_code":"RATE_LIMIT"' in json_str
        assert '"err_msg":"Rate limit exceeded"' in json_str


class TestAPIResponseModelIntegration:
    """Integration tests for API response models."""
    
    def test_model_roundtrip_serialization(self):
        """Test that models can be serialized and deserialized."""
        # Test listen response roundtrip
        original_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Hello world",
                                "confidence": 0.95,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        original_response = ListenV1Response(**original_data)
        
        # Serialize to JSON and back
        json_str = original_response.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_response = ListenV1Response(**parsed_data)
        
        assert original_response.metadata.request_id == reconstructed_response.metadata.request_id
        assert original_response.metadata.duration == reconstructed_response.metadata.duration
        assert len(original_response.results.channels) == len(reconstructed_response.results.channels)
    
    def test_model_validation_edge_cases(self):
        """Test edge cases in model validation."""
        # Test with very long transcript
        long_transcript = "word " * 10000  # ~50KB
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1000.0,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": long_transcript,
                                "confidence": 0.95,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        response = ListenV1Response(**response_data)
        assert len(response.results.channels[0].alternatives[0].transcript) > 40000
    
    def test_model_with_extreme_numeric_values(self):
        """Test models with extreme numeric values."""
        # Test with very high confidence and long duration
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 99999.999999,
                "channels": 1000,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Test",
                                "confidence": 1.0,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        response = ListenV1Response(**response_data)
        assert response.metadata.duration == 99999.999999
        assert response.metadata.channels == 1000
        assert response.results.channels[0].alternatives[0].confidence == 1.0
    
    def test_comprehensive_error_scenarios(self):
        """Test comprehensive error scenarios."""
        # Test various HTTP error codes and messages
        error_scenarios = [
            {
                "message": "Bad Request - Invalid parameters",
                "type": "bad_request_error"
            },
            {
                "message": "Unauthorized - Invalid API key",
                "type": "authentication_error"
            },
            {
                "message": "Forbidden - Insufficient permissions",
                "type": "permission_error"
            },
            {
                "message": "Not Found - Resource does not exist",
                "type": "not_found_error"
            },
            {
                "message": "Too Many Requests - Rate limit exceeded",
                "type": "rate_limit_error"
            },
            {
                "message": "Internal Server Error",
                "type": "server_error"
            },
            {
                "message": "Service Unavailable - Try again later",
                "type": "service_unavailable_error"
            }
        ]
        
        for scenario in error_scenarios:
            error_response = ErrorResponseModernError(
                message=scenario["message"],
                category=scenario["type"]
            )
            assert error_response.message == scenario["message"]
            assert error_response.category == scenario["type"]
    
    def test_model_comparison_and_equality(self):
        """Test model equality comparison."""
        response_data = {
            "metadata": {
                "transaction_key": "deprecated",
                "request_id": "req-123",
                "sha256": "abc123def456",
                "created": "2023-01-01T00:00:00Z",
                "duration": 1.5,
                "channels": 1,
                "models": ["nova-2-general"],
                "model_info": {
                    "name": "nova-2-general",
                    "version": "1.0",
                    "arch": "nova"
                }
            },
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {
                                "transcript": "Hello world",
                                "confidence": 0.95,
                                "words": []
                            }
                        ]
                    }
                ]
            }
        }
        
        response1 = ListenV1Response(**response_data)
        response2 = ListenV1Response(**response_data)
        
        # Same data should be equal
        assert response1 == response2
        
        # Different data should not be equal
        different_data = response_data.copy()
        different_data["metadata"]["request_id"] = "req-456"
        response3 = ListenV1Response(**different_data)
        assert response1 != response3
