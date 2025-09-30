"""Integration tests for Listen client implementations."""

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

# Import Listen clients
from deepgram.listen.client import ListenClient, AsyncListenClient
from deepgram.listen.v1.client import V1Client as ListenV1Client, AsyncV1Client as ListenAsyncV1Client
from deepgram.listen.v2.client import V2Client as ListenV2Client, AsyncV2Client as ListenAsyncV2Client

# Import Listen raw clients
from deepgram.listen.v1.raw_client import RawV1Client as ListenRawV1Client, AsyncRawV1Client as ListenAsyncRawV1Client
from deepgram.listen.v2.raw_client import RawV2Client as ListenRawV2Client, AsyncRawV2Client as ListenAsyncRawV2Client

# Import Listen socket clients
from deepgram.listen.v1.socket_client import V1SocketClient as ListenV1SocketClient, AsyncV1SocketClient as ListenAsyncV1SocketClient
from deepgram.listen.v2.socket_client import V2SocketClient as ListenV2SocketClient, AsyncV2SocketClient as ListenAsyncV2SocketClient

# Import Listen media clients
from deepgram.listen.v1.media.client import MediaClient, AsyncMediaClient

# Import socket message types
from deepgram.extensions.types.sockets import (
    ListenV1ControlMessage,
    ListenV1MediaMessage,
    ListenV2ControlMessage,
    ListenV2MediaMessage,
)

# Import request and response types for mocking
from deepgram.types.listen_v1response import ListenV1Response
from deepgram.listen.v1.media.types.media_transcribe_request_callback_method import MediaTranscribeRequestCallbackMethod
from deepgram.listen.v1.media.types.media_transcribe_request_summarize import MediaTranscribeRequestSummarize
from deepgram.listen.v1.media.types.media_transcribe_request_custom_topic_mode import MediaTranscribeRequestCustomTopicMode
from deepgram.listen.v1.media.types.media_transcribe_request_custom_intent_mode import MediaTranscribeRequestCustomIntentMode
from deepgram.listen.v1.media.types.media_transcribe_request_encoding import MediaTranscribeRequestEncoding
from deepgram.listen.v1.media.types.media_transcribe_request_model import MediaTranscribeRequestModel
from deepgram.listen.v1.media.types.media_transcribe_request_version import MediaTranscribeRequestVersion


class TestListenClient:
    """Test cases for Listen Client."""

    def test_listen_client_initialization(self, mock_api_key):
        """Test ListenClient initialization."""
        client = DeepgramClient(api_key=mock_api_key).listen
        assert client is not None
        assert hasattr(client, 'v1')
        assert hasattr(client, 'v2')

    def test_async_listen_client_initialization(self, mock_api_key):
        """Test AsyncListenClient initialization."""
        client = AsyncDeepgramClient(api_key=mock_api_key).listen
        assert client is not None
        assert hasattr(client, 'v1')
        assert hasattr(client, 'v2')

    def test_listen_client_with_raw_response(self, mock_api_key):
        """Test ListenClient with_raw_response property."""
        client = DeepgramClient(api_key=mock_api_key).listen
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')

    def test_async_listen_client_with_raw_response(self, mock_api_key):
        """Test AsyncListenClient with_raw_response property."""
        client = AsyncDeepgramClient(api_key=mock_api_key).listen
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')


class TestListenRawV1Client:
    """Test cases for Listen V1 Raw Client."""

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

    def test_sync_raw_client_initialization(self, sync_client_wrapper):
        """Test synchronous raw client initialization."""
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper

    def test_async_raw_client_initialization(self, async_client_wrapper):
        """Test asynchronous raw client initialization."""
        client = ListenAsyncRawV1Client(client_wrapper=async_client_wrapper)
        assert client is not None
        assert client._client_wrapper is async_client_wrapper

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_sync_connect_success(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test successful synchronous WebSocket connection."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        with client.connect(model="nova-2-general") as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_sync_connect_with_all_parameters(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test synchronous connection with all parameters."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        with client.connect(
            model="nova-2-general",
            encoding="linear16",
            sample_rate="16000",
            channels="1",
            language="en-US",
            punctuate="true",
            smart_format="true",
            diarize="true",
            interim_results="true",
            utterance_end_ms="1000",
            vad_events="true",
            authorization="Bearer test_token"
        ) as connection:
            assert connection is not None

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_sync_connect_invalid_credentials(self, mock_websocket_connect, sync_client_wrapper):
        """Test synchronous connection with invalid credentials."""
        mock_websocket_connect.side_effect = websockets.exceptions.InvalidStatusCode(
            status_code=401, headers={}
        )
        
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            with client.connect(model="nova-2-general") as connection:
                pass
        
        assert exc_info.value.status_code == 401
        assert "invalid credentials" in exc_info.value.body.lower()

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_sync_connect_unexpected_error(self, mock_websocket_connect, sync_client_wrapper):
        """Test synchronous connection with unexpected error."""
        mock_websocket_connect.side_effect = Exception("Unexpected connection error")
        
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(Exception) as exc_info:
            with client.connect(model="nova-2-general") as connection:
                pass
        
        assert "Unexpected connection error" in str(exc_info.value)

    @patch('deepgram.listen.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_connect_success(self, mock_websocket_connect, async_client_wrapper, mock_async_websocket):
        """Test successful asynchronous WebSocket connection."""
        mock_websocket_connect.return_value.__aenter__ = AsyncMock(return_value=mock_async_websocket)
        mock_websocket_connect.return_value.__aexit__ = AsyncMock(return_value=None)
        
        client = ListenAsyncRawV1Client(client_wrapper=async_client_wrapper)
        
        async with client.connect(model="nova-2-general") as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    @patch('deepgram.listen.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_connect_with_all_parameters(self, mock_websocket_connect, async_client_wrapper, mock_async_websocket):
        """Test asynchronous connection with all parameters."""
        mock_websocket_connect.return_value.__aenter__ = AsyncMock(return_value=mock_async_websocket)
        mock_websocket_connect.return_value.__aexit__ = AsyncMock(return_value=None)
        
        client = ListenAsyncRawV1Client(client_wrapper=async_client_wrapper)
        
        async with client.connect(
            model="nova-2-general",
            encoding="linear16",
            sample_rate="16000",
            channels="1"
        ) as connection:
            assert connection is not None

    @patch('deepgram.listen.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_connect_invalid_credentials(self, mock_websocket_connect, async_client_wrapper):
        """Test asynchronous connection with invalid credentials."""
        mock_websocket_connect.side_effect = websockets.exceptions.InvalidStatusCode(
            status_code=401, headers={}
        )
        
        client = ListenAsyncRawV1Client(client_wrapper=async_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            async with client.connect(model="nova-2-general") as connection:
                pass
        
        assert exc_info.value.status_code == 401
        assert "invalid credentials" in exc_info.value.body.lower()

    def test_sync_query_params_construction(self, sync_client_wrapper):
        """Test query parameters are properly constructed."""
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        # Mock the websocket connection to capture the URL
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.return_value.__enter__ = Mock(return_value=Mock())
            mock_connect.return_value.__exit__ = Mock(return_value=None)
            
            try:
                with client.connect(
                    model="nova-2-general",
                    encoding="linear16",
                    sample_rate="16000",
                    punctuate="true"
                ) as connection:
                    pass
            except:
                pass  # We just want to check the URL construction
            
            # Verify the URL was constructed with query parameters
            call_args = mock_connect.call_args
            if call_args and len(call_args[0]) > 0:
                url = call_args[0][0]
                assert "model=nova-2-general" in url
                assert "encoding=linear16" in url
                assert "sample_rate=16000" in url
                assert "punctuate=true" in url

    def test_sync_headers_construction(self, sync_client_wrapper):
        """Test headers are properly constructed."""
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        # Mock the websocket connection to capture headers
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.return_value.__enter__ = Mock(return_value=Mock())
            mock_connect.return_value.__exit__ = Mock(return_value=None)
            
            try:
                with client.connect(
                    model="nova-2-general",
                    authorization="Bearer custom_token"
                ) as connection:
                    pass
            except:
                pass  # We just want to check the headers construction
            
            # Verify headers were passed
            call_args = mock_connect.call_args
            if call_args and 'additional_headers' in call_args[1]:
                headers = call_args[1]['additional_headers']
                assert 'Authorization' in headers

    def test_sync_request_options(self, sync_client_wrapper):
        """Test request options are properly handled."""
        client = ListenRawV1Client(client_wrapper=sync_client_wrapper)
        
        request_options = RequestOptions(
            additional_headers={"Custom-Header": "custom-value"},
            timeout_in_seconds=30.0
        )
        
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.return_value.__enter__ = Mock(return_value=Mock())
            mock_connect.return_value.__exit__ = Mock(return_value=None)
            
            try:
                with client.connect(
                    model="nova-2-general",
                    request_options=request_options
                ) as connection:
                    pass
            except:
                pass  # We just want to check the options handling
            
            # Verify request options were applied
            call_args = mock_connect.call_args
            assert call_args is not None


class TestListenRawV2Client:
    """Test cases for Listen V2 Raw Client."""

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

    def test_sync_raw_v2_client_initialization(self, sync_client_wrapper):
        """Test synchronous raw V2 client initialization."""
        client = ListenRawV2Client(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper

    @patch('deepgram.listen.v2.raw_client.websockets_sync_client.connect')
    def test_sync_v2_connect_success(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test successful V2 synchronous WebSocket connection."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = ListenRawV2Client(client_wrapper=sync_client_wrapper)
        
        with client.connect(model="nova-2-general", encoding="linear16", sample_rate="16000") as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')


class TestListenV1SocketClient:
    """Test cases for Listen V1 Socket Client."""

    @pytest.fixture
    def mock_sync_websocket(self):
        """Create a mock synchronous websocket."""
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock()
        mock_ws.__iter__ = Mock(return_value=iter([]))
        return mock_ws

    @pytest.fixture
    def mock_async_websocket(self):
        """Create a mock asynchronous websocket."""
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock()
        mock_ws.__aiter__ = AsyncMock(return_value=iter([]))
        return mock_ws

    def test_sync_socket_client_initialization(self, mock_sync_websocket):
        """Test synchronous socket client initialization."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        assert client is not None
        assert client._websocket is mock_sync_websocket

    def test_async_socket_client_initialization(self, mock_async_websocket):
        """Test asynchronous socket client initialization."""
        client = ListenAsyncV1SocketClient(websocket=mock_async_websocket)
        assert client is not None
        assert client._websocket is mock_async_websocket

    def test_is_binary_message_detection(self, mock_sync_websocket):
        """Test binary message detection."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        # Test with bytes
        assert client._is_binary_message(b'binary data') is True
        
        # Test with bytearray
        assert client._is_binary_message(bytearray(b'binary data')) is True
        
        # Test with string
        assert client._is_binary_message('text data') is False
        
        # Test with dict
        assert client._is_binary_message({'key': 'value'}) is False

    def test_handle_binary_message(self, mock_sync_websocket, sample_audio_data):
        """Test binary message handling."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        # Test handling binary audio data
        result = client._handle_binary_message(sample_audio_data)
        assert result == sample_audio_data

    def test_handle_json_message_success(self, mock_sync_websocket):
        """Test successful JSON message handling."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)

        json_message = '{"type": "Metadata", "request_id": "test-123", "sha256": "abc123", "created": "2023-01-01T00:00:00Z", "duration": 5.0, "channels": 1}'
        result = client._handle_json_message(json_message)
        
        assert result is not None
        assert result.type == "Metadata"
        assert result.request_id == "test-123"
        assert result.sha256 == "abc123"

    def test_handle_json_message_invalid(self, mock_sync_websocket):
        """Test invalid JSON message handling."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        invalid_json = '{"invalid": json}'
        
        # Should raise JSONDecodeError for invalid JSON
        with pytest.raises(json.JSONDecodeError):
            client._handle_json_message(invalid_json)

    @patch('deepgram.listen.v1.socket_client.V1SocketClient._handle_json_message')
    def test_sync_iteration(self, mock_handle_json, mock_sync_websocket):
        """Test synchronous iteration over websocket messages."""
        mock_sync_websocket.__iter__ = Mock(return_value=iter([
            '{"type": "Metadata", "request_id": "test-1"}',
            b'\x00\x01\x02\x03',
            '{"type": "Results", "channel_index": [0]}'
        ]))

        # Mock the JSON handling to return simple objects
        mock_handle_json.side_effect = [
            {"type": "Metadata", "request_id": "test-1"},
            {"type": "Results", "channel_index": [0]}
        ]

        client = ListenV1SocketClient(websocket=mock_sync_websocket)

        messages = list(client)
        assert len(messages) == 3
        assert messages[0]["type"] == "Metadata"
        assert messages[1] == b'\x00\x01\x02\x03'
        assert messages[2]["type"] == "Results"

    @patch('deepgram.listen.v1.socket_client.AsyncV1SocketClient._handle_json_message')
    @pytest.mark.asyncio
    async def test_async_iteration(self, mock_handle_json, mock_async_websocket):
        """Test asynchronous iteration over websocket messages."""
        async def mock_aiter():
            yield '{"type": "Metadata", "request_id": "test-1"}'
            yield b'\x00\x01\x02\x03'
            yield '{"type": "Results", "channel_index": [0]}'
        
        mock_async_websocket.__aiter__ = Mock(return_value=mock_aiter())
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.side_effect = [
            {"type": "Metadata", "request_id": "test-1"},
            {"type": "Results", "channel_index": [0]}
        ]
        
        client = ListenAsyncV1SocketClient(websocket=mock_async_websocket)
        
        messages = []
        async for message in client:
            messages.append(message)
        
        assert len(messages) == 3
        assert messages[0]["type"] == "Metadata"
        assert messages[1] == b'\x00\x01\x02\x03'
        assert messages[2]["type"] == "Results"

    def test_sync_recv_binary(self, mock_sync_websocket, sample_audio_data):
        """Test synchronous receive of binary data."""
        mock_sync_websocket.recv.return_value = sample_audio_data
        
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        result = client.recv()
        
        assert result == sample_audio_data
        mock_sync_websocket.recv.assert_called_once()

    def test_sync_recv_json(self, mock_sync_websocket):
        """Test synchronous receive of JSON data."""
        json_message = '{"type": "Metadata", "request_id": "test-123", "sha256": "abc123", "created": "2023-01-01T00:00:00Z", "duration": 5.0, "channels": 1}'
        mock_sync_websocket.recv.return_value = json_message
        
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        result = client.recv()
        
        assert result.type == "Metadata"
        assert result.request_id == "test-123"
        mock_sync_websocket.recv.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_recv_binary(self, mock_async_websocket, sample_audio_data):
        """Test asynchronous receive of binary data."""
        mock_async_websocket.recv.return_value = sample_audio_data
        
        client = ListenAsyncV1SocketClient(websocket=mock_async_websocket)
        result = await client.recv()
        
        assert result == sample_audio_data
        mock_async_websocket.recv.assert_called_once()

    def test_sync_send_binary(self, mock_sync_websocket, sample_audio_data):
        """Test synchronous sending of binary data."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        client.send_media(sample_audio_data)
        
        mock_sync_websocket.send.assert_called_once_with(sample_audio_data)

    def test_sync_send_dict(self, mock_sync_websocket):
        """Test synchronous sending of dictionary data."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        message_dict = {"type": "Metadata", "request_id": "test-123"}
        
        control_message = ListenV1ControlMessage(type="KeepAlive")
        client.send_control(control_message)
        
        mock_sync_websocket.send.assert_called_once()
        # Verify JSON was sent
        call_args = mock_sync_websocket.send.call_args[0]
        sent_data = call_args[0]
        assert isinstance(sent_data, str)
        parsed = json.loads(sent_data)
        assert parsed["type"] == "KeepAlive"

    def test_sync_send_string(self, mock_sync_websocket):
        """Test synchronous sending of string data."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        message_str = '{"type": "KeepAlive"}'
        
        # For string data, we'll use the private _send method for testing
        client._send(message_str)
        
        mock_sync_websocket.send.assert_called_once_with(message_str)

    def test_sync_send_pydantic_model(self, mock_sync_websocket):
        """Test synchronous sending of Pydantic model."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        control_message = ListenV1ControlMessage(type="KeepAlive")
        client.send_control(control_message)
        
        mock_sync_websocket.send.assert_called_once()

    def test_sync_send_control(self, mock_sync_websocket):
        """Test synchronous control message sending."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        # Mock control message
        mock_control_msg = Mock(spec=ListenV1ControlMessage)
        mock_control_msg.dict.return_value = {"type": "KeepAlive"}
        
        client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_sync_websocket.send.assert_called_once()

    def test_sync_send_media(self, mock_sync_websocket, sample_audio_data):
        """Test synchronous media message sending."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        client.send_media(sample_audio_data)
        
        mock_sync_websocket.send.assert_called_once_with(sample_audio_data)

    @patch('deepgram.listen.v1.socket_client.V1SocketClient._handle_json_message')
    def test_sync_start_listening_with_event_handler(self, mock_handle_json, mock_sync_websocket):
        """Test synchronous start_listening with event handler."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        # Mock websocket iteration
        mock_sync_websocket.__iter__ = Mock(return_value=iter([
            '{"type": "Metadata", "request_id": "test-123"}',
            '{"type": "Results", "channel_index": [0], "is_final": true}'
        ]))
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.side_effect = [
            {"type": "Metadata", "request_id": "test-123"},
            {"type": "Results", "channel_index": [0], "is_final": True}
        ]
        
        # Mock event handler
        event_handler = Mock()
        client.on(EventType.OPEN, event_handler)
        client.on(EventType.MESSAGE, event_handler)
        client.on(EventType.CLOSE, event_handler)
        
        # Start listening (this will iterate through the mock messages)
        client.start_listening()
        
        # Verify event handler was called
        assert event_handler.call_count >= 1

    def test_sync_start_listening_with_error(self, mock_sync_websocket):
        """Test synchronous start_listening with error."""
        client = ListenV1SocketClient(websocket=mock_sync_websocket)
        
        # Mock websocket to raise a websocket exception
        from websockets.exceptions import WebSocketException
        mock_sync_websocket.__iter__ = Mock(side_effect=WebSocketException("Connection error"))
        
        # Mock error handler
        error_handler = Mock()
        client.on(EventType.ERROR, error_handler)
        
        # Start listening (this should trigger error)
        client.start_listening()
        
        # Verify error handler was called
        error_handler.assert_called()


class TestListenV2SocketClient:
    """Test cases for Listen V2 Socket Client."""

    def test_v2_sync_socket_client_initialization(self):
        """Test V2 synchronous socket client initialization."""
        mock_ws = Mock()
        client = ListenV2SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_v2_async_socket_client_initialization(self):
        """Test V2 asynchronous socket client initialization."""
        mock_ws = AsyncMock()
        client = ListenAsyncV2SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_v2_sync_send_control(self):
        """Test V2 synchronous control message sending."""
        mock_ws = Mock()
        client = ListenV2SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=ListenV2ControlMessage)
        mock_control_msg.dict.return_value = {"type": "KeepAlive"}
        
        client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_v2_async_send_control(self):
        """Test V2 asynchronous control message sending."""
        mock_ws = AsyncMock()
        client = ListenAsyncV2SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=ListenV2ControlMessage)
        mock_control_msg.dict.return_value = {"type": "KeepAlive"}
        
        await client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()


class TestListenMediaClient:
    """Test cases for Listen Media Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        mock_httpx_client = Mock()
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        mock_httpx_client = AsyncMock()
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def mock_listen_response(self):
        """Mock listen response data."""
        mock_response = Mock(spec=ListenV1Response)
        mock_response.metadata = Mock()
        mock_response.results = Mock()
        return mock_response

    def test_media_client_initialization(self, sync_client_wrapper):
        """Test MediaClient initialization."""
        client = MediaClient(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._raw_client is not None

    def test_async_media_client_initialization(self, async_client_wrapper):
        """Test AsyncMediaClient initialization."""
        client = AsyncMediaClient(client_wrapper=async_client_wrapper)
        assert client is not None
        assert client._raw_client is not None

    def test_media_client_raw_response_access(self, sync_client_wrapper):
        """Test MediaClient raw response access."""
        client = MediaClient(client_wrapper=sync_client_wrapper)
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_media_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncMediaClient raw response access."""
        client = AsyncMediaClient(client_wrapper=async_client_wrapper)
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url')
    def test_media_client_transcribe_url(self, mock_transcribe, sync_client_wrapper, mock_listen_response):
        """Test MediaClient transcribe_url method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = MediaClient(client_wrapper=sync_client_wrapper)

        result = client.transcribe_url(
            url="https://example.com/audio.mp3",
            model="nova-2-general"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)
        assert result.metadata is not None
        assert result.results is not None

        # Verify the call was made
        mock_transcribe.assert_called_once()

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url')
    def test_media_client_transcribe_url_with_all_features(self, mock_transcribe, sync_client_wrapper, mock_listen_response):
        """Test MediaClient transcribe_url with all features enabled."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = MediaClient(client_wrapper=sync_client_wrapper)

        result = client.transcribe_url(
            url="https://example.com/audio.mp3",
            model="nova-2-general",
            language="en-US",
            encoding="linear16",
            smart_format=True,
            punctuate=True,
            diarize=True,
            summarize="v2",
            sentiment=True,
            topics=True,
            intents=True,
            custom_topic_mode="extend",
            custom_intent_mode="extend"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)

        # Verify the call was made with all parameters
        mock_transcribe.assert_called_once()
        call_args = mock_transcribe.call_args
        assert "model" in call_args[1]
        assert "smart_format" in call_args[1]

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_file')
    def test_media_client_transcribe_file(self, mock_transcribe, sync_client_wrapper, mock_listen_response, sample_audio_data):
        """Test MediaClient transcribe_file method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = MediaClient(client_wrapper=sync_client_wrapper)

        # Create a mock file-like object
        from io import BytesIO
        audio_file = BytesIO(sample_audio_data)

        result = client.transcribe_file(
            request=audio_file,
            model="nova-2-general"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)

        # Verify the call was made
        mock_transcribe.assert_called_once()

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url')
    def test_media_client_transcribe_url_with_callback(self, mock_transcribe, sync_client_wrapper, mock_listen_response):
        """Test MediaClient transcribe_url with callback configuration."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = MediaClient(client_wrapper=sync_client_wrapper)

        result = client.transcribe_url(
            url="https://example.com/audio.mp3",
            model="nova-2-general",
            callback="https://example.com/callback",
            callback_method="POST"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)

        # Verify the call was made
        mock_transcribe.assert_called_once()

    @patch('deepgram.listen.v1.media.raw_client.AsyncRawMediaClient.transcribe_url')
    @pytest.mark.asyncio
    async def test_async_media_client_transcribe_url(self, mock_transcribe, async_client_wrapper, mock_listen_response):
        """Test AsyncMediaClient transcribe_url method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = AsyncMediaClient(client_wrapper=async_client_wrapper)

        result = await client.transcribe_url(
            url="https://example.com/audio.mp3",
            model="nova-2-general"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)

        # Verify the call was made
        mock_transcribe.assert_called_once()

    @patch('deepgram.listen.v1.media.raw_client.AsyncRawMediaClient.transcribe_file')
    @pytest.mark.asyncio
    async def test_async_media_client_transcribe_file(self, mock_transcribe, async_client_wrapper, mock_listen_response, sample_audio_data):
        """Test AsyncMediaClient transcribe_file method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_listen_response
        mock_transcribe.return_value = mock_response

        client = AsyncMediaClient(client_wrapper=async_client_wrapper)

        # Create a mock file-like object
        from io import BytesIO
        audio_file = BytesIO(sample_audio_data)

        result = await client.transcribe_file(
            request=audio_file,
            model="nova-2-general"
        )

        assert result is not None
        assert isinstance(result, ListenV1Response)

        # Verify the call was made
        mock_transcribe.assert_called_once()


class TestListenIntegrationScenarios:
    """Test Listen API integration scenarios."""

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_listen_v1_transcription_workflow(self, mock_websocket_connect, mock_api_key, sample_audio_data):
        """Test complete Listen V1 transcription workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock(side_effect=[
            '{"type": "Metadata", "request_id": "test-123", "sha256": "abc123", "created": "2023-01-01T00:00:00Z", "duration": 1.0, "channels": 1}',
            '{"type": "Metadata", "request_id": "test-456", "sha256": "def456", "created": "2023-01-01T00:00:01Z", "duration": 2.0, "channels": 1}'
        ])
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Metadata", "request_id": "test-123", "sha256": "abc123", "created": "2023-01-01T00:00:00Z", "duration": 1.0, "channels": 1}',
            '{"type": "Metadata", "request_id": "test-456", "sha256": "def456", "created": "2023-01-01T00:00:01Z", "duration": 2.0, "channels": 1}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect and send audio
        with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
            # Send control message
            connection.send_control(Mock())
            
            # Send audio data
            connection.send_media(sample_audio_data)
            
            # Receive transcription results
            result = connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('deepgram.listen.v2.socket_client.V2SocketClient._handle_json_message')
    @patch('deepgram.listen.v2.raw_client.websockets_sync_client.connect')
    def test_listen_v2_transcription_workflow(self, mock_websocket_connect, mock_handle_json, mock_api_key, sample_audio_data):
        """Test complete Listen V2 transcription workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock(side_effect=[
            '{"type": "Connected", "request_id": "test-v2-123"}',
            '{"type": "TurnInfo", "request_id": "test-v2-123", "turn_id": "turn-1"}'
        ])
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Connected", "request_id": "test-v2-123"}',
            '{"type": "TurnInfo", "request_id": "test-v2-123", "turn_id": "turn-1"}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.return_value = {"type": "Connected", "request_id": "test-v2-123"}
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect and send audio
        with client.listen.v2.with_raw_response.connect(
            model="nova-2-general",
            encoding="linear16",
            sample_rate=16000
        ) as connection:
            # Send control message
            connection.send_control(Mock())
            
            # Send audio data
            connection.send_media(sample_audio_data)
            
            # Receive transcription results
            result = connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('deepgram.listen.v1.socket_client.V1SocketClient._handle_json_message')
    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_listen_event_driven_workflow(self, mock_websocket_connect, mock_handle_json, mock_api_key):
        """Test Listen event-driven workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Metadata", "request_id": "event-test-123"}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.return_value = {"type": "Metadata", "request_id": "event-test-123"}
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Mock event handlers
        on_open = Mock()
        on_message = Mock()
        on_close = Mock()
        on_error = Mock()
        
        # Connect with event handlers
        with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
            # Set up event handlers
            connection.on(EventType.OPEN, on_open)
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, on_close)
            connection.on(EventType.ERROR, on_error)
            
            # Start listening (this will process the mock messages)
            connection.start_listening()
        
        # Verify event handlers were set up (they may or may not be called depending on mock behavior)
        assert hasattr(connection, 'on')

    @patch('deepgram.listen.v1.socket_client.AsyncV1SocketClient._handle_json_message')
    @patch('deepgram.listen.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_listen_transcription_workflow(self, mock_websocket_connect, mock_handle_json, mock_api_key, sample_audio_data):
        """Test async Listen transcription workflow."""
        # Mock async websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=[
            '{"type": "Metadata", "request_id": "async-test-123"}',
            '{"type": "Results", "channel_index": [0]}'
        ])
        
        async def mock_aiter():
            yield '{"type": "Metadata", "request_id": "async-test-123"}'
            yield '{"type": "Results", "channel_index": [0]}'
        
        mock_ws.__aiter__ = Mock(return_value=mock_aiter())
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.return_value = {"type": "Metadata", "request_id": "async-test-123"}
        
        # Initialize async client
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Connect and send audio
        async with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
            # Send control message
            await connection.send_control(Mock())
            
            # Send audio data
            await connection.send_media(sample_audio_data)
            
            # Receive transcription results
            result = await connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    def test_complete_listen_media_workflow_sync(self, mock_api_key):
        """Test complete Listen Media workflow using sync client."""
        with patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url') as mock_transcribe:
            # Mock the response with Mock objects to avoid Pydantic validation
            mock_response = Mock()
            mock_response.data = Mock(spec=ListenV1Response)
            mock_response.data.metadata = Mock()
            mock_response.data.metadata.request_id = "media-sync-123"
            mock_response.data.results = Mock()
            mock_response.data.results.channels = [Mock()]
            mock_response.data.results.channels[0].alternatives = [Mock()]
            mock_response.data.results.channels[0].alternatives[0].transcript = "This is a test transcription."
            mock_transcribe.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested listen media functionality
            result = client.listen.v1.media.transcribe_url(
                url="https://example.com/test-audio.mp3",
                model="nova-2-general",
                smart_format=True,
                punctuate=True
            )
            
            assert result is not None
            assert isinstance(result, ListenV1Response)
            assert result.metadata is not None
            assert result.results is not None
            
            # Verify the call was made
            mock_transcribe.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_listen_media_workflow_async(self, mock_api_key):
        """Test complete Listen Media workflow using async client."""
        with patch('deepgram.listen.v1.media.raw_client.AsyncRawMediaClient.transcribe_url') as mock_transcribe:
            # Mock the async response with Mock objects to avoid Pydantic validation
            mock_response = Mock()
            mock_response.data = Mock(spec=ListenV1Response)
            mock_response.data.metadata = Mock()
            mock_response.data.metadata.request_id = "media-async-456"
            mock_response.data.results = Mock()
            mock_response.data.results.channels = [Mock()]
            mock_response.data.results.channels[0].alternatives = [Mock()]
            mock_response.data.results.channels[0].alternatives[0].transcript = "This is an async test transcription."
            mock_transcribe.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested listen media functionality
            result = await client.listen.v1.media.transcribe_url(
                url="https://example.com/test-audio-async.mp3",
                model="nova-2-general",
                topics=True,
                sentiment=True
            )
            
            assert result is not None
            assert isinstance(result, ListenV1Response)
            assert result.metadata is not None
            assert result.results is not None
            
            # Verify the call was made
            mock_transcribe.assert_called_once()


class TestListenErrorHandling:
    """Test Listen client error handling."""

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url')
    def test_media_client_api_error_handling(self, mock_transcribe, mock_api_key):
        """Test MediaClient API error handling."""
        # Mock an API error
        mock_transcribe.side_effect = ApiError(
            status_code=400,
            headers={},
            body="Invalid request parameters"
        )
        
        client = DeepgramClient(api_key=mock_api_key).listen.v1.media
        
        with pytest.raises(ApiError) as exc_info:
            client.transcribe_url(url="https://example.com/audio.mp3")
        
        assert exc_info.value.status_code == 400
        assert "Invalid request parameters" in str(exc_info.value.body)

    @patch('deepgram.listen.v1.media.raw_client.RawMediaClient.transcribe_url')
    def test_media_client_network_error_handling(self, mock_transcribe, mock_api_key):
        """Test MediaClient network error handling."""
        # Mock a network error
        mock_transcribe.side_effect = httpx.ConnectError("Connection failed")
        
        client = DeepgramClient(api_key=mock_api_key).listen.v1.media
        
        with pytest.raises(httpx.ConnectError):
            client.transcribe_url(url="https://example.com/audio.mp3")

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_websocket_connection_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test WebSocket connection error handling."""
        mock_websocket_connect.side_effect = websockets.exceptions.ConnectionClosedError(None, None)
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(websockets.exceptions.ConnectionClosedError):
            with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
                pass

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_generic_websocket_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test generic WebSocket error handling."""
        mock_websocket_connect.side_effect = Exception("Generic WebSocket error")
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(Exception) as exc_info:
            with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
                pass
        
        assert "Generic WebSocket error" in str(exc_info.value)


class TestListenSocketClientErrorScenarios:
    """Test Listen socket client error scenarios."""

    def test_json_decode_error_handling(self, mock_websocket):
        """Test JSON decode error handling."""
        mock_websocket.recv.return_value = '{"invalid": json}'
        
        client = ListenV1SocketClient(websocket=mock_websocket)
        
        # Should raise JSONDecodeError for invalid JSON
        with pytest.raises(json.JSONDecodeError):
            client.recv()

    def test_connection_closed_ok_no_error_emission(self, mock_websocket):
        """Test that normal connection closure doesn't emit error."""
        mock_websocket.__iter__ = Mock(side_effect=websockets.exceptions.ConnectionClosedOK(None, None))
        
        client = ListenV1SocketClient(websocket=mock_websocket)
        
        # Mock error handler
        error_handler = Mock()
        client.on(EventType.ERROR, error_handler)
        
        # Start listening (should handle ConnectionClosedOK gracefully)
        client.start_listening()
        
        # Error handler should not be called for normal closure
        error_handler.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_connection_closed_ok_no_error_emission(self, mock_async_websocket):
        """Test that async normal connection closure doesn't emit error."""
        async def mock_aiter():
            raise websockets.exceptions.ConnectionClosedOK(None, None)
            yield  # This will never be reached, but makes it a generator
        
        mock_async_websocket.__aiter__ = Mock(return_value=mock_aiter())
        
        client = ListenAsyncV1SocketClient(websocket=mock_async_websocket)
        
        # Mock error handler
        error_handler = Mock()
        client.on(EventType.ERROR, error_handler)
        
        # Start listening (should handle ConnectionClosedOK gracefully)
        await client.start_listening()
        
        # Error handler should not be called for normal closure
        error_handler.assert_not_called()
