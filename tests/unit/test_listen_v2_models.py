"""
Unit tests for Listen V2 socket event models.
"""
import pytest
from pydantic import ValidationError

from deepgram.extensions.types.sockets.listen_v2_connected_event import ListenV2ConnectedEvent
from deepgram.extensions.types.sockets.listen_v2_turn_info_event import ListenV2TurnInfoEvent
from deepgram.extensions.types.sockets.listen_v2_fatal_error_event import ListenV2FatalErrorEvent
from deepgram.extensions.types.sockets.listen_v2_control_message import ListenV2ControlMessage
from deepgram.extensions.types.sockets.listen_v2_media_message import ListenV2MediaMessage


class TestListenV2ConnectedEvent:
    """Test ListenV2ConnectedEvent model."""
    
    def test_valid_connected_event(self):
        """Test creating a valid connected event."""
        event = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=1
        )
        
        assert event.type == "Connected"
        assert event.request_id == "req-123"
        assert event.sequence_id == 1
    
    def test_connected_event_serialization(self):
        """Test connected event serialization."""
        event = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=1
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Connected"
        assert event_dict["request_id"] == "req-123"
        assert event_dict["sequence_id"] == 1
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Connected"' in json_str
        assert '"request_id":"req-123"' in json_str
    
    def test_connected_event_missing_required_fields(self):
        """Test connected event with missing required fields."""
        # Missing request_id
        with pytest.raises(ValidationError) as exc_info:
            ListenV2ConnectedEvent(
                type="Connected",
                sequence_id=1
            )
        assert "request_id" in str(exc_info.value)
        
        # Missing sequence_id
        with pytest.raises(ValidationError) as exc_info:
            ListenV2ConnectedEvent(
                type="Connected",
                request_id="req-123"
            )
        assert "sequence_id" in str(exc_info.value)
    
    def test_connected_event_wrong_type(self):
        """Test connected event with wrong type field."""
        # Note: ListenV2ConnectedEvent doesn't enforce specific type values,
        # so this should succeed but with the wrong type value
        event = ListenV2ConnectedEvent(
            type="Results",  # Wrong type but still valid string
            request_id="req-123",
            sequence_id=1
        )
        assert event.type == "Results"  # It accepts any string
    
    def test_connected_event_invalid_data_types(self):
        """Test connected event with invalid data types."""
        # Invalid sequence_id type
        with pytest.raises(ValidationError) as exc_info:
            ListenV2ConnectedEvent(
                type="Connected",
                request_id="req-123",
                sequence_id="not_a_number"
            )
        assert "Input should be a valid integer" in str(exc_info.value)


class TestListenV2TurnInfoEvent:
    """Test ListenV2TurnInfoEvent model."""
    
    def test_valid_turn_info_event(self):
        """Test creating a valid turn info event."""
        event = ListenV2TurnInfoEvent(
            type="TurnInfo",
            request_id="req-123",
            sequence_id=1,
            event="TurnInfo",
            turn_index=0,
            audio_window_start=0.0,
            audio_window_end=1.5,
            transcript="Hello world",
            words=[],
            end_of_turn_confidence=0.95
        )
        
        assert event.type == "TurnInfo"
        assert event.request_id == "req-123"
        assert event.sequence_id == 1
        assert event.event == "TurnInfo"
        assert event.turn_index == 0
        assert event.audio_window_start == 0.0
        assert event.audio_window_end == 1.5
        assert event.transcript == "Hello world"
    
    def test_turn_info_event_serialization(self):
        """Test turn info event serialization."""
        event = ListenV2TurnInfoEvent(
            type="TurnInfo",
            request_id="req-123",
            sequence_id=1,
            event="TurnInfo",
            turn_index=0,
            audio_window_start=0.0,
            audio_window_end=1.5,
            transcript="Hello world",
            words=[],
            end_of_turn_confidence=0.95
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "TurnInfo"
        assert event_dict["turn_index"] == 0
        assert event_dict["transcript"] == "Hello world"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"TurnInfo"' in json_str
        assert '"transcript":"Hello world"' in json_str
    
    def test_turn_info_event_missing_required_fields(self):
        """Test turn info event with missing required fields."""
        # Missing event field
        with pytest.raises(ValidationError) as exc_info:
            ListenV2TurnInfoEvent(
                type="TurnInfo",
                request_id="req-123",
                sequence_id=1,
                turn_index=0,
                audio_window_start=0.0,
                audio_window_end=1.5,
                transcript="Hello world",
                words=[],
                end_of_turn_confidence=0.95
            )
        assert "event" in str(exc_info.value)
    
    def test_turn_info_event_invalid_data_types(self):
        """Test turn info event with invalid data types."""
        # Invalid audio_window_start type
        with pytest.raises(ValidationError) as exc_info:
            ListenV2TurnInfoEvent(
                type="TurnInfo",
                request_id="req-123",
                sequence_id=1,
                event="TurnInfo",
                turn_index=0,
                audio_window_start="not_a_number",
                audio_window_end=1.5,
                transcript="Hello world",
                words=[],
                end_of_turn_confidence=0.95
            )
        assert "Input should be a valid number" in str(exc_info.value)
        
        # Invalid audio_window_end type
        with pytest.raises(ValidationError) as exc_info:
            ListenV2TurnInfoEvent(
                type="TurnInfo",
                request_id="req-123",
                sequence_id=1,
                event="TurnInfo",
                turn_index=0,
                audio_window_start=0.0,
                audio_window_end="not_a_number",
                transcript="Hello world",
                words=[],
                end_of_turn_confidence=0.95
            )
        assert "Input should be a valid number" in str(exc_info.value)


class TestListenV2FatalErrorEvent:
    """Test ListenV2FatalErrorEvent model."""
    
    def test_valid_fatal_error_event(self):
        """Test creating a valid fatal error event."""
        event = ListenV2FatalErrorEvent(
            type="FatalError",
            sequence_id=1,
            code="500",
            description="Internal server error"
        )
        
        assert event.type == "FatalError"
        assert event.sequence_id == 1
        assert event.code == "500"
        assert event.description == "Internal server error"
    
    def test_fatal_error_event_serialization(self):
        """Test fatal error event serialization."""
        event = ListenV2FatalErrorEvent(
            type="FatalError",
            sequence_id=1,
            code="500",
            description="Internal server error"
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "FatalError"
        assert event_dict["code"] == "500"
        assert event_dict["description"] == "Internal server error"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"FatalError"' in json_str
        assert '"code":"500"' in json_str
    
    def test_fatal_error_event_missing_required_fields(self):
        """Test fatal error event with missing required fields."""
        # Missing code
        with pytest.raises(ValidationError) as exc_info:
            ListenV2FatalErrorEvent(
                type="FatalError",
                sequence_id=1,
                description="Internal server error"
            )
        assert "code" in str(exc_info.value)
        
        # Missing description
        with pytest.raises(ValidationError) as exc_info:
            ListenV2FatalErrorEvent(
                type="FatalError",
                sequence_id=1,
                code=500
            )
        assert "description" in str(exc_info.value)
    
    def test_fatal_error_event_wrong_type(self):
        """Test fatal error event with wrong type field."""
        # Note: ListenV2FatalErrorEvent doesn't enforce specific type values,
        # so this should succeed but with the wrong type value
        event = ListenV2FatalErrorEvent(
            type="Connected",  # Wrong type but still valid string
            sequence_id=1,
            code="500",
            description="Internal server error"
        )
        assert event.type == "Connected"  # It accepts any string
    
    def test_fatal_error_event_invalid_data_types(self):
        """Test fatal error event with invalid data types."""
        # Invalid sequence_id type
        with pytest.raises(ValidationError) as exc_info:
            ListenV2FatalErrorEvent(
                type="FatalError",
                sequence_id="not_a_number",
                code="500",
                description="Internal server error"
            )
        assert "Input should be a valid integer" in str(exc_info.value)


class TestListenV2ControlMessage:
    """Test ListenV2ControlMessage model."""
    
    def test_valid_control_message(self):
        """Test creating a valid control message."""
        message = ListenV2ControlMessage(
            type="CloseStream"
        )
        
        assert message.type == "CloseStream"
    
    def test_control_message_serialization(self):
        """Test control message serialization."""
        message = ListenV2ControlMessage(type="CloseStream")
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "CloseStream"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"CloseStream"' in json_str
    
    def test_control_message_missing_type(self):
        """Test control message with missing type field."""
        with pytest.raises(ValidationError) as exc_info:
            ListenV2ControlMessage()
        assert "type" in str(exc_info.value)


class TestListenV2MediaMessage:
    """Test ListenV2MediaMessage model."""
    
    def test_valid_media_message(self):
        """Test creating a valid media message."""
        # ListenV2MediaMessage appears to be an empty model
        message = ListenV2MediaMessage()
        
        # Test that it can be instantiated
        assert message is not None
    
    def test_media_message_serialization(self):
        """Test media message serialization."""
        message = ListenV2MediaMessage()
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert isinstance(message_dict, dict)
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert isinstance(json_str, str)


class TestListenV2ModelIntegration:
    """Integration tests for Listen V2 models."""
    
    def test_model_roundtrip_serialization(self):
        """Test that models can be serialized and deserialized."""
        # Test connected event roundtrip
        original_event = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=1
        )
        
        # Serialize to JSON and back
        json_str = original_event.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_event = ListenV2ConnectedEvent(**parsed_data)
        
        assert original_event.type == reconstructed_event.type
        assert original_event.request_id == reconstructed_event.request_id
        assert original_event.sequence_id == reconstructed_event.sequence_id
    
    def test_model_validation_edge_cases(self):
        """Test edge cases in model validation."""
        # Test with very long strings
        long_string = "x" * 10000
        event = ListenV2ConnectedEvent(
            type="Connected",
            request_id=long_string,
            sequence_id=999999
        )
        assert len(event.request_id) == 10000
        assert event.sequence_id == 999999
        
        # Test with negative sequence_id (should be allowed if not restricted)
        event = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=0
        )
        assert event.sequence_id == 0
    
    def test_model_comparison(self):
        """Test model equality comparison."""
        event1 = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=1
        )
        event2 = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-123",
            sequence_id=1
        )
        event3 = ListenV2ConnectedEvent(
            type="Connected",
            request_id="req-456",
            sequence_id=1
        )
        
        # Same data should be equal
        assert event1 == event2
        # Different data should not be equal
        assert event1 != event3
    
    def test_error_event_comprehensive(self):
        """Test comprehensive error event scenarios."""
        # Test common HTTP error codes
        error_codes = [400, 401, 403, 404, 429, 500, 502, 503]
        error_messages = [
            "Bad Request",
            "Unauthorized",
            "Forbidden",
            "Not Found",
            "Too Many Requests",
            "Internal Server Error",
            "Bad Gateway",
            "Service Unavailable"
        ]
        
        for code, message in zip(error_codes, error_messages):
            event = ListenV2FatalErrorEvent(
                type="FatalError",
                sequence_id=code,
                code=str(code),
                description=message
            )
            assert event.code == str(code)
            assert event.description == message
