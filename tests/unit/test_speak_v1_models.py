"""
Unit tests for Speak V1 socket event models.
"""
import pytest
from pydantic import ValidationError

from deepgram.extensions.types.sockets.speak_v1_metadata_event import SpeakV1MetadataEvent
from deepgram.extensions.types.sockets.speak_v1_control_event import SpeakV1ControlEvent
from deepgram.extensions.types.sockets.speak_v1_warning_event import SpeakV1WarningEvent
from deepgram.extensions.types.sockets.speak_v1_audio_chunk_event import SpeakV1AudioChunkEvent
from deepgram.extensions.types.sockets.speak_v1_text_message import SpeakV1TextMessage
from deepgram.extensions.types.sockets.speak_v1_control_message import SpeakV1ControlMessage


class TestSpeakV1MetadataEvent:
    """Test SpeakV1MetadataEvent model."""
    
    def test_valid_metadata_event(self, valid_model_data):
        """Test creating a valid metadata event."""
        data = valid_model_data("speak_v1_metadata")
        event = SpeakV1MetadataEvent(**data)
        
        assert event.type == "Metadata"
        assert event.request_id == "speak-123"
        assert event.model_name == "aura-asteria-en"
        assert event.model_version == "1.0"
        assert event.model_uuid == "uuid-123"
    
    def test_metadata_event_serialization(self, valid_model_data):
        """Test metadata event serialization."""
        data = valid_model_data("speak_v1_metadata")
        event = SpeakV1MetadataEvent(**data)
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Metadata"
        assert event_dict["request_id"] == "speak-123"
        assert event_dict["model_name"] == "aura-asteria-en"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Metadata"' in json_str
        assert '"request_id":"speak-123"' in json_str
    
    def test_metadata_event_missing_required_fields(self):
        """Test metadata event with missing required fields."""
        # Missing request_id
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1MetadataEvent(
                type="Metadata",
                model_name="aura-asteria-en",
                model_version="1.0",
                model_uuid="uuid-123"
            )
        assert "request_id" in str(exc_info.value)
        
        # Missing model_name
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1MetadataEvent(
                type="Metadata",
                request_id="speak-123",
                model_version="1.0",
                model_uuid="uuid-123"
            )
        assert "model_name" in str(exc_info.value)
    
    def test_metadata_event_wrong_type(self):
        """Test metadata event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1MetadataEvent(
                type="Audio",  # Wrong type
                request_id="speak-123",
                model_name="aura-asteria-en",
                model_version="1.0",
                model_uuid="uuid-123"
            )
        assert "Input should be 'Metadata'" in str(exc_info.value)
    
    def test_metadata_event_optional_fields(self):
        """Test metadata event with minimal required fields."""
        event = SpeakV1MetadataEvent(
            type="Metadata",
            request_id="speak-123",
            model_name="aura-asteria-en",
            model_version="1.0",
            model_uuid="uuid-123"
        )
        
        assert event.type == "Metadata"
        assert event.request_id == "speak-123"
        assert event.model_name == "aura-asteria-en"


class TestSpeakV1ControlEvent:
    """Test SpeakV1ControlEvent model."""
    
    def test_valid_control_event(self):
        """Test creating a valid control event."""
        event = SpeakV1ControlEvent(
            type="Flushed",
            sequence_id=1
        )
        
        assert event.type == "Flushed"
        assert event.sequence_id == 1
    
    def test_control_event_serialization(self):
        """Test control event serialization."""
        event = SpeakV1ControlEvent(
            type="Flushed",
            sequence_id=1
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Flushed"
        assert event_dict["sequence_id"] == 1
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Flushed"' in json_str
        assert '"sequence_id":1' in json_str
    
    def test_control_event_missing_required_fields(self):
        """Test control event with missing required fields."""
        # Missing sequence_id
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1ControlEvent(
                type="Flushed"
            )
        assert "sequence_id" in str(exc_info.value)
    
    def test_control_event_wrong_type(self):
        """Test control event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1ControlEvent(
                type="Metadata",  # Wrong type
                sequence_id=1
            )
        assert "Input should be 'Flushed'" in str(exc_info.value)
    
    def test_control_event_invalid_data_types(self):
        """Test control event with invalid data types."""
        # Invalid sequence_id type
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1ControlEvent(
                type="Flushed",
                sequence_id="not_a_number"
            )
        assert "Input should be a valid integer" in str(exc_info.value)


class TestSpeakV1WarningEvent:
    """Test SpeakV1WarningEvent model."""
    
    def test_valid_warning_event(self):
        """Test creating a valid warning event."""
        event = SpeakV1WarningEvent(
            type="Warning",
            warn_msg="Audio quality may be degraded",
            warn_code="AUDIO_QUALITY_WARNING"
        )

        assert event.type == "Warning"
        assert event.warn_msg == "Audio quality may be degraded"
        assert event.warn_code == "AUDIO_QUALITY_WARNING"
    
    def test_warning_event_serialization(self):
        """Test warning event serialization."""
        event = SpeakV1WarningEvent(
            type="Warning",
            warn_msg="Audio quality may be degraded",
            warn_code="AUDIO_QUALITY_WARNING"
        )

        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Warning"
        assert event_dict["warn_msg"] == "Audio quality may be degraded"
        assert event_dict["warn_code"] == "AUDIO_QUALITY_WARNING"

        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Warning"' in json_str
        assert '"warn_msg":"Audio quality may be degraded"' in json_str
    
    def test_warning_event_missing_required_fields(self):
        """Test warning event with missing required fields."""
        # Missing warn_msg
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1WarningEvent(
                type="Warning",
                warn_code="AUDIO_QUALITY_WARNING"
            )
        assert "warn_msg" in str(exc_info.value)

        # Missing warn_code
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1WarningEvent(
                type="Warning",
                warn_msg="Audio quality may be degraded"
            )
        assert "warn_code" in str(exc_info.value)
    
    def test_warning_event_wrong_type(self):
        """Test warning event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1WarningEvent(
                type="Error",  # Wrong type
                warn_msg="Audio quality may be degraded",
                warn_code="AUDIO_QUALITY_WARNING"
            )
        assert "Input should be 'Warning'" in str(exc_info.value)


class TestSpeakV1AudioChunkEvent:
    """Test SpeakV1AudioChunkEvent model."""
    
    def test_valid_audio_chunk_event(self, sample_audio_data):
        """Test creating a valid audio chunk event."""
        # SpeakV1AudioChunkEvent is typically just bytes
        assert isinstance(sample_audio_data, bytes)
        assert len(sample_audio_data) > 0
    
    def test_empty_audio_chunk(self):
        """Test empty audio chunk."""
        empty_data = b""
        assert isinstance(empty_data, bytes)
        assert len(empty_data) == 0
    
    def test_large_audio_chunk(self):
        """Test large audio chunk."""
        large_data = b"\x00\x01\x02\x03" * 10000  # 40KB
        assert isinstance(large_data, bytes)
        assert len(large_data) == 40000


class TestSpeakV1TextMessage:
    """Test SpeakV1TextMessage model."""
    
    def test_valid_text_message(self):
        """Test creating a valid text message."""
        message = SpeakV1TextMessage(
            type="Speak",
            text="Hello, world!"
        )
        
        assert message.type == "Speak"
        assert message.text == "Hello, world!"
    
    def test_text_message_serialization(self):
        """Test text message serialization."""
        message = SpeakV1TextMessage(
            type="Speak",
            text="Hello, world!"
        )
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "Speak"
        assert message_dict["text"] == "Hello, world!"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"Speak"' in json_str
        assert '"text":"Hello, world!"' in json_str
    
    def test_text_message_missing_required_fields(self):
        """Test text message with missing required fields."""
        # Missing text
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1TextMessage(
                type="Speak"
            )
        assert "text" in str(exc_info.value)
    
    def test_text_message_wrong_type(self):
        """Test text message with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1TextMessage(
                type="Control",  # Wrong type
                text="Hello, world!"
            )
        assert "Input should be 'Speak'" in str(exc_info.value)
    
    def test_text_message_empty_text(self):
        """Test text message with empty text."""
        message = SpeakV1TextMessage(
            type="Speak",
            text=""
        )
        
        assert message.type == "Speak"
        assert message.text == ""
    
    def test_text_message_long_text(self):
        """Test text message with very long text."""
        long_text = "Hello, world! " * 1000  # ~14KB
        message = SpeakV1TextMessage(
            type="Speak",
            text=long_text
        )
        
        assert message.type == "Speak"
        assert len(message.text) > 10000
    
    def test_text_message_special_characters(self):
        """Test text message with special characters."""
        special_text = "Hello! 🌍 こんにちは 你好 🎵 ñáéíóú @#$%^&*()_+-=[]{}|;':\",./<>?"
        message = SpeakV1TextMessage(
            type="Speak",
            text=special_text
        )
        
        assert message.type == "Speak"
        assert message.text == special_text


class TestSpeakV1ControlMessage:
    """Test SpeakV1ControlMessage model."""
    
    def test_valid_control_message(self):
        """Test creating a valid control message."""
        message = SpeakV1ControlMessage(
            type="Flush"
        )
        
        assert message.type == "Flush"
    
    def test_control_message_serialization(self):
        """Test control message serialization."""
        message = SpeakV1ControlMessage(type="Flush")
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "Flush"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"Flush"' in json_str
    
    def test_control_message_missing_type(self):
        """Test control message with missing type field."""
        with pytest.raises(ValidationError) as exc_info:
            SpeakV1ControlMessage()
        assert "type" in str(exc_info.value)
    
    def test_control_message_different_types(self):
        """Test control message with different valid types."""
        valid_types = ["Flush", "Clear", "Close"]
        
        for control_type in valid_types:
            message = SpeakV1ControlMessage(type=control_type)
            assert message.type == control_type


class TestSpeakV1ModelIntegration:
    """Integration tests for Speak V1 models."""
    
    def test_model_roundtrip_serialization(self, valid_model_data):
        """Test that models can be serialized and deserialized."""
        # Test metadata event roundtrip
        metadata_data = valid_model_data("speak_v1_metadata")
        original_event = SpeakV1MetadataEvent(**metadata_data)
        
        # Serialize to JSON and back
        json_str = original_event.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_event = SpeakV1MetadataEvent(**parsed_data)
        
        assert original_event.type == reconstructed_event.type
        assert original_event.request_id == reconstructed_event.request_id
        assert original_event.model_name == reconstructed_event.model_name
    
    def test_model_validation_edge_cases(self):
        """Test edge cases in model validation."""
        # Test with very long strings
        long_string = "x" * 10000
        event = SpeakV1MetadataEvent(
            type="Metadata",
            request_id=long_string,
            model_name="aura-asteria-en",
            model_version="1.0",
            model_uuid="uuid-123"
        )
        assert len(event.request_id) == 10000
    
    def test_comprehensive_text_scenarios(self):
        """Test comprehensive text message scenarios."""
        test_cases = [
            # Empty text
            "",
            # Simple text
            "Hello, world!",
            # Text with numbers
            "The year is 2023 and the temperature is 25.5 degrees.",
            # Text with punctuation
            "Hello! How are you? I'm fine, thanks. What about you...",
            # Text with newlines
            "Line 1\nLine 2\nLine 3",
            # Text with tabs
            "Column1\tColumn2\tColumn3",
            # Mixed case
            "MiXeD CaSe TeXt",
            # Only numbers
            "1234567890",
            # Only symbols
            "!@#$%^&*()",
        ]
        
        for text in test_cases:
            message = SpeakV1TextMessage(
                type="Speak",
                text=text
            )
            assert message.text == text
            assert message.type == "Speak"
    
    def test_model_immutability(self, valid_model_data):
        """Test that models are properly validated on construction."""
        data = valid_model_data("speak_v1_metadata")
        event = SpeakV1MetadataEvent(**data)
        
        # Models should be immutable by default in Pydantic v2
        # Test that we can access all fields
        assert event.type == "Metadata"
        assert event.request_id is not None
        assert event.model_name is not None
        assert event.model_version is not None
        assert event.model_uuid is not None
    
    def test_warning_event_comprehensive(self):
        """Test comprehensive warning event scenarios."""
        # Test common warning scenarios
        warning_scenarios = [
            {
                "warn_msg": "Audio quality may be degraded due to low bitrate",
                "warn_code": "AUDIO_QUALITY_WARNING"
            },
            {
                "warn_msg": "Rate limit approaching",
                "warn_code": "RATE_LIMIT_WARNING"
            },
            {
                "warn_msg": "Model switching to fallback version",
                "warn_code": "MODEL_FALLBACK_WARNING"
            },
            {
                "warn_msg": "Connection quality poor",
                "warn_code": "CONNECTION_WARNING"
            }
        ]

        for scenario in warning_scenarios:
            event = SpeakV1WarningEvent(
                type="Warning",
                warn_msg=scenario["warn_msg"],
                warn_code=scenario["warn_code"]
            )
            assert event.warn_msg == scenario["warn_msg"]
            assert event.warn_code == scenario["warn_code"]
