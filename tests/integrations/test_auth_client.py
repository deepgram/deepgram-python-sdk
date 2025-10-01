"""Integration tests for Auth client implementations."""

import pytest
import httpx
from unittest.mock import Mock, AsyncMock, patch

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.environment import DeepgramClientEnvironment
from deepgram.types.grant_v1response import GrantV1Response

from deepgram.auth.client import AuthClient, AsyncAuthClient
from deepgram.auth.v1.client import V1Client as AuthV1Client, AsyncV1Client as AuthAsyncV1Client
from deepgram.auth.v1.tokens.client import TokensClient, AsyncTokensClient


class TestAuthClient:
    """Test cases for Auth Client."""

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

    def test_auth_client_initialization(self, sync_client_wrapper):
        """Test AuthClient initialization."""
        client = AuthClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_async_auth_client_initialization(self, async_client_wrapper):
        """Test AsyncAuthClient initialization."""
        client = AsyncAuthClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_auth_client_v1_property_lazy_loading(self, sync_client_wrapper):
        """Test AuthClient v1 property lazy loading."""
        client = AuthClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, AuthV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_async_auth_client_v1_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncAuthClient v1 property lazy loading."""
        client = AsyncAuthClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, AuthAsyncV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_auth_client_raw_response_access(self, sync_client_wrapper):
        """Test AuthClient raw response access."""
        client = AuthClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_auth_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncAuthClient raw response access."""
        client = AsyncAuthClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_auth_client_integration_with_main_client(self, mock_api_key):
        """Test AuthClient integration with main DeepgramClient."""
        client = DeepgramClient(api_key=mock_api_key)
        
        auth_client = client.auth
        assert auth_client is not None
        assert isinstance(auth_client, AuthClient)

    def test_async_auth_client_integration_with_main_client(self, mock_api_key):
        """Test AsyncAuthClient integration with main AsyncDeepgramClient."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        auth_client = client.auth
        assert auth_client is not None
        assert isinstance(auth_client, AsyncAuthClient)


class TestAuthV1Client:
    """Test cases for Auth V1 Client."""

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

    def test_auth_v1_client_initialization(self, sync_client_wrapper):
        """Test AuthV1Client initialization."""
        client = AuthV1Client(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._tokens is None  # Lazy loaded

    def test_async_auth_v1_client_initialization(self, async_client_wrapper):
        """Test AsyncAuthV1Client initialization."""
        client = AuthAsyncV1Client(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._tokens is None  # Lazy loaded

    def test_auth_v1_client_tokens_property_lazy_loading(self, sync_client_wrapper):
        """Test AuthV1Client tokens property lazy loading."""
        client = AuthV1Client(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._tokens is None
        
        # Access triggers lazy loading
        tokens_client = client.tokens
        assert client._tokens is not None
        assert isinstance(tokens_client, TokensClient)
        
        # Subsequent access returns same instance
        assert client.tokens is tokens_client

    def test_async_auth_v1_client_tokens_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncAuthV1Client tokens property lazy loading."""
        client = AuthAsyncV1Client(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._tokens is None
        
        # Access triggers lazy loading
        tokens_client = client.tokens
        assert client._tokens is not None
        assert isinstance(tokens_client, AsyncTokensClient)
        
        # Subsequent access returns same instance
        assert client.tokens is tokens_client

    def test_auth_v1_client_raw_response_access(self, sync_client_wrapper):
        """Test AuthV1Client raw response access."""
        client = AuthV1Client(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_auth_v1_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncAuthV1Client raw response access."""
        client = AuthAsyncV1Client(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client


class TestTokensClient:
    """Test cases for Tokens Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        mock_httpx_client = Mock(spec=httpx.Client)
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
        mock_httpx_client = AsyncMock(spec=httpx.AsyncClient)
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def mock_grant_response(self):
        """Mock grant response data."""
        return {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "expires_in": 30
        }

    def test_tokens_client_initialization(self, sync_client_wrapper):
        """Test TokensClient initialization."""
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_async_tokens_client_initialization(self, async_client_wrapper):
        """Test AsyncTokensClient initialization."""
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_tokens_client_raw_response_access(self, sync_client_wrapper):
        """Test TokensClient raw response access."""
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_tokens_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncTokensClient raw response access."""
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant')
    def test_tokens_client_grant_default_ttl(self, mock_grant, sync_client_wrapper, mock_grant_response):
        """Test TokensClient grant with default TTL."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        result = client.grant()
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        assert result.access_token == mock_grant_response["access_token"]
        assert result.expires_in == mock_grant_response["expires_in"]
        
        # Verify raw client was called with correct parameters
        mock_grant.assert_called_once_with(ttl_seconds=..., request_options=None)

    @patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant')
    def test_tokens_client_grant_custom_ttl(self, mock_grant, sync_client_wrapper, mock_grant_response):
        """Test TokensClient grant with custom TTL."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        custom_ttl = 60
        result = client.grant(ttl_seconds=custom_ttl)
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        
        # Verify raw client was called with custom TTL
        mock_grant.assert_called_once_with(ttl_seconds=custom_ttl, request_options=None)

    @patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant')
    def test_tokens_client_grant_with_request_options(self, mock_grant, sync_client_wrapper, mock_grant_response):
        """Test TokensClient grant with request options."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        request_options = RequestOptions(
            additional_headers={"X-Custom-Header": "test-value"}
        )
        result = client.grant(ttl_seconds=45, request_options=request_options)
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        
        # Verify raw client was called with request options
        mock_grant.assert_called_once_with(ttl_seconds=45, request_options=request_options)

    @patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant')
    @pytest.mark.asyncio
    async def test_async_tokens_client_grant_default_ttl(self, mock_grant, async_client_wrapper, mock_grant_response):
        """Test AsyncTokensClient grant with default TTL."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        result = await client.grant()
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        assert result.access_token == mock_grant_response["access_token"]
        assert result.expires_in == mock_grant_response["expires_in"]
        
        # Verify async raw client was called with correct parameters
        mock_grant.assert_called_once_with(ttl_seconds=..., request_options=None)

    @patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant')
    @pytest.mark.asyncio
    async def test_async_tokens_client_grant_custom_ttl(self, mock_grant, async_client_wrapper, mock_grant_response):
        """Test AsyncTokensClient grant with custom TTL."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        custom_ttl = 120
        result = await client.grant(ttl_seconds=custom_ttl)
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        
        # Verify async raw client was called with custom TTL
        mock_grant.assert_called_once_with(ttl_seconds=custom_ttl, request_options=None)

    @patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant')
    @pytest.mark.asyncio
    async def test_async_tokens_client_grant_with_request_options(self, mock_grant, async_client_wrapper, mock_grant_response):
        """Test AsyncTokensClient grant with request options."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = GrantV1Response(**mock_grant_response)
        mock_grant.return_value = mock_response
        
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        request_options = RequestOptions(
            additional_headers={"X-Custom-Header": "async-test-value"}
        )
        result = await client.grant(ttl_seconds=90, request_options=request_options)
        
        assert result is not None
        assert isinstance(result, GrantV1Response)
        
        # Verify async raw client was called with request options
        mock_grant.assert_called_once_with(ttl_seconds=90, request_options=request_options)


class TestAuthIntegrationScenarios:
    """Test Auth integration scenarios."""

    def test_complete_auth_workflow_sync(self, mock_api_key):
        """Test complete Auth workflow using sync client."""
        with patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant') as mock_grant:
            # Mock the response
            mock_response = Mock()
            mock_response.data = GrantV1Response(
                access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                expires_in=30
            )
            mock_grant.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested auth functionality
            result = client.auth.v1.tokens.grant(ttl_seconds=60)
            
            assert result is not None
            assert isinstance(result, GrantV1Response)
            assert result.access_token is not None
            assert result.expires_in == 30
            
            # Verify the call was made
            mock_grant.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_auth_workflow_async(self, mock_api_key):
        """Test complete Auth workflow using async client."""
        with patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant') as mock_grant:
            # Mock the async response
            mock_response = Mock()
            mock_response.data = GrantV1Response(
                access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                expires_in=60
            )
            mock_grant.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested auth functionality
            result = await client.auth.v1.tokens.grant(ttl_seconds=120)
            
            assert result is not None
            assert isinstance(result, GrantV1Response)
            assert result.access_token is not None
            assert result.expires_in == 60
            
            # Verify the call was made
            mock_grant.assert_called_once()

    def test_auth_client_property_isolation(self, mock_api_key):
        """Test that auth clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        auth1 = client1.auth
        auth2 = client2.auth
        
        # Verify they are different instances
        assert auth1 is not auth2
        assert auth1._client_wrapper is not auth2._client_wrapper
        
        # Verify nested clients are also different
        tokens1 = auth1.v1.tokens
        tokens2 = auth2.v1.tokens
        
        assert tokens1 is not tokens2

    @pytest.mark.asyncio
    async def test_mixed_sync_async_auth_clients(self, mock_api_key):
        """Test mixing sync and async auth clients."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        sync_auth = sync_client.auth
        async_auth = async_client.auth
        
        # Verify they are different types
        assert type(sync_auth) != type(async_auth)
        assert isinstance(sync_auth, AuthClient)
        assert isinstance(async_auth, AsyncAuthClient)
        
        # Verify nested clients are also different types
        sync_tokens = sync_auth.v1.tokens
        async_tokens = async_auth.v1.tokens
        
        assert type(sync_tokens) != type(async_tokens)
        assert isinstance(sync_tokens, TokensClient)
        assert isinstance(async_tokens, AsyncTokensClient)


class TestAuthErrorHandling:
    """Test Auth client error handling."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        mock_httpx_client = Mock(spec=httpx.Client)
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
        mock_httpx_client = AsyncMock(spec=httpx.AsyncClient)
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant')
    def test_tokens_client_api_error_handling(self, mock_grant, sync_client_wrapper):
        """Test TokensClient API error handling."""
        # Mock an API error
        mock_grant.side_effect = ApiError(
            status_code=401,
            headers={},
            body="Invalid API key"
        )
        
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            client.grant()
        
        assert exc_info.value.status_code == 401
        assert "Invalid API key" in str(exc_info.value.body)

    @patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant')
    @pytest.mark.asyncio
    async def test_async_tokens_client_api_error_handling(self, mock_grant, async_client_wrapper):
        """Test AsyncTokensClient API error handling."""
        # Mock an API error
        mock_grant.side_effect = ApiError(
            status_code=403,
            headers={},
            body="Insufficient permissions"
        )
        
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            await client.grant()
        
        assert exc_info.value.status_code == 403
        assert "Insufficient permissions" in str(exc_info.value.body)

    @patch('deepgram.auth.v1.tokens.raw_client.RawTokensClient.grant')
    def test_tokens_client_network_error_handling(self, mock_grant, sync_client_wrapper):
        """Test TokensClient network error handling."""
        # Mock a network error
        mock_grant.side_effect = httpx.ConnectError("Connection failed")
        
        client = TokensClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(httpx.ConnectError):
            client.grant()

    @patch('deepgram.auth.v1.tokens.raw_client.AsyncRawTokensClient.grant')
    @pytest.mark.asyncio
    async def test_async_tokens_client_network_error_handling(self, mock_grant, async_client_wrapper):
        """Test AsyncTokensClient network error handling."""
        # Mock a network error
        mock_grant.side_effect = httpx.ConnectError("Async connection failed")
        
        client = AsyncTokensClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises(httpx.ConnectError):
            await client.grant()

    def test_client_wrapper_integration(self, sync_client_wrapper):
        """Test integration with client wrapper."""
        client = AuthClient(client_wrapper=sync_client_wrapper)
        
        # Test that client wrapper methods are accessible
        assert hasattr(client._client_wrapper, 'get_environment')
        assert hasattr(client._client_wrapper, 'get_headers')
        assert hasattr(client._client_wrapper, 'api_key')
        
        environment = client._client_wrapper.get_environment()
        headers = client._client_wrapper.get_headers()
        api_key = client._client_wrapper.api_key
        
        assert environment is not None
        assert isinstance(headers, dict)
        assert api_key is not None
