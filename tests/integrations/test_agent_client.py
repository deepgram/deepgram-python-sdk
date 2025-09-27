"""Integration tests for Agent client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from contextlib import contextmanager, asynccontextmanager
import httpx
import websockets.exceptions
import json
import asyncio
from json.decoder import JSONDecodeError

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.core.events import EventType
from deepgram.environment import DeepgramClientEnvironment

# Import Agent clients
from deepgram.agent.client import AgentClient, AsyncAgentClient
from deepgram.agent.v1.client import V1Client as AgentV1Client, AsyncV1Client as AgentAsyncV1Client

# Import Agent raw clients
from deepgram.agent.v1.raw_client import RawV1Client as AgentRawV1Client, AsyncRawV1Client as AgentAsyncRawV1Client

# Import Agent socket clients
from deepgram.agent.v1.socket_client import V1SocketClient as AgentV1SocketClient, AsyncV1SocketClient as AgentAsyncV1SocketClient

# Import socket message types
from deepgram.extensions.types.sockets import (
    AgentV1SettingsMessage,
    AgentV1ControlMessage,
    AgentV1MediaMessage,
)


class TestAgentClient:
    """Test cases for Agent Client."""

    def test_agent_client_initialization(self, mock_api_key):
        """Test AgentClient initialization."""
        client = DeepgramClient(api_key=mock_api_key).agent
        assert client is not None
        assert hasattr(client, 'v1')

    def test_async_agent_client_initialization(self, mock_api_key):
        """Test AsyncAgentClient initialization."""
        client = AsyncDeepgramClient(api_key=mock_api_key).agent
        assert client is not None
        assert hasattr(client, 'v1')

    def test_agent_client_with_raw_response(self, mock_api_key):
        """Test AgentClient with_raw_response property."""
        client = DeepgramClient(api_key=mock_api_key).agent
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')

    def test_async_agent_client_with_raw_response(self, mock_api_key):
        """Test AsyncAgentClient with_raw_response property."""
        client = AsyncDeepgramClient(api_key=mock_api_key).agent
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')


class TestAgentRawV1Client:
    """Test cases for Agent V1 Raw Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=Mock(),
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=AsyncMock(),
            timeout=60.0
        )

    def test_sync_agent_raw_client_initialization(self, sync_client_wrapper):
        """Test synchronous agent raw client initialization."""
        client = AgentRawV1Client(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper

    def test_async_agent_raw_client_initialization(self, async_client_wrapper):
        """Test asynchronous agent raw client initialization."""
        client = AgentAsyncRawV1Client(client_wrapper=async_client_wrapper)
        assert client is not None
        assert client._client_wrapper is async_client_wrapper

    @patch('websockets.sync.client.connect')
    def test_sync_agent_connect_success(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test successful synchronous Agent WebSocket connection."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = AgentRawV1Client(client_wrapper=sync_client_wrapper)
        
        with client.connect() as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    @patch('deepgram.agent.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_agent_connect_success(self, mock_websocket_connect, async_client_wrapper, mock_async_websocket):
        """Test successful asynchronous Agent WebSocket connection."""
        mock_websocket_connect.return_value.__aenter__ = AsyncMock(return_value=mock_async_websocket)
        mock_websocket_connect.return_value.__aexit__ = AsyncMock(return_value=None)
        
        client = AgentAsyncRawV1Client(client_wrapper=async_client_wrapper)
        
        async with client.connect() as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    def test_agent_url_construction(self, sync_client_wrapper):
        """Test Agent WebSocket URL construction."""
        client = AgentRawV1Client(client_wrapper=sync_client_wrapper)
        
        # Mock the websocket connection to capture the URL
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.return_value.__enter__ = Mock(return_value=Mock())
            mock_connect.return_value.__exit__ = Mock(return_value=None)
            
            try:
                with client.connect() as connection:
                    pass
            except:
                pass  # We just want to check the URL construction
            
            # Verify the URL was constructed for Agent endpoint
            call_args = mock_connect.call_args
            if call_args and len(call_args[0]) > 0:
                url = call_args[0][0]
                assert "agent" in url.lower()


class TestAgentV1SocketClient:
    """Test cases for Agent V1 Socket Client."""

    def test_agent_sync_socket_client_initialization(self):
        """Test Agent synchronous socket client initialization."""
        mock_ws = Mock()
        client = AgentV1SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_agent_async_socket_client_initialization(self):
        """Test Agent asynchronous socket client initialization."""
        mock_ws = AsyncMock()
        client = AgentAsyncV1SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_agent_sync_send_settings(self):
        """Test Agent synchronous settings message sending."""
        mock_ws = Mock()
        client = AgentV1SocketClient(websocket=mock_ws)
        
        # Mock settings message
        mock_settings_msg = Mock(spec=AgentV1SettingsMessage)
        mock_settings_msg.dict.return_value = {"type": "SettingsConfiguration"}
        
        client.send_settings(mock_settings_msg)
        
        mock_settings_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    def test_agent_sync_send_control(self):
        """Test Agent synchronous control message sending."""
        mock_ws = Mock()
        client = AgentV1SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=AgentV1ControlMessage)
        mock_control_msg.dict.return_value = {"type": "KeepAlive"}
        
        client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    def test_agent_sync_send_media(self, sample_audio_data):
        """Test Agent synchronous media message sending."""
        mock_ws = Mock()
        client = AgentV1SocketClient(websocket=mock_ws)
        
        client.send_media(sample_audio_data)
        
        mock_ws.send.assert_called_once_with(sample_audio_data)

    @pytest.mark.asyncio
    async def test_agent_async_send_settings(self):
        """Test Agent asynchronous settings message sending."""
        mock_ws = AsyncMock()
        client = AgentAsyncV1SocketClient(websocket=mock_ws)
        
        # Mock settings message
        mock_settings_msg = Mock(spec=AgentV1SettingsMessage)
        mock_settings_msg.dict.return_value = {"type": "SettingsConfiguration"}
        
        await client.send_settings(mock_settings_msg)
        
        mock_settings_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_agent_async_send_control(self):
        """Test Agent asynchronous control message sending."""
        mock_ws = AsyncMock()
        client = AgentAsyncV1SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=AgentV1ControlMessage)
        mock_control_msg.dict.return_value = {"type": "KeepAlive"}
        
        await client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_agent_async_send_media(self, sample_audio_data):
        """Test Agent asynchronous media message sending."""
        mock_ws = AsyncMock()
        client = AgentAsyncV1SocketClient(websocket=mock_ws)
        
        await client.send_media(sample_audio_data)
        
        mock_ws.send.assert_called_once_with(sample_audio_data)


class TestAgentIntegrationScenarios:
    """Test Agent API integration scenarios."""

    @patch('websockets.sync.client.connect')
    def test_agent_conversation_workflow(self, mock_websocket_connect, mock_api_key, sample_audio_data):
        """Test complete Agent conversation workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock(side_effect=[
            '{"type": "Welcome", "request_id": "req-123"}',
            '{"type": "ConversationText", "role": "assistant", "content": "Hello!"}',
            b'\x00\x01\x02\x03'  # Audio chunk
        ])
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Welcome", "request_id": "req-123"}',
            '{"type": "ConversationText", "role": "assistant", "content": "Hello!"}',
            b'\x00\x01\x02\x03'  # Audio chunk
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect and interact with agent
        with client.agent.v1.with_raw_response.connect() as connection:
            # Send settings
            connection.send_settings(Mock())
            
            # Send control message
            connection.send_control(Mock())
            
            # Send audio data
            connection.send_media(sample_audio_data)
            
            # Receive agent response
            result = connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('websockets.sync.client.connect')
    def test_agent_function_call_workflow(self, mock_websocket_connect, mock_api_key):
        """Test Agent function call workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock(side_effect=[
            '{"type": "Welcome", "request_id": "func-req-123"}',
            '{"type": "FunctionCallRequest", "function_name": "get_weather", "arguments": {"location": "New York"}}'
        ])
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Welcome", "request_id": "func-req-123"}',
            '{"type": "FunctionCallRequest", "function_name": "get_weather", "arguments": {"location": "New York"}}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect and handle function calls
        with client.agent.v1.with_raw_response.connect() as connection:
            # Send settings with function definitions
            connection.send_settings(Mock())
            
            # Send user message that triggers function call
            connection.send_media(b'User asks about weather')
            
            # Receive function call request
            result = connection.recv()
            assert result is not None
            
            # Send function call response
            connection.send_control(Mock())  # Function response message
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('websockets.sync.client.connect')
    def test_agent_event_driven_workflow(self, mock_websocket_connect, mock_api_key):
        """Test Agent event-driven workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Welcome", "request_id": "event-agent-123"}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Mock event handlers
        on_open = Mock()
        on_message = Mock()
        on_close = Mock()
        on_error = Mock()
        
        # Connect with event handlers
        with client.agent.v1.with_raw_response.connect() as connection:
            # Set up event handlers
            connection.on(EventType.OPEN, on_open)
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, on_close)
            connection.on(EventType.ERROR, on_error)
            
            # Start listening (this will process the mock messages)
            connection.start_listening()
        
        # Verify event handlers were set up
        assert hasattr(connection, 'on')

    @patch('deepgram.agent.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_agent_conversation_workflow(self, mock_websocket_connect, mock_api_key, sample_audio_data):
        """Test async Agent conversation workflow."""
        # Mock async websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=[
            '{"type": "Welcome", "request_id": "async-agent-123"}',
            '{"type": "ConversationText", "role": "assistant", "content": "Hello from async agent!"}'
        ])
        
        async def mock_aiter():
            yield '{"type": "Welcome", "request_id": "async-agent-123"}'
            yield '{"type": "ConversationText", "role": "assistant", "content": "Hello from async agent!"}'
        
        mock_ws.__aiter__ = Mock(return_value=mock_aiter())
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize async client
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Connect and interact with agent
        async with client.agent.v1.with_raw_response.connect() as connection:
            # Send settings
            await connection.send_settings(Mock())
            
            # Send control message
            await connection.send_control(Mock())
            
            # Send audio data
            await connection.send_media(sample_audio_data)
            
            # Receive agent response
            result = await connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('deepgram.agent.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_agent_function_call_workflow(self, mock_websocket_connect, mock_api_key):
        """Test async Agent function call workflow."""
        # Mock async websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=[
            '{"type": "Welcome", "request_id": "async-func-123"}',
            '{"type": "FunctionCallRequest", "function_name": "get_weather", "arguments": {"location": "San Francisco"}}'
        ])
        
        async def mock_aiter():
            yield '{"type": "Welcome", "request_id": "async-func-123"}'
            yield '{"type": "FunctionCallRequest", "function_name": "get_weather", "arguments": {"location": "San Francisco"}}'
        
        mock_ws.__aiter__ = Mock(return_value=mock_aiter())
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize async client
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Connect and handle function calls
        async with client.agent.v1.with_raw_response.connect() as connection:
            # Send settings with function definitions
            await connection.send_settings(Mock())
            
            # Send user message that triggers function call
            await connection.send_media(b'User asks about weather in SF')
            
            # Receive function call request
            result = await connection.recv()
            assert result is not None
            
            # Send function call response
            await connection.send_control(Mock())  # Function response message
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    def test_complete_agent_workflow_sync(self, mock_api_key):
        """Test complete Agent workflow using sync client."""
        with patch('websockets.sync.client.connect') as mock_websocket_connect:
            # Mock websocket connection
            mock_ws = Mock()
            mock_ws.send = Mock()
            mock_ws.__iter__ = Mock(return_value=iter([
                '{"type": "Welcome", "request_id": "complete-sync-123"}'
            ]))
            mock_ws.__enter__ = Mock(return_value=mock_ws)
            mock_ws.__exit__ = Mock(return_value=None)
            mock_websocket_connect.return_value = mock_ws
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested agent functionality
            with client.agent.v1.with_raw_response.connect() as connection:
                # Send initial settings
                connection.send_settings(Mock())
                
                # Send user audio
                connection.send_media(b'Hello agent')
                
                # Process response
                for message in connection:
                    if isinstance(message, dict) and message.get('type') == 'Welcome':
                        break
            
            # Verify the connection was established
            mock_websocket_connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_agent_workflow_async(self, mock_api_key):
        """Test complete Agent workflow using async client."""
        with patch('deepgram.agent.v1.raw_client.websockets_client_connect') as mock_websocket_connect:
            # Mock async websocket connection
            mock_ws = AsyncMock()
            mock_ws.send = AsyncMock()
            
            async def mock_aiter():
                yield '{"type": "Welcome", "request_id": "complete-async-123"}'
            
            mock_ws.__aiter__ = Mock(return_value=mock_aiter())
            mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
            mock_ws.__aexit__ = AsyncMock(return_value=None)
            mock_websocket_connect.return_value = mock_ws
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested agent functionality
            async with client.agent.v1.with_raw_response.connect() as connection:
                # Send initial settings
                await connection.send_settings(Mock())
                
                # Send user audio
                await connection.send_media(b'Hello async agent')
                
                # Process response
                async for message in connection:
                    if isinstance(message, dict) and message.get('type') == 'Welcome':
                        break
            
            # Verify the connection was established
            mock_websocket_connect.assert_called_once()

    def test_agent_client_property_isolation(self, mock_api_key):
        """Test that agent clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        # Verify clients are different instances
        assert client1.agent is not client2.agent
        
        # Verify nested clients are also different
        agent1 = client1.agent.v1
        agent2 = client2.agent.v1
        
        assert agent1 is not agent2

    @pytest.mark.asyncio
    async def test_mixed_sync_async_agent_clients(self, mock_api_key):
        """Test mixing sync and async agent clients."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Verify clients are different types
        assert type(sync_client.agent) != type(async_client.agent)
        
        # Verify nested clients are also different types
        sync_agent = sync_client.agent.v1
        async_agent = async_client.agent.v1
        
        assert type(sync_agent) != type(async_agent)
        assert isinstance(sync_agent, AgentV1Client)
        assert isinstance(async_agent, AgentAsyncV1Client)


class TestAgentErrorHandling:
    """Test Agent client error handling."""

    @patch('websockets.sync.client.connect')
    def test_websocket_connection_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test WebSocket connection error handling."""
        mock_websocket_connect.side_effect = websockets.exceptions.ConnectionClosedError(None, None)
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(websockets.exceptions.ConnectionClosedError):
            with client.agent.v1.with_raw_response.connect() as connection:
                pass

    @patch('websockets.sync.client.connect')
    def test_generic_websocket_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test generic WebSocket error handling."""
        mock_websocket_connect.side_effect = Exception("Generic Agent WebSocket error")
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(Exception) as exc_info:
            with client.agent.v1.with_raw_response.connect() as connection:
                pass
        
        assert "Generic Agent WebSocket error" in str(exc_info.value)

    @patch('deepgram.agent.v1.raw_client.websockets_sync_client.connect')
    def test_agent_invalid_credentials_error(self, mock_websocket_connect, mock_api_key):
        """Test Agent connection with invalid credentials."""
        mock_websocket_connect.side_effect = websockets.exceptions.InvalidStatusCode(
            status_code=401, headers={}
        )

        client = DeepgramClient(api_key=mock_api_key)

        with pytest.raises(ApiError) as exc_info:
            with client.agent.v1.with_raw_response.connect() as connection:
                pass

        assert exc_info.value.status_code == 401
        assert "invalid credentials" in exc_info.value.body.lower()

    @patch('deepgram.agent.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_websocket_connection_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test async WebSocket connection error handling."""
        mock_websocket_connect.side_effect = websockets.exceptions.ConnectionClosedError(None, None)
        
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(websockets.exceptions.ConnectionClosedError):
            async with client.agent.v1.with_raw_response.connect() as connection:
                pass

    def test_client_wrapper_integration(self, mock_api_key):
        """Test integration with client wrapper."""
        client = DeepgramClient(api_key=mock_api_key).agent
        assert client._client_wrapper is not None
        assert client._client_wrapper.api_key == mock_api_key

    def test_socket_client_error_scenarios(self, sample_audio_data):
        """Test Agent socket client error scenarios."""
        mock_ws = Mock()
        mock_ws.send = Mock(side_effect=Exception("Send error"))
        
        client = AgentV1SocketClient(websocket=mock_ws)
        
        # Test that send errors are properly propagated
        with pytest.raises(Exception) as exc_info:
            client.send_media(sample_audio_data)
        
        assert "Send error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_async_socket_client_error_scenarios(self, sample_audio_data):
        """Test async Agent socket client error scenarios."""
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock(side_effect=Exception("Async send error"))
        
        client = AgentAsyncV1SocketClient(websocket=mock_ws)
        
        # Test that async send errors are properly propagated
        with pytest.raises(Exception) as exc_info:
            await client.send_media(sample_audio_data)
        
        assert "Async send error" in str(exc_info.value)
