import pytest
import json
from unittest.mock import patch, MagicMock

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    InjectUserMessageOptions,
    FunctionCallResponse
)

class TestAgentInjectUserMessage:
    """Focused unit tests for inject_user_message functionality"""

    def test_inject_user_message_options_serialization(self):
        """Test JSON serialization is correct"""
        options = InjectUserMessageOptions(content="Test message")
        result = json.loads(str(options))
        expected = {"type": "InjectUserMessage", "content": "Test message"}
        assert result == expected

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_inject_user_message_success(self, mock_send):
        """Test successful message injection"""
        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")
        options = InjectUserMessageOptions(content="Hello")

        result = connection.inject_user_message(options)

        assert result == True
        mock_send.assert_called_once_with(str(options))

    def test_inject_user_message_invalid_type(self):
        """Test error handling for invalid parameter type"""
        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        # Should return False for invalid type
        result = connection.inject_user_message("not an options object")
        assert result == False

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_send_function_call_response_success(self, mock_send):
        """Test successful function call response"""
        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")
        response = FunctionCallResponse(function_call_id="test-id", output="success")

        result = connection.send_function_call_response(response)

        assert result == True
        mock_send.assert_called_once_with(str(response))
