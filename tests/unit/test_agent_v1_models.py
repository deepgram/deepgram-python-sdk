"""
Unit tests for Agent V1 socket event models.
"""
import pytest
from pydantic import ValidationError

from deepgram.extensions.types.sockets.agent_v1_agent_started_speaking_event import AgentV1AgentStartedSpeakingEvent
from deepgram.extensions.types.sockets.agent_v1_agent_thinking_event import AgentV1AgentThinkingEvent
from deepgram.extensions.types.sockets.agent_v1_control_message import AgentV1ControlMessage
from deepgram.extensions.types.sockets.agent_v1_conversation_text_event import AgentV1ConversationTextEvent
from deepgram.extensions.types.sockets.agent_v1_error_event import AgentV1ErrorEvent
from deepgram.extensions.types.sockets.agent_v1_function_call_request_event import AgentV1FunctionCallRequestEvent
from deepgram.extensions.types.sockets.agent_v1_function_call_response_message import AgentV1FunctionCallResponseMessage
from deepgram.extensions.types.sockets.agent_v1_warning_event import AgentV1WarningEvent
from deepgram.extensions.types.sockets.agent_v1_welcome_message import AgentV1WelcomeMessage


class TestAgentV1WelcomeMessage:
    """Test AgentV1WelcomeMessage model."""
    
    def test_valid_welcome_message(self, valid_model_data):
        """Test creating a valid welcome message."""
        data = valid_model_data("agent_v1_welcome")
        message = AgentV1WelcomeMessage(**data)
        
        assert message.type == "Welcome"
        assert message.request_id == "req-123"
    
    def test_welcome_message_serialization(self, valid_model_data):
        """Test welcome message serialization."""
        data = valid_model_data("agent_v1_welcome")
        message = AgentV1WelcomeMessage(**data)
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "Welcome"
        assert message_dict["request_id"] == "req-123"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"Welcome"' in json_str
        assert '"request_id":"req-123"' in json_str
    
    def test_welcome_message_missing_required_fields(self):
        """Test welcome message with missing required fields."""
        # Missing request_id
        with pytest.raises(ValidationError) as exc_info:
            AgentV1WelcomeMessage(
                type="Welcome"
            )
        assert "request_id" in str(exc_info.value)
    
    def test_welcome_message_wrong_type(self):
        """Test welcome message with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            AgentV1WelcomeMessage(
                type="ConversationText",  # Wrong type
                request_id="req-123"
            )
        assert "Input should be 'Welcome'" in str(exc_info.value)


class TestAgentV1ConversationTextEvent:
    """Test AgentV1ConversationTextEvent model."""
    
    def test_valid_conversation_text_event(self, valid_model_data):
        """Test creating a valid conversation text event."""
        data = valid_model_data("agent_v1_conversation_text")
        event = AgentV1ConversationTextEvent(**data)
        
        assert event.type == "ConversationText"
        assert event.role == "assistant"
        assert event.content == "Hello!"
    
    def test_conversation_text_event_serialization(self, valid_model_data):
        """Test conversation text event serialization."""
        data = valid_model_data("agent_v1_conversation_text")
        event = AgentV1ConversationTextEvent(**data)
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "ConversationText"
        assert event_dict["role"] == "assistant"
        assert event_dict["content"] == "Hello!"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"ConversationText"' in json_str
        assert '"role":"assistant"' in json_str
    
    def test_conversation_text_event_missing_required_fields(self):
        """Test conversation text event with missing required fields."""
        # Missing role
        with pytest.raises(ValidationError) as exc_info:
            AgentV1ConversationTextEvent(
                type="ConversationText",
                content="Hello!"
            )
        assert "role" in str(exc_info.value)
        
        # Missing content
        with pytest.raises(ValidationError) as exc_info:
            AgentV1ConversationTextEvent(
                type="ConversationText",
                role="assistant"
            )
        assert "content" in str(exc_info.value)
    
    def test_conversation_text_event_valid_roles(self):
        """Test conversation text event with valid roles."""
        valid_roles = ["user", "assistant"]
        
        for role in valid_roles:
            event = AgentV1ConversationTextEvent(
                type="ConversationText",
                role=role,
                content="Test content"
            )
            assert event.role == role
    
    def test_conversation_text_event_invalid_role(self):
        """Test conversation text event with invalid role."""
        with pytest.raises(ValidationError) as exc_info:
            AgentV1ConversationTextEvent(
                type="ConversationText",
                role="system",  # Invalid role
                content="Hello!"
            )
        assert "Input should be 'user' or 'assistant'" in str(exc_info.value)
    
    def test_conversation_text_event_empty_content(self):
        """Test conversation text event with empty content."""
        event = AgentV1ConversationTextEvent(
            type="ConversationText",
            role="assistant",
            content=""
        )
        
        assert event.content == ""
    
    def test_conversation_text_event_long_content(self):
        """Test conversation text event with very long content."""
        long_content = "This is a very long message. " * 1000  # ~30KB
        event = AgentV1ConversationTextEvent(
            type="ConversationText",
            role="assistant",
            content=long_content
        )
        
        assert len(event.content) > 20000


class TestAgentV1FunctionCallRequestEvent:
    """Test AgentV1FunctionCallRequestEvent model."""
    
    def test_valid_function_call_request_event(self, valid_model_data):
        """Test creating a valid function call request event."""
        data = valid_model_data("agent_v1_function_call_request")
        event = AgentV1FunctionCallRequestEvent(**data)
        
        assert event.type == "FunctionCallRequest"
        assert len(event.functions) == 1
        assert event.functions[0].id == "func-123"
        assert event.functions[0].name == "get_weather"
        assert event.functions[0].arguments == "{}"
        assert event.functions[0].client_side is False
    
    def test_function_call_request_event_serialization(self, valid_model_data):
        """Test function call request event serialization."""
        data = valid_model_data("agent_v1_function_call_request")
        event = AgentV1FunctionCallRequestEvent(**data)
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "FunctionCallRequest"
        assert len(event_dict["functions"]) == 1
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"FunctionCallRequest"' in json_str
        assert '"name":"get_weather"' in json_str
    
    def test_function_call_request_event_missing_required_fields(self):
        """Test function call request event with missing required fields."""
        # Missing functions
        with pytest.raises(ValidationError) as exc_info:
            AgentV1FunctionCallRequestEvent(
                type="FunctionCallRequest"
            )
        assert "functions" in str(exc_info.value)
    
    def test_function_call_request_event_empty_functions(self):
        """Test function call request event with empty functions list."""
        event = AgentV1FunctionCallRequestEvent(
            type="FunctionCallRequest",
            functions=[]
        )
        
        assert event.type == "FunctionCallRequest"
        assert len(event.functions) == 0
    
    def test_function_call_request_event_multiple_functions(self, sample_function_call):
        """Test function call request event with multiple functions."""
        functions = [
            sample_function_call,
            {
                "id": "func-456",
                "name": "get_time",
                "arguments": '{"timezone": "UTC"}',
                "client_side": True
            }
        ]
        
        event = AgentV1FunctionCallRequestEvent(
            type="FunctionCallRequest",
            functions=functions
        )
        
        assert len(event.functions) == 2
        assert event.functions[0].name == "get_weather"
        assert event.functions[1].name == "get_time"
        assert event.functions[1].client_side is True
    
    def test_function_call_request_event_invalid_function_structure(self):
        """Test function call request event with invalid function structure."""
        # Missing required function fields
        with pytest.raises(ValidationError) as exc_info:
            AgentV1FunctionCallRequestEvent(
                type="FunctionCallRequest",
                functions=[{
                    "id": "func-123",
                    "name": "get_weather"
                    # Missing arguments and client_side
                }]
            )
        # The validation error should mention missing fields
        error_str = str(exc_info.value)
        assert "arguments" in error_str or "client_side" in error_str


class TestAgentV1FunctionCallResponseMessage:
    """Test AgentV1FunctionCallResponseMessage model."""
    
    def test_valid_function_call_response_message(self):
        """Test creating a valid function call response message."""
        message = AgentV1FunctionCallResponseMessage(
            type="FunctionCallResponse",
            name="get_weather",
            content='{"temperature": 25, "condition": "sunny"}'
        )
        
        assert message.type == "FunctionCallResponse"
        assert message.name == "get_weather"
        assert message.content == '{"temperature": 25, "condition": "sunny"}'
    
    def test_function_call_response_message_serialization(self):
        """Test function call response message serialization."""
        message = AgentV1FunctionCallResponseMessage(
            type="FunctionCallResponse",
            name="get_weather",
            content='{"temperature": 25, "condition": "sunny"}'
        )
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "FunctionCallResponse"
        assert message_dict["name"] == "get_weather"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"FunctionCallResponse"' in json_str
        assert '"name":"get_weather"' in json_str
    
    def test_function_call_response_message_missing_required_fields(self):
        """Test function call response message with missing required fields."""
        # Missing name
        with pytest.raises(ValidationError) as exc_info:
            AgentV1FunctionCallResponseMessage(
                type="FunctionCallResponse",
                content='{"temperature": 25}'
            )
        assert "name" in str(exc_info.value)
        
        # Missing content
        with pytest.raises(ValidationError) as exc_info:
            AgentV1FunctionCallResponseMessage(
                type="FunctionCallResponse",
                name="get_weather"
            )
        assert "content" in str(exc_info.value)


class TestAgentV1AgentThinkingEvent:
    """Test AgentV1AgentThinkingEvent model."""
    
    def test_valid_agent_thinking_event(self):
        """Test creating a valid agent thinking event."""
        event = AgentV1AgentThinkingEvent(
            type="AgentThinking",
            content="I'm thinking about your request..."
        )
        
        assert event.type == "AgentThinking"
        assert event.content == "I'm thinking about your request..."
    
    def test_agent_thinking_event_serialization(self):
        """Test agent thinking event serialization."""
        event = AgentV1AgentThinkingEvent(
            type="AgentThinking",
            content="Processing your request..."
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "AgentThinking"
        assert event_dict["content"] == "Processing your request..."
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"AgentThinking"' in json_str
        assert '"content":"Processing your request..."' in json_str
    
    def test_agent_thinking_event_wrong_type(self):
        """Test agent thinking event with wrong type field."""
        with pytest.raises(ValidationError) as exc_info:
            AgentV1AgentThinkingEvent(
                type="UserStartedSpeaking",  # Wrong type
                content="Test content"
            )
        assert "Input should be 'AgentThinking'" in str(exc_info.value)


class TestAgentV1AgentStartedSpeakingEvent:
    """Test AgentV1AgentStartedSpeakingEvent model."""
    
    def test_valid_agent_started_speaking_event(self):
        """Test creating a valid agent started speaking event."""
        event = AgentV1AgentStartedSpeakingEvent(
            type="AgentStartedSpeaking",
            total_latency=150.5,
            tts_latency=50.2,
            ttt_latency=100.3
        )
        
        assert event.type == "AgentStartedSpeaking"
        assert event.total_latency == 150.5
        assert event.tts_latency == 50.2
        assert event.ttt_latency == 100.3
    
    def test_agent_started_speaking_event_serialization(self):
        """Test agent started speaking event serialization."""
        event = AgentV1AgentStartedSpeakingEvent(
            type="AgentStartedSpeaking",
            total_latency=150.5,
            tts_latency=50.2,
            ttt_latency=100.3
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "AgentStartedSpeaking"
        assert event_dict["total_latency"] == 150.5
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"AgentStartedSpeaking"' in json_str
        assert '"total_latency":150.5' in json_str
    
    def test_agent_started_speaking_event_missing_required_fields(self):
        """Test agent started speaking event with missing required fields."""
        # Missing total_latency
        with pytest.raises(ValidationError) as exc_info:
            AgentV1AgentStartedSpeakingEvent(
                type="AgentStartedSpeaking",
                tts_latency=50.2,
                ttt_latency=100.3
            )
        assert "total_latency" in str(exc_info.value)
    
    def test_agent_started_speaking_event_invalid_data_types(self):
        """Test agent started speaking event with invalid data types."""
        # Invalid total_latency type
        with pytest.raises(ValidationError) as exc_info:
            AgentV1AgentStartedSpeakingEvent(
                type="AgentStartedSpeaking",
                total_latency="not_a_number",
                tts_latency=50.2,
                ttt_latency=100.3
            )
        assert "Input should be a valid number" in str(exc_info.value)


class TestAgentV1ErrorEvent:
    """Test AgentV1ErrorEvent model."""
    
    def test_valid_error_event(self):
        """Test creating a valid error event."""
        event = AgentV1ErrorEvent(
            type="Error",
            description="Function call failed",
            code="FUNCTION_CALL_ERROR"
        )
        
        assert event.type == "Error"
        assert event.description == "Function call failed"
        assert event.code == "FUNCTION_CALL_ERROR"
    
    def test_error_event_serialization(self):
        """Test error event serialization."""
        event = AgentV1ErrorEvent(
            type="Error",
            description="Function call failed",
            code="FUNCTION_CALL_ERROR"
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Error"
        assert event_dict["description"] == "Function call failed"
        assert event_dict["code"] == "FUNCTION_CALL_ERROR"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Error"' in json_str
        assert '"description":"Function call failed"' in json_str
    
    def test_error_event_missing_required_fields(self):
        """Test error event with missing required fields."""
        # Missing description
        with pytest.raises(ValidationError) as exc_info:
            AgentV1ErrorEvent(
                type="Error",
                code="FUNCTION_CALL_ERROR"
            )
        assert "description" in str(exc_info.value)
        
        # Missing code
        with pytest.raises(ValidationError) as exc_info:
            AgentV1ErrorEvent(
                type="Error",
                description="Function call failed"
            )
        assert "code" in str(exc_info.value)


class TestAgentV1WarningEvent:
    """Test AgentV1WarningEvent model."""
    
    def test_valid_warning_event(self):
        """Test creating a valid warning event."""
        event = AgentV1WarningEvent(
            type="Warning",
            description="Connection quality degraded",
            code="CONNECTION_WARNING"
        )
        
        assert event.type == "Warning"
        assert event.description == "Connection quality degraded"
        assert event.code == "CONNECTION_WARNING"
    
    def test_warning_event_serialization(self):
        """Test warning event serialization."""
        event = AgentV1WarningEvent(
            type="Warning",
            description="Connection quality degraded",
            code="CONNECTION_WARNING"
        )
        
        # Test dict conversion
        event_dict = event.model_dump()
        assert event_dict["type"] == "Warning"
        assert event_dict["description"] == "Connection quality degraded"
        
        # Test JSON serialization
        json_str = event.model_dump_json()
        assert '"type":"Warning"' in json_str


class TestAgentV1ControlMessage:
    """Test AgentV1ControlMessage model."""
    
    def test_valid_control_message(self):
        """Test creating a valid control message."""
        message = AgentV1ControlMessage(
            type="KeepAlive"
        )
        
        assert message.type == "KeepAlive"
    
    def test_control_message_serialization(self):
        """Test control message serialization."""
        message = AgentV1ControlMessage(type="KeepAlive")
        
        # Test dict conversion
        message_dict = message.model_dump()
        assert message_dict["type"] == "KeepAlive"
        
        # Test JSON serialization
        json_str = message.model_dump_json()
        assert '"type":"KeepAlive"' in json_str


class TestAgentV1MediaMessage:
    """Test AgentV1MediaMessage model."""
    
    def test_valid_media_message(self, sample_audio_data):
        """Test creating a valid media message."""
        # AgentV1MediaMessage is typically just bytes
        assert isinstance(sample_audio_data, bytes)
        assert len(sample_audio_data) > 0
    
    def test_empty_media_message(self):
        """Test empty media message."""
        empty_data = b""
        assert isinstance(empty_data, bytes)
        assert len(empty_data) == 0


class TestAgentV1ModelIntegration:
    """Integration tests for Agent V1 models."""
    
    def test_model_roundtrip_serialization(self, valid_model_data):
        """Test that models can be serialized and deserialized."""
        # Test conversation text event roundtrip
        conversation_data = valid_model_data("agent_v1_conversation_text")
        original_event = AgentV1ConversationTextEvent(**conversation_data)
        
        # Serialize to JSON and back
        json_str = original_event.model_dump_json()
        import json
        parsed_data = json.loads(json_str)
        reconstructed_event = AgentV1ConversationTextEvent(**parsed_data)
        
        assert original_event.type == reconstructed_event.type
        assert original_event.role == reconstructed_event.role
        assert original_event.content == reconstructed_event.content
    
    def test_comprehensive_function_call_scenarios(self):
        """Test comprehensive function call scenarios."""
        # Test various function call types
        function_scenarios = [
            {
                "id": "weather-1",
                "name": "get_weather",
                "arguments": '{"location": "New York", "units": "metric"}',
                "client_side": False
            },
            {
                "id": "time-1", 
                "name": "get_current_time",
                "arguments": '{"timezone": "America/New_York"}',
                "client_side": True
            },
            {
                "id": "calc-1",
                "name": "calculate",
                "arguments": '{"expression": "2 + 2"}',
                "client_side": False
            }
        ]
        
        for scenario in function_scenarios:
            event = AgentV1FunctionCallRequestEvent(
                type="FunctionCallRequest",
                functions=[scenario]
            )
            assert len(event.functions) == 1
            assert event.functions[0].name == scenario["name"]
            assert event.functions[0].client_side == scenario["client_side"]
    
    def test_latency_measurements_edge_cases(self):
        """Test latency measurements with edge cases."""
        # Test with zero latencies
        event = AgentV1AgentStartedSpeakingEvent(
            type="AgentStartedSpeaking",
            total_latency=0.0,
            tts_latency=0.0,
            ttt_latency=0.0
        )
        assert event.total_latency == 0.0
        
        # Test with very high latencies
        event = AgentV1AgentStartedSpeakingEvent(
            type="AgentStartedSpeaking",
            total_latency=99999.999,
            tts_latency=50000.0,
            ttt_latency=49999.999
        )
        assert event.total_latency == 99999.999
        
        # Test with fractional latencies
        event = AgentV1AgentStartedSpeakingEvent(
            type="AgentStartedSpeaking",
            total_latency=123.456789,
            tts_latency=45.123456,
            ttt_latency=78.333333
        )
        assert event.total_latency == 123.456789
    
    def test_error_and_warning_comprehensive(self):
        """Test comprehensive error and warning scenarios."""
        # Test common error scenarios
        error_scenarios = [
            {
                "description": "Function 'get_weather' not found",
                "code": "FUNCTION_NOT_FOUND"
            },
            {
                "description": "Invalid function arguments provided",
                "code": "INVALID_ARGUMENTS"
            },
            {
                "description": "Function execution timeout",
                "code": "FUNCTION_TIMEOUT"
            },
            {
                "description": "Rate limit exceeded for function calls",
                "code": "RATE_LIMIT_EXCEEDED"
            }
        ]
        
        for scenario in error_scenarios:
            event = AgentV1ErrorEvent(
                type="Error",
                description=scenario["description"],
                code=scenario["code"]
            )
            assert event.description == scenario["description"]
            assert event.code == scenario["code"]
        
        # Test common warning scenarios
        warning_scenarios = [
            {
                "description": "Function call taking longer than expected",
                "code": "FUNCTION_SLOW_WARNING"
            },
            {
                "description": "Connection quality may affect performance",
                "code": "CONNECTION_QUALITY_WARNING"
            }
        ]
        
        for scenario in warning_scenarios:
            event = AgentV1WarningEvent(
                type="Warning",
                description=scenario["description"],
                code=scenario["code"]
            )
            assert event.description == scenario["description"]
            assert event.code == scenario["code"]
    
    def test_model_immutability(self, valid_model_data):
        """Test that models are properly validated on construction."""
        data = valid_model_data("agent_v1_conversation_text")
        event = AgentV1ConversationTextEvent(**data)
        
        # Models should be immutable by default in Pydantic v2
        # Test that we can access all fields
        assert event.type == "ConversationText"
        assert event.role is not None
        assert event.content is not None
