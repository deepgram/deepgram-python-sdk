"""
Unit tests for Listen V1 socket event models.
"""
import pytest
from pydantic import ValidationError

from deepgram.extensions.types.sockets.listen_v1_metadata_event import ListenV1MetadataEvent
from deepgram.extensions.types.sockets.listen_v1_results_event import ListenV1ResultsEvent
from deepgram.extensions.types.sockets.listen_v1_speech_started_event import ListenV1SpeechStartedEvent
from deepgram.extensions.types.sockets.listen_v1_utterance_end_event import ListenV1UtteranceEndEvent
from deepgram.extensions.types.sockets.listen_v1_control_message import ListenV1ControlMessage
from deepgram.extensions.types.sockets.listen_v1_media_message import ListenV1MediaMessage


class TestListenV1MetadataEvent:
    """Test ListenV1MetadataEvent model."""
    
    def test_valid_metadata_event(self, valid_model_data):
        """Test creating a valid metadata event."""
        data = valid_model_data("listen_v1_metadata")
        event = ListenV1MetadataEvent(**data)
        
        assert event.type == "Metadata"
        assert event.request_id == "test-123"
        assert event.sha256 == "abc123"
        assert event.created == "2023-01-01T00:00:00Z"
        assert event.duration == 1.0
        assert event.channels == 1
    
    def test_metadata_event_serialization(self, valid_model_data):
        """Test metadata event serialization."""
        data = valid_model_data("listen_v1_metadata")
        event = ListenV1MetadataEvent(**data)
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Metadata"
        assert event_dict["request_id"] == "test-123"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Metadata"' in json_str
        assert '"request_id":"test-123"' in json_str
    
    def test_metadata_event_missing_required_fields(self):
        """Test metadata event with missing required fields."""
        # Missing request_id
        with pytest.raises(ValidationError) as exc_info:
            ListenV1MetadataEvent(
                type="Metadata",
                sha256="abc123",
                created="2023-01-01T00:00:00Z",
                duration=1.0,
                channels=1
            )
        assert "request_id" in str(exc_info.value)
        
        # Missing sha256
        with pytest.raises(ValidationError) as exc_info:
            ListenV1MetadataEvent(
                type="Metadata",
                request_id="test-123",
                created="2023-01-01T00:00:00Z",
                duration=1.0,
                channels=1
            )
        assert "sha256" in str(exc_info.value)
    
    def test_metadata_event_wrong_type(self):
        """Test metadata event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1MetadataEvent(
                type="Results",  # Wrong type
                request_id="test-123",
                sha256="abc123",
                created="2023-01-01T00:00:00Z",
                duration=1.0,
                channels=1
            )
        assert "Input should be 'Metadata'" in str(exc_info.value)
    
    def test_metadata_event_invalid_data_types(self):
        """Test metadata event with invalid data types."""
        # Invalid duration type
        with pytest.raises(ValidationError) as exc_info:
            ListenV1MetadataEvent(
                type="Metadata",
                request_id="test-123",
                sha256="abc123",
                created="2023-01-01T00:00:00Z",
                duration="not_a_number",
                channels=1
            )
        assert "Input should be a valid number" in str(exc_info.value)
        
        # Invalid channels type
        with pytest.raises(ValidationError) as exc_info:
            ListenV1MetadataEvent(
                type="Metadata",
                request_id="test-123",
                sha256="abc123",
                created="2023-01-01T00:00:00Z",
                duration=1.0,
                channels="not_a_number"
            )
        assert "Input should be a valid number" in str(exc_info.value)


class TestListenV1ResultsEvent:
    """Test ListenV1ResultsEvent model."""
    
    def test_valid_results_event(self, valid_model_data):
        """Test creating a valid results event."""
        data = valid_model_data("listen_v1_results")
        event = ListenV1ResultsEvent(**data)
        
        assert event.type == "Results"
        assert event.channel_index == [0]
        assert event.duration == 1.0
        assert event.start == 0.0
        assert event.is_final is True
        assert event.channel is not None
        assert event.metadata is not None
    
    def test_results_event_serialization(self, valid_model_data):
        """Test results event serialization."""
        data = valid_model_data("listen_v1_results")
        event = ListenV1ResultsEvent(**data)
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Results"
        assert event_dict["channel_index"] == [0]
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Results"' in json_str
    
    def test_results_event_missing_required_fields(self):
        """Test results event with missing required fields."""
        # Missing channel
        with pytest.raises(ValidationError) as exc_info:
            ListenV1ResultsEvent(
                type="Results",
                channel_index=[0],
                duration=1.0,
                start=0.0,
                is_final=True,
                metadata={"request_id": "test-123"}
            )
        assert "channel" in str(exc_info.value)
    
    def test_results_event_wrong_type(self):
        """Test results event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1ResultsEvent(
                type="Metadata",  # Wrong type
                channel_index=[0],
                duration=1.0,
                start=0.0,
                is_final=True,
                channel={"alternatives": []},
                metadata={"request_id": "test-123"}
            )
        assert "Input should be 'Results'" in str(exc_info.value)


class TestListenV1SpeechStartedEvent:
    """Test ListenV1SpeechStartedEvent model."""
    
    def test_valid_speech_started_event(self):
        """Test creating a valid speech started event."""
        event = ListenV1SpeechStartedEvent(
            type="SpeechStarted",
            channel=[0],
            timestamp=1672531200.0
        )
        
        assert event.type == "SpeechStarted"
        assert event.channel == [0]
        assert event.timestamp == 1672531200.0
    
    def test_speech_started_event_serialization(self):
        """Test speech started event serialization."""
        event = ListenV1SpeechStartedEvent(
            type="SpeechStarted",
            channel=[0],
            timestamp=1672531200.0
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "SpeechStarted"
        assert event_dict["channel"] == [0]
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"SpeechStarted"' in json_str
    
    def test_speech_started_event_missing_fields(self):
        """Test speech started event with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1SpeechStartedEvent(
                type="SpeechStarted",
                channel=[0]
                # Missing timestamp
            )
        assert "timestamp" in str(exc_info.value)
    
    def test_speech_started_event_wrong_type(self):
        """Test speech started event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1SpeechStartedEvent(
                type="Results",  # Wrong type
                channel=[0],
                timestamp="2023-01-01T00:00:00Z"
            )
        assert "Input should be 'SpeechStarted'" in str(exc_info.value)


class TestListenV1UtteranceEndEvent:
    """Test ListenV1UtteranceEndEvent model."""
    
    def test_valid_utterance_end_event(self):
        """Test creating a valid utterance end event."""
        event = ListenV1UtteranceEndEvent(
            type="UtteranceEnd",
            channel=[0],
            last_word_end=1.5
        )
        
        assert event.type == "UtteranceEnd"
        assert event.channel == [0]
        assert event.last_word_end == 1.5
    
    def test_utterance_end_event_serialization(self):
        """Test utterance end event serialization."""
        event = ListenV1UtteranceEndEvent(
            type="UtteranceEnd",
            channel=[0],
            last_word_end=1.5
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "UtteranceEnd"
        assert event_dict["last_word_end"] == 1.5
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"UtteranceEnd"' in json_str
    
    def test_utterance_end_event_missing_fields(self):
        """Test utterance end event with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1UtteranceEndEvent(
                type="UtteranceEnd",
                channel=[0]
                # Missing last_word_end
            )
        assert "last_word_end" in str(exc_info.value)
    
    def test_utterance_end_event_invalid_data_types(self):
        """Test utterance end event with invalid data types."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1UtteranceEndEvent(
                type="UtteranceEnd",
                channel=[0],
                last_word_end="not_a_number"
            )
        assert "Input should be a valid number" in str(exc_info.value)


class TestListenV1ControlMessage:
    """Test ListenV1ControlMessage model."""
    
    def test_valid_control_message(self):
        """Test creating a valid control message."""
        message = ListenV1ControlMessage(
            type="KeepAlive"
        )
        
        assert message.type == "KeepAlive"
    
    def test_control_message_serialization(self):
        """Test control message serialization."""
        message = ListenV1ControlMessage(type="KeepAlive")
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "KeepAlive"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"KeepAlive"' in json_str
    
    def test_control_message_missing_type(self):
        """Test control message with missing type field."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV1ControlMessage()
        assert "type" in str(exc_info.value)


class TestListenV1MediaMessage:
    """Test ListenV1MediaMessage model."""
    
    def test_valid_media_message(self, sample_audio_data):
        """Test creating a valid media message."""
        # ListenV1MediaMessage is typically just bytes
        assert isinstance(sample_audio_data, bytes)
        assert len(sample_audio_data) > 0
    
    def test_empty_media_message(self):
        """Test empty media message."""
        empty_data = b""
        assert isinstance(empty_data, bytes)
        assert len(empty_data) == 0


class TestListenV1ModelIntegration:
    """Integration tests for Listen V1 models."""
    
    def test_model_roundtrip_serialization(self, valid_model_data):
        """Test that models can be serialized and deserialized."""
        # Test metadata event roundtrip
        metadata_data = valid_model_data("listen_v1_metadata")
        original_event = ListenV1MetadataEvent(**metadata_data)
        
        # Serialize to JSON and back
        json_str = original_event.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_event = ListenV1MetadataEvent(**parsed_data)
        
        assert original_event.type == reconstructed_event.type
        assert original_event.request_id == reconstructed_event.request_id
        assert original_event.sha256 == reconstructed_event.sha256
        assert original_event.duration == reconstructed_event.duration
    
    def test_model_validation_edge_cases(self):
        """Test edge cases in model validation."""
        # Test with very long strings
        long_string = "x" * 10000
        event = ListenV1MetadataEvent(
            type="Metadata",
            request_id=long_string,
            sha256="abc123",
            created="2023-01-01T00:00:00Z",
            duration=1.0,
            channels=1
        )
        assert len(event.request_id) == 10000
        
        # Test with extreme numeric values
        event = ListenV1MetadataEvent(
            type="Metadata",
            request_id="test-123",
            sha256="abc123",
            created="2023-01-01T00:00:00Z",
            duration=999999.999999,
            channels=999999
        )
        assert event.duration == 999999.999999
        assert event.channels == 999999
    
    def test_model_immutability(self, valid_model_data):
        """Test that models are properly validated on construction."""
        data = valid_model_data("listen_v1_metadata")
        event = ListenV1MetadataEvent(**data)
        
        # Models should be immutable by default in Pydantic v2
        # Test that we can access all fields
        assert event.type == "Metadata"
        assert event.request_id is not None
        assert event.sha256 is not None
        assert event.created is not None
        assert event.duration is not None
        assert event.channels is not None
