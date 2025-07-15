import pytest
import json
from unittest.mock import patch, MagicMock

from deepgram import (
    DeepgramClient,
    InjectAgentMessageOptions,
)

class TestAgentInjectAgentMessage:
    """Focused unit tests for inject_agent_message functionality"""

    def test_inject_agent_message_options_serialization(self):
        """Test JSON serialization is correct"""
        options = InjectAgentMessageOptions(message="Test agent message")
        result = json.loads(str(options))
        expected = {"type": "InjectAgentMessage", "message": "Test agent message"}
        assert result == expected

    def test_inject_agent_message_options_default_message(self):
        """Test default empty message serialization"""
        options = InjectAgentMessageOptions()
        result = json.loads(str(options))
        expected = {"type": "InjectAgentMessage", "message": ""}
        assert result == expected

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_inject_agent_message_success(self, mock_send):
        """Test successful message injection"""
        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")
        options = InjectAgentMessageOptions(message="Hello from agent")

        result = connection.inject_agent_message(options)

        assert result == True
        mock_send.assert_called_once_with(str(options))

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_inject_agent_message_send_failure(self, mock_send):
        """Test handling of send method failure"""
        mock_send.return_value = False

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")
        options = InjectAgentMessageOptions(message="Hello from agent")

        result = connection.inject_agent_message(options)

        assert result == False
        mock_send.assert_called_once_with(str(options))

    def test_inject_agent_message_invalid_type(self):
        """Test error handling for invalid parameter type"""
        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        # Should return False for invalid type
        result = connection.inject_agent_message("not an options object")
        assert result == False

    def test_inject_agent_message_none_parameter(self):
        """Test error handling for None parameter"""
        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        # Should return False for None parameter
        result = connection.inject_agent_message(None)
        assert result == False

    def test_inject_agent_message_wrong_options_type(self):
        """Test error handling for wrong options type"""
        from deepgram import InjectUserMessageOptions

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        # Should return False for wrong options type
        wrong_options = InjectUserMessageOptions(content="test")
        result = connection.inject_agent_message(wrong_options)
        assert result == False


class TestAsyncAgentInjectAgentMessage:
    """Focused unit tests for async inject_agent_message functionality"""

    @pytest.mark.asyncio
    @patch('deepgram.clients.agent.v1.websocket.async_client.AsyncAgentWebSocketClient.send')
    async def test_async_inject_agent_message_success(self, mock_send):
        """Test successful async message injection"""
        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.asyncwebsocket.v("1")
        options = InjectAgentMessageOptions(message="Hello from async agent")

        result = await connection.inject_agent_message(options)

        assert result == True
        mock_send.assert_called_once_with(str(options))

    @pytest.mark.asyncio
    @patch('deepgram.clients.agent.v1.websocket.async_client.AsyncAgentWebSocketClient.send')
    async def test_async_inject_agent_message_send_failure(self, mock_send):
        """Test handling of async send method failure"""
        mock_send.return_value = False

        client = DeepgramClient("fake-key")
        connection = client.agent.asyncwebsocket.v("1")
        options = InjectAgentMessageOptions(message="Hello from async agent")

        result = await connection.inject_agent_message(options)

        assert result == False
        mock_send.assert_called_once_with(str(options))

    @pytest.mark.asyncio
    async def test_async_inject_agent_message_invalid_type(self):
        """Test error handling for invalid parameter type in async client"""
        client = DeepgramClient("fake-key")
        connection = client.agent.asyncwebsocket.v("1")

        # Should return False for invalid type
        result = await connection.inject_agent_message("not an options object")
        assert result == False

    @pytest.mark.asyncio
    async def test_async_inject_agent_message_none_parameter(self):
        """Test error handling for None parameter in async client"""
        client = DeepgramClient("fake-key")
        connection = client.agent.asyncwebsocket.v("1")

        # Should return False for None parameter
        result = await connection.inject_agent_message(None)
        assert result == False


class TestInjectAgentMessageIntegration:
    """Integration tests comparing inject_user_message and inject_agent_message"""

    def test_options_classes_have_different_types(self):
        """Test that agent and user message options have different types"""
        from deepgram import InjectUserMessageOptions

        agent_options = InjectAgentMessageOptions(message="agent message")
        user_options = InjectUserMessageOptions(content="user message")

        agent_json = json.loads(str(agent_options))
        user_json = json.loads(str(user_options))

        assert agent_json["type"] == "InjectAgentMessage"
        assert user_json["type"] == "InjectUserMessage"
        assert agent_json["type"] != user_json["type"]

    def test_options_classes_have_different_message_fields(self):
        """Test that agent and user message options have different field names"""
        from deepgram import InjectUserMessageOptions

        agent_options = InjectAgentMessageOptions(message="agent message")
        user_options = InjectUserMessageOptions(content="user message")

        agent_json = json.loads(str(agent_options))
        user_json = json.loads(str(user_options))

        # Agent uses 'message' field
        assert "message" in agent_json
        assert agent_json["message"] == "agent message"

        # User uses 'content' field
        assert "content" in user_json
        assert user_json["content"] == "user message"

        # They should not have each other's fields
        assert "content" not in agent_json
        assert "message" not in user_json

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_both_injection_methods_exist(self, mock_send):
        """Test that both injection methods exist and are callable"""
        from deepgram import InjectUserMessageOptions

        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        # Test inject_user_message exists
        user_options = InjectUserMessageOptions(content="user message")
        user_result = connection.inject_user_message(user_options)
        assert user_result == True

        # Test inject_agent_message exists
        agent_options = InjectAgentMessageOptions(message="agent message")
        agent_result = connection.inject_agent_message(agent_options)
        assert agent_result == True

        # Both methods should have been called
        assert mock_send.call_count == 2