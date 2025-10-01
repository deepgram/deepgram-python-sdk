"""End-to-end integration test scenarios across multiple products."""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json
import asyncio

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.events import EventType


class TestMultiProductIntegrationScenarios:
    """Test integration scenarios that span multiple Deepgram products."""

    @patch('deepgram.listen.v1.socket_client.V1SocketClient._handle_json_message')
    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_listen_to_speak_workflow(self, mock_websocket_connect, mock_handle_json, mock_api_key, sample_audio_data, sample_text):
        """Test workflow from Listen transcription to Speak TTS."""
        # Mock Listen websocket connection
        mock_listen_ws = Mock()
        mock_listen_ws.send = Mock()
        mock_listen_ws.recv = Mock(side_effect=[
            '{"type": "Results", "channel": {"alternatives": [{"transcript": "Hello world"}]}}'
        ])
        mock_listen_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Results", "channel": {"alternatives": [{"transcript": "Hello world"}]}}'
        ]))
        mock_listen_ws.__enter__ = Mock(return_value=mock_listen_ws)
        mock_listen_ws.__exit__ = Mock(return_value=None)
        
        # Mock Speak websocket connection
        mock_speak_ws = Mock()
        mock_speak_ws.send = Mock()
        mock_speak_ws.recv = Mock(side_effect=[b'\x00\x01\x02\x03'])  # Audio chunk
        mock_speak_ws.__iter__ = Mock(return_value=iter([b'\x00\x01\x02\x03']))
        mock_speak_ws.__enter__ = Mock(return_value=mock_speak_ws)
        mock_speak_ws.__exit__ = Mock(return_value=None)
        
        # Alternate between Listen and Speak connections
        mock_websocket_connect.side_effect = [mock_listen_ws, mock_speak_ws]
        
        # Mock the JSON message handler to return simple objects
        mock_handle_json.return_value = {"type": "Results", "channel": {"alternatives": [{"transcript": "Hello world"}]}}
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Step 1: Transcribe audio with Listen
        with client.listen.v1.with_raw_response.connect(model="nova-2-general") as listen_conn:
            listen_conn.send_media(sample_audio_data)
            transcription_result = listen_conn.recv()
            assert transcription_result is not None
        
        # Step 2: Generate speech from transcription with Speak
        with client.speak.v1.with_raw_response.connect(model="aura-asteria-en") as speak_conn:
            speak_conn.send_text(Mock())  # Would use transcription text
            audio_result = speak_conn.recv()
            assert audio_result is not None
        
        # Verify both connections were established
        assert mock_websocket_connect.call_count == 2

    @patch('deepgram.listen.v1.raw_client.websockets_sync_client.connect')
    def test_agent_with_listen_speak_integration(self, mock_websocket_connect, mock_api_key, sample_audio_data):
        """Test Agent integration with Listen and Speak capabilities."""
        # Mock Agent websocket connection
        mock_agent_ws = Mock()
        mock_agent_ws.send = Mock()
        mock_agent_ws.recv = Mock(side_effect=[
            '{"type": "Welcome", "request_id": "agent-123"}',
            '{"type": "ConversationText", "role": "assistant", "content": "How can I help you?"}',
            b'\x00\x01\x02\x03'  # Generated speech audio
        ])
        mock_agent_ws.__iter__ = Mock(return_value=iter([
            '{"type": "Welcome", "request_id": "agent-123"}',
            '{"type": "ConversationText", "role": "assistant", "content": "How can I help you?"}',
            b'\x00\x01\x02\x03'
        ]))
        mock_agent_ws.__enter__ = Mock(return_value=mock_agent_ws)
        mock_agent_ws.__exit__ = Mock(return_value=None)
        mock_websocket_connect.return_value = mock_agent_ws
        
        # Initialize client
        client = DeepgramClient(api_key=mock_api_key)
        
        # Connect to Agent (which internally uses Listen and Speak)
        with client.agent.v1.with_raw_response.connect() as agent_conn:
            # Send initial settings
            agent_conn.send_settings(Mock())
            
            # Send user audio (Listen functionality)
            agent_conn.send_media(sample_audio_data)
            
            # Receive welcome message
            welcome = agent_conn.recv()
            assert welcome is not None
            
            # Receive conversation response
            response = agent_conn.recv()
            assert response is not None
            
            # Receive generated audio (Speak functionality)
            audio = agent_conn.recv()
            assert audio is not None
        
        # Verify connection was established
        mock_websocket_connect.assert_called_once()

    def test_multi_client_concurrent_usage(self, mock_api_key):
        """Test concurrent usage of multiple product clients."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Access multiple product clients concurrently
        listen_client = client.listen
        speak_client = client.speak
        agent_client = client.agent
        auth_client = client.auth
        manage_client = client.manage
        read_client = client.read
        self_hosted_client = client.self_hosted
        
        # Verify all clients are properly initialized
        assert listen_client is not None
        assert speak_client is not None
        assert agent_client is not None
        assert auth_client is not None
        assert manage_client is not None
        assert read_client is not None
        assert self_hosted_client is not None
        
        # Verify they're all different instances
        clients = [listen_client, speak_client, agent_client, auth_client, 
                  manage_client, read_client, self_hosted_client]
        for i, client1 in enumerate(clients):
            for j, client2 in enumerate(clients):
                if i != j:
                    assert client1 is not client2

    @pytest.mark.asyncio
    async def test_async_multi_product_workflow(self, mock_api_key):
        """Test async workflow across multiple products."""
        with patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant') as mock_grant, \
             patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze') as mock_analyze:
            
            # Mock auth token generation
            from deepgram.types.grant_v1response import GrantV1Response
            mock_auth_response = Mock()
            mock_auth_response.data = GrantV1Response(access_token="temp_token", expires_in=3600)
            mock_grant.return_value = mock_auth_response
            
            # Mock text analysis
            from deepgram.types.read_v1response import ReadV1Response
            from deepgram.types.read_v1response_metadata import ReadV1ResponseMetadata
            from deepgram.types.read_v1response_results import ReadV1ResponseResults
            mock_read_response = Mock()
            mock_read_response.data = ReadV1Response(
                metadata=ReadV1ResponseMetadata(),
                results=ReadV1ResponseResults()
            )
            mock_analyze.return_value = mock_read_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Step 1: Generate temporary token
            token_result = await client.auth.v1.tokens.grant(ttl_seconds=3600)
            assert token_result is not None
            assert isinstance(token_result, GrantV1Response)
            
            # Step 2: Analyze text
            from deepgram.requests.read_v1request_text import ReadV1RequestTextParams
            text_request = ReadV1RequestTextParams(text="Sample text for analysis")
            analysis_result = await client.read.v1.text.analyze(
                request=text_request,
                sentiment=True,
                topics=True
            )
            assert analysis_result is not None
            assert isinstance(analysis_result, ReadV1Response)
            
            # Verify both calls were made
            mock_grant.assert_called_once()
            mock_analyze.assert_called_once()

    def test_client_isolation_across_products(self, mock_api_key):
        """Test that product clients maintain proper isolation."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        # Verify top-level product clients are isolated
        assert client1.listen is not client2.listen
        assert client1.speak is not client2.speak
        assert client1.agent is not client2.agent
        assert client1.auth is not client2.auth
        assert client1.manage is not client2.manage
        assert client1.read is not client2.read
        assert client1.self_hosted is not client2.self_hosted
        
        # Verify nested clients are also isolated
        assert client1.listen.v1 is not client2.listen.v1
        assert client1.speak.v1 is not client2.speak.v1
        assert client1.agent.v1 is not client2.agent.v1
        assert client1.auth.v1 is not client2.auth.v1
        assert client1.manage.v1 is not client2.manage.v1
        assert client1.read.v1 is not client2.read.v1
        assert client1.self_hosted.v1 is not client2.self_hosted.v1

    @pytest.mark.asyncio
    async def test_mixed_sync_async_multi_product(self, mock_api_key):
        """Test mixing synchronous and asynchronous clients across products."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Verify sync and async clients are different types
        assert type(sync_client.listen) != type(async_client.listen)
        assert type(sync_client.speak) != type(async_client.speak)
        assert type(sync_client.agent) != type(async_client.agent)
        assert type(sync_client.auth) != type(async_client.auth)
        assert type(sync_client.manage) != type(async_client.manage)
        assert type(sync_client.read) != type(async_client.read)
        assert type(sync_client.self_hosted) != type(async_client.self_hosted)
        
        # Verify nested clients are also different types
        assert type(sync_client.listen.v1) != type(async_client.listen.v1)
        assert type(sync_client.speak.v1) != type(async_client.speak.v1)
        assert type(sync_client.agent.v1) != type(async_client.agent.v1)
        assert type(sync_client.auth.v1) != type(async_client.auth.v1)
        assert type(sync_client.manage.v1) != type(async_client.manage.v1)
        assert type(sync_client.read.v1) != type(async_client.read.v1)
        assert type(sync_client.self_hosted.v1) != type(async_client.self_hosted.v1)


class TestErrorHandlingScenarios:
    """Test error handling across integration scenarios."""

    def test_connection_failure_handling(self, mock_api_key):
        """Test connection failure handling."""
        with patch('websockets.sync.client.connect') as mock_connect:
            mock_connect.side_effect = ConnectionError("Network unavailable")
            
            client = DeepgramClient(api_key=mock_api_key)
            
            # Test that connection failures are properly handled across products
            with pytest.raises(ConnectionError):
                with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
                    pass
            
            with pytest.raises(ConnectionError):
                with client.speak.v1.with_raw_response.connect() as connection:
                    pass
            
            with pytest.raises(ConnectionError):
                with client.agent.v1.with_raw_response.connect() as connection:
                    pass

    def test_message_processing_error_handling(self, mock_api_key):
        """Test message processing error handling."""
        with patch('websockets.sync.client.connect') as mock_connect:
            # Mock websocket that sends invalid JSON
            mock_ws = Mock()
            mock_ws.send = Mock()
            mock_ws.recv = Mock(side_effect=['{"invalid": json}'])
            mock_ws.__iter__ = Mock(return_value=iter(['{"invalid": json}']))
            mock_ws.__enter__ = Mock(return_value=mock_ws)
            mock_ws.__exit__ = Mock(return_value=None)
            mock_connect.return_value = mock_ws
            
            client = DeepgramClient(api_key=mock_api_key)
            
            # Test that invalid JSON raises JSONDecodeError
            with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
                with pytest.raises(json.JSONDecodeError):
                    connection.recv()

    @pytest.mark.asyncio
    async def test_async_connection_failure_handling(self, mock_api_key):
        """Test async connection failure handling."""
        with patch('deepgram.listen.v1.raw_client.websockets_client_connect') as mock_connect:
            mock_connect.side_effect = ConnectionError("Async network unavailable")
            
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Test that async connection failures are properly handled
            with pytest.raises(ConnectionError):
                async with client.listen.v1.with_raw_response.connect(model="nova-2-general") as connection:
                    pass