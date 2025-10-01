"""Integration tests for Speak client implementations."""

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

# Import Speak clients
from deepgram.speak.client import SpeakClient, AsyncSpeakClient
from deepgram.speak.v1.client import V1Client as SpeakV1Client, AsyncV1Client as SpeakAsyncV1Client

# Import Speak raw clients
from deepgram.speak.v1.raw_client import RawV1Client as SpeakRawV1Client, AsyncRawV1Client as SpeakAsyncRawV1Client

# Import Speak socket clients
from deepgram.speak.v1.socket_client import V1SocketClient as SpeakV1SocketClient, AsyncV1SocketClient as SpeakAsyncV1SocketClient

# Import Speak audio clients
from deepgram.speak.v1.audio.client import AudioClient, AsyncAudioClient

# Import socket message types
from deepgram.extensions.types.sockets import (
    SpeakV1TextMessage,
    SpeakV1ControlMessage,
)

# Import request and response types for mocking
from deepgram.speak.v1.audio.types.audio_generate_request_callback_method import AudioGenerateRequestCallbackMethod
from deepgram.speak.v1.audio.types.audio_generate_request_container import AudioGenerateRequestContainer
from deepgram.speak.v1.audio.types.audio_generate_request_encoding import AudioGenerateRequestEncoding
from deepgram.speak.v1.audio.types.audio_generate_request_model import AudioGenerateRequestModel


class TestSpeakClient:
    """Test cases for Speak Client."""

    def test_speak_client_initialization(self, mock_api_key):
        """Test SpeakClient initialization."""
        client = DeepgramClient(api_key=mock_api_key).speak
        assert client is not None
        assert hasattr(client, 'v1')

    def test_async_speak_client_initialization(self, mock_api_key):
        """Test AsyncSpeakClient initialization."""
        client = AsyncDeepgramClient(api_key=mock_api_key).speak
        assert client is not None
        assert hasattr(client, 'v1')

    def test_speak_client_with_raw_response(self, mock_api_key):
        """Test SpeakClient with_raw_response property."""
        client = DeepgramClient(api_key=mock_api_key).speak
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')

    def test_async_speak_client_with_raw_response(self, mock_api_key):
        """Test AsyncSpeakClient with_raw_response property."""
        client = AsyncDeepgramClient(api_key=mock_api_key).speak
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert hasattr(raw_client, '_client_wrapper')


class TestSpeakRawV1Client:
    """Test cases for Speak V1 Raw Client."""

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

    def test_sync_speak_raw_client_initialization(self, sync_client_wrapper):
        """Test synchronous speak raw client initialization."""
        client = SpeakRawV1Client(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper

    def test_async_speak_raw_client_initialization(self, async_client_wrapper):
        """Test asynchronous speak raw client initialization."""
        client = SpeakAsyncRawV1Client(client_wrapper=async_client_wrapper)
        assert client is not None
        assert client._client_wrapper is async_client_wrapper

    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_sync_speak_connect_success(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test successful synchronous Speak WebSocket connection."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = SpeakRawV1Client(client_wrapper=sync_client_wrapper)
        
        with client.connect() as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_sync_speak_connect_with_parameters(self, mock_websocket_connect, sync_client_wrapper, mock_websocket):
        """Test synchronous Speak connection with parameters."""
        mock_websocket_connect.return_value.__enter__ = Mock(return_value=mock_websocket)
        mock_websocket_connect.return_value.__exit__ = Mock(return_value=None)
        
        client = SpeakRawV1Client(client_wrapper=sync_client_wrapper)
        
        with client.connect(
            model="aura-asteria-en",
            encoding="linear16",
            sample_rate="24000"
        ) as connection:
            assert connection is not None

    @patch('deepgram.speak.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_speak_connect_success(self, mock_websocket_connect, async_client_wrapper, mock_async_websocket):
        """Test successful asynchronous Speak WebSocket connection."""
        mock_websocket_connect.return_value.__aenter__ = AsyncMock(return_value=mock_async_websocket)
        mock_websocket_connect.return_value.__aexit__ = AsyncMock(return_value=None)
        
        client = SpeakAsyncRawV1Client(client_wrapper=async_client_wrapper)
        
        async with client.connect() as connection:
            assert connection is not None
            assert hasattr(connection, '_websocket')

    def test_speak_query_params_construction(self, sync_client_wrapper):
        """Test Speak query parameters are properly constructed."""
        client = SpeakRawV1Client(client_wrapper=sync_client_wrapper)
        
        # Mock the websocket connection to capture the URL
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.return_value.__enter__ = Mock(return_value=Mock())
            mock_connect.return_value.__exit__ = Mock(return_value=None)
            
            try:
                with client.connect(
                    model="aura-asteria-en",
                    encoding="linear16",
                    sample_rate="24000"
                ) as connection:
                    pass
            except:
                pass  # We just want to check the URL construction
            
            # Verify the URL was constructed with query parameters
            call_args = mock_connect.call_args
            if call_args and len(call_args[0]) > 0:
                url = call_args[0][0]
                assert "model=aura-asteria-en" in url
                assert "encoding=linear16" in url
                assert "sample_rate=24000" in url


class TestSpeakV1SocketClient:
    """Test cases for Speak V1 Socket Client."""

    def test_speak_sync_socket_client_initialization(self):
        """Test Speak synchronous socket client initialization."""
        mock_ws = Mock()
        client = SpeakV1SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_speak_async_socket_client_initialization(self):
        """Test Speak asynchronous socket client initialization."""
        mock_ws = AsyncMock()
        client = SpeakAsyncV1SocketClient(websocket=mock_ws)
        
        assert client is not None
        assert client._websocket is mock_ws

    def test_speak_sync_send_text(self):
        """Test Speak synchronous text message sending."""
        mock_ws = Mock()
        client = SpeakV1SocketClient(websocket=mock_ws)
        
        # Mock text message
        mock_text_msg = Mock(spec=SpeakV1TextMessage)
        mock_text_msg.dict.return_value = {"type": "Speak", "text": "Hello world"}
        
        client.send_text(mock_text_msg)
        
        mock_text_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    def test_speak_sync_send_control(self):
        """Test Speak synchronous control message sending."""
        mock_ws = Mock()
        client = SpeakV1SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=SpeakV1ControlMessage)
        mock_control_msg.dict.return_value = {"type": "Flush"}
        
        client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_speak_async_send_text(self):
        """Test Speak asynchronous text message sending."""
        mock_ws = AsyncMock()
        client = SpeakAsyncV1SocketClient(websocket=mock_ws)
        
        # Mock text message
        mock_text_msg = Mock(spec=SpeakV1TextMessage)
        mock_text_msg.dict.return_value = {"type": "Speak", "text": "Hello world"}
        
        await client.send_text(mock_text_msg)
        
        mock_text_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_speak_async_send_control(self):
        """Test Speak asynchronous control message sending."""
        mock_ws = AsyncMock()
        client = SpeakAsyncV1SocketClient(websocket=mock_ws)
        
        # Mock control message
        mock_control_msg = Mock(spec=SpeakV1ControlMessage)
        mock_control_msg.dict.return_value = {"type": "Flush"}
        
        await client.send_control(mock_control_msg)
        
        mock_control_msg.dict.assert_called_once()
        mock_ws.send.assert_called_once()


class TestSpeakAudioClient:
    """Test cases for Speak Audio Client."""

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
    def sample_audio_chunks(self):
        """Sample audio chunks for testing."""
        return [
            b'\x00\x01\x02\x03\x04\x05',
            b'\x06\x07\x08\x09\x0a\x0b',
            b'\x0c\x0d\x0e\x0f\x10\x11'
        ]

    def test_audio_client_initialization(self, sync_client_wrapper):
        """Test AudioClient initialization."""
        client = AudioClient(client_wrapper=sync_client_wrapper)
        assert client is not None
        assert client._raw_client is not None

    def test_async_audio_client_initialization(self, async_client_wrapper):
        """Test AsyncAudioClient initialization."""
        client = AsyncAudioClient(client_wrapper=async_client_wrapper)
        assert client is not None
        assert client._raw_client is not None

    def test_audio_client_raw_response_access(self, sync_client_wrapper):
        """Test AudioClient raw response access."""
        client = AudioClient(client_wrapper=sync_client_wrapper)
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_audio_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncAudioClient raw response access."""
        client = AsyncAudioClient(client_wrapper=async_client_wrapper)
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.speak.v1.audio.raw_client.RawAudioClient.generate')
    def test_audio_client_generate(self, mock_generate, sync_client_wrapper, sample_audio_chunks):
        """Test AudioClient generate method."""
        # Mock the raw client response with context manager
        mock_response = Mock()
        mock_data_response = Mock()
        mock_data_response.data = iter(sample_audio_chunks)
        mock_response.__enter__ = Mock(return_value=mock_data_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_generate.return_value = mock_response

        client = AudioClient(client_wrapper=sync_client_wrapper)

        response = client.generate(
            text="Hello, world!",
            model="aura-asteria-en"
        )
        audio_chunks = list(response)
        assert len(audio_chunks) == 3
        assert audio_chunks[0] == sample_audio_chunks[0]

        # Verify the call was made
        mock_generate.assert_called_once()

    @patch('deepgram.speak.v1.audio.raw_client.RawAudioClient.generate')
    def test_audio_client_generate_with_all_options(self, mock_generate, sync_client_wrapper, sample_audio_chunks):
        """Test AudioClient generate with all options."""
        # Mock the raw client response with context manager
        mock_response = Mock()
        mock_data_response = Mock()
        mock_data_response.data = iter(sample_audio_chunks)
        mock_response.__enter__ = Mock(return_value=mock_data_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_generate.return_value = mock_response
        
        client = AudioClient(client_wrapper=sync_client_wrapper)
        
        response = client.generate(
            text="Hello, world!",
            model="aura-asteria-en",
            encoding="linear16",
            container="wav",
            sample_rate=22050,
            callback="https://example.com/callback",
            callback_method="POST"
        )
        audio_chunks = list(response)
        assert len(audio_chunks) == 3

        # Verify the call was made with all parameters
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        assert "model" in call_args[1]
        assert "encoding" in call_args[1]
        assert "sample_rate" in call_args[1]

    @patch('deepgram.speak.v1.audio.raw_client.AsyncRawAudioClient.generate')
    @pytest.mark.asyncio
    async def test_async_audio_client_generate(self, mock_generate, async_client_wrapper, sample_audio_chunks):
        """Test AsyncAudioClient generate method."""
        # Mock the async raw client response with context manager
        mock_response = AsyncMock()
        mock_data_response = AsyncMock()
        
        async def mock_aiter_data():
            for chunk in sample_audio_chunks:
                yield chunk
        
        mock_data_response.data = mock_aiter_data()
        mock_response.__aenter__ = AsyncMock(return_value=mock_data_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        mock_generate.return_value = mock_response

        client = AsyncAudioClient(client_wrapper=async_client_wrapper)

        response = client.generate(
            text="Hello, world!",
            model="aura-asteria-en"
        )
        audio_chunks = []
        async for chunk in response:
            audio_chunks.append(chunk)
            
        assert len(audio_chunks) == 3
        assert audio_chunks[0] == sample_audio_chunks[0]

        # Verify the call was made
        mock_generate.assert_called_once()

    @patch('deepgram.speak.v1.audio.raw_client.AsyncRawAudioClient.generate')
    @pytest.mark.asyncio
    async def test_async_audio_client_generate_with_options(self, mock_generate, async_client_wrapper, sample_audio_chunks):
        """Test AsyncAudioClient generate with options."""
        # Mock the async raw client response with context manager
        mock_response = AsyncMock()
        mock_data_response = AsyncMock()
        
        async def mock_aiter_data():
            for chunk in sample_audio_chunks:
                yield chunk
        
        mock_data_response.data = mock_aiter_data()
        mock_response.__aenter__ = AsyncMock(return_value=mock_data_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        mock_generate.return_value = mock_response
        
        client = AsyncAudioClient(client_wrapper=async_client_wrapper)
        
        response = client.generate(
            text="Hello, world!",
            model="aura-asteria-en",
            encoding="linear16",
            sample_rate=22050
        )
        audio_chunks = []
        async for chunk in response:
            audio_chunks.append(chunk)
            
        assert len(audio_chunks) == 3

        # Verify the call was made
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args

        assert call_args[1]["sample_rate"] == 22050


class TestSpeakIntegrationScenarios:
    """Test Speak API integration scenarios."""

    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_speak_tts_workflow(self, mock_websocket_connect, mock_api_key, sample_text):
        """Test complete Speak TTS workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.recv = Mock(side_effect=[
            b'\x00\x01\x02\x03',  # Audio chunk
            '{"type": "Metadata", "request_id": "speak-123", "model_name": "aura-asteria-en", "model_version": "1.0", "model_uuid": "uuid-123"}'
        ])
        mock_ws.__iter__ = Mock(return_value=iter([
            b'\x00\x01\x02\x03',  # Audio chunk
            '{"type": "Metadata", "request_id": "speak-123", "model_name": "aura-asteria-en", "model_version": "1.0", "model_uuid": "uuid-123"}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect and send text
        with client.speak.v1.with_raw_response.connect() as connection:
            # Send text message
            connection.send_text(Mock())
            
            # Send control message
            connection.send_control(Mock())
            
            # Receive audio data
            result = connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    @patch('deepgram.speak.v1.socket_client.V1SocketClient._handle_json_message')
    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_speak_event_driven_workflow(self, mock_websocket_connect, mock_handle_json, mock_api_key):
        """Test Speak event-driven workflow."""
        # Mock websocket connection
        mock_ws = Mock()
        mock_ws.send = Mock()
        mock_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Metadata", "request_id": "speak-event-123"}'
        ]))
        mock_ws.__enter__ = Mock(return_value=mock_ws)
        mock_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.return_value = {"type": "Metadata", "request_id": "speak-event-123"}
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Mock event handlers
        on_open = Mock()
        on_message = Mock()
        on_close = Mock()
        on_error = Mock()
        
        # Connect with event handlers
        with client.speak.v1.with_raw_response.connect() as connection:
            # Set up event handlers
            connection.on(EventType.OPEN, on_open)
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.CLOSE, on_close)
            connection.on(EventType.ERROR, on_error)
            
            # Start listening (this will process the mock messages)
            connection.start_listening()
        
        # Verify event handlers were set up
        assert hasattr(connection, 'on')

    @patch('deepgram.speak.v1.raw_client.websockets_client_connect')
    @pytest.mark.asyncio
    async def test_async_speak_tts_workflow(self, mock_websocket_connect, mock_api_key):
        """Test async Speak TTS workflow."""
        # Mock async websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=[
            b'\x00\x01\x02\x03',  # Audio chunk
            '{"type": "Metadata", "request_id": "async-speak-123"}'
        ])
        
        async def mock_aiter():
            yield b'\x00\x01\x02\x03'  # Audio chunk
            yield '{"type": "Metadata", "request_id": "async-speak-123"}'
        
        mock_ws.__aiter__ = Mock(return_value=mock_aiter())
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)
        mock_websocket_connect.return_value = mock_ws
        
        # Initialize async client
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Connect and send text
        async with client.speak.v1.with_raw_response.connect() as connection:
            # Send text message
            await connection.send_text(Mock())
            
            # Send control message
            await connection.send_control(Mock())
            
            # Receive audio data
            result = await connection.recv()
            assert result is not None
        
        # Verify websocket operations
        mock_ws.send.assert_called()

    def test_complete_speak_audio_workflow_sync(self, mock_api_key):
        """Test complete Speak Audio workflow using sync client."""
        with patch('deepgram.speak.v1.audio.raw_client.RawAudioClient.generate') as mock_generate:
            # Mock the response with context manager
            mock_response = Mock()
            mock_data_response = Mock()
            mock_data_response.data = iter([
                b'\x00\x01\x02\x03',
                b'\x04\x05\x06\x07',
                b'\x08\x09\x0a\x0b'
            ])
            mock_response.__enter__ = Mock(return_value=mock_data_response)
            mock_response.__exit__ = Mock(return_value=None)
            mock_generate.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested speak audio functionality
            response = client.speak.v1.audio.generate(
                text="Hello, this is a test of the Deepgram TTS API.",
                model="aura-asteria-en",
                encoding="linear16",
                sample_rate=24000
            )
            audio_chunks = list(response)
            assert len(audio_chunks) == 3
            assert audio_chunks[0] == b'\x00\x01\x02\x03'
            
            # Verify the call was made
            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_speak_audio_workflow_async(self, mock_api_key):
        """Test complete Speak Audio workflow using async client."""
        with patch('deepgram.speak.v1.audio.raw_client.AsyncRawAudioClient.generate') as mock_generate:
            # Mock the async response with context manager
            mock_response = AsyncMock()
            mock_data_response = AsyncMock()
            
            async def mock_aiter_data():
                yield b'\x00\x01\x02\x03'
                yield b'\x04\x05\x06\x07'
                yield b'\x08\x09\x0a\x0b'
            
            mock_data_response.data = mock_aiter_data()
            mock_response.__aenter__ = AsyncMock(return_value=mock_data_response)
            mock_response.__aexit__ = AsyncMock(return_value=None)
            mock_generate.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested speak audio functionality
            response = client.speak.v1.audio.generate(
                text="Hello, this is an async test of the Deepgram TTS API.",
                model="aura-asteria-en",
                encoding="linear16"
            )
            audio_chunks = []
            async for chunk in response:
                audio_chunks.append(chunk)
            
            assert len(audio_chunks) == 3
            assert audio_chunks[0] == b'\x00\x01\x02\x03'
            
            # Verify the call was made
            mock_generate.assert_called_once()

    def test_speak_client_property_isolation(self, mock_api_key):
        """Test that speak clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        # Verify clients are different instances
        assert client1.speak is not client2.speak
        
        # Verify nested clients are also different
        speak1 = client1.speak.v1
        speak2 = client2.speak.v1
        
        assert speak1 is not speak2

    @pytest.mark.asyncio
    async def test_mixed_sync_async_speak_clients(self, mock_api_key):
        """Test mixing sync and async speak clients."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Verify clients are different types
        assert type(sync_client.speak) != type(async_client.speak)
        
        # Verify nested clients are also different types
        sync_speak = sync_client.speak.v1
        async_speak = async_client.speak.v1
        
        assert type(sync_speak) != type(async_speak)
        assert isinstance(sync_speak, SpeakV1Client)
        assert isinstance(async_speak, SpeakAsyncV1Client)


class TestSpeakErrorHandling:
    """Test Speak client error handling."""

    @patch('deepgram.speak.v1.audio.raw_client.RawAudioClient.generate')
    def test_audio_client_api_error_handling(self, mock_generate, mock_api_key):
        """Test AudioClient API error handling."""
        # Mock an API error
        mock_generate.side_effect = ApiError(
            status_code=400,
            headers={},
            body="Invalid request parameters"
        )
        
        client = DeepgramClient(api_key=mock_api_key).speak.v1.audio
        
        with pytest.raises(ApiError) as exc_info:
            response = client.generate(text="Hello world")
            list(response)
        
        assert exc_info.value.status_code == 400
        assert "Invalid request parameters" in str(exc_info.value.body)

    @patch('deepgram.speak.v1.audio.raw_client.AsyncRawAudioClient.generate')
    @pytest.mark.asyncio
    async def test_async_audio_client_api_error_handling(self, mock_generate, mock_api_key):
        """Test AsyncAudioClient API error handling."""
        # Mock an API error
        mock_generate.side_effect = ApiError(
            status_code=429,
            headers={},
            body="Rate limit exceeded"
        )
        
        client = AsyncDeepgramClient(api_key=mock_api_key).speak.v1.audio
        
        with pytest.raises(ApiError) as exc_info:
            response = client.generate(text="Hello world")
            async for chunk in response:
                pass
        
        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in str(exc_info.value.body)

    @patch('deepgram.speak.v1.audio.raw_client.RawAudioClient.generate')
    def test_audio_client_network_error_handling(self, mock_generate, mock_api_key):
        """Test AudioClient network error handling."""
        # Mock a network error
        mock_generate.side_effect = httpx.ConnectError("Connection failed")
        
        client = DeepgramClient(api_key=mock_api_key).speak.v1.audio
        
        with pytest.raises(httpx.ConnectError):
            response = client.generate(text="Hello world")
            list(response)

    @patch('deepgram.speak.v1.audio.raw_client.AsyncRawAudioClient.generate')
    @pytest.mark.asyncio
    async def test_async_audio_client_network_error_handling(self, mock_generate, mock_api_key):
        """Test AsyncAudioClient network error handling."""
        # Mock a network error
        mock_generate.side_effect = httpx.ConnectError("Async connection failed")
        
        client = AsyncDeepgramClient(api_key=mock_api_key).speak.v1.audio
        
        with pytest.raises(httpx.ConnectError):
            response = client.generate(text="Hello world")
            async for chunk in response:
                pass

    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_websocket_connection_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test WebSocket connection error handling."""
        mock_websocket_connect.side_effect = websockets.exceptions.ConnectionClosedError(None, None)
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(websockets.exceptions.ConnectionClosedError):
            with client.speak.v1.with_raw_response.connect() as connection:
                pass

    @patch('deepgram.speak.v1.raw_client.websockets_sync_client.connect')
    def test_generic_websocket_error_handling(self, mock_websocket_connect, mock_api_key):
        """Test generic WebSocket error handling."""
        mock_websocket_connect.side_effect = Exception("Generic WebSocket error")
        
        client = DeepgramClient(api_key=mock_api_key)
        
        with pytest.raises(Exception) as exc_info:
            with client.speak.v1.with_raw_response.connect() as connection:
                pass
        
        assert "Generic WebSocket error" in str(exc_info.value)

    def test_client_wrapper_integration(self, mock_api_key):
        """Test integration with client wrapper."""
        client = DeepgramClient(api_key=mock_api_key).speak.v1.audio
        assert client._raw_client is not None
        assert client._raw_client._client_wrapper.api_key == mock_api_key
