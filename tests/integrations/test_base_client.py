"""Integration tests for BaseClient and AsyncBaseClient."""

import pytest
from unittest.mock import Mock, patch
import httpx

from deepgram.base_client import BaseClient, AsyncBaseClient
from deepgram.environment import DeepgramClientEnvironment
from deepgram.core.api_error import ApiError


class TestBaseClient:
    """Test cases for BaseClient."""

    def test_base_client_initialization(self, mock_api_key):
        """Test BaseClient initialization."""
        client = BaseClient(api_key=mock_api_key)
        
        assert client is not None
        assert client._client_wrapper is not None

    def test_base_client_initialization_without_api_key(self):
        """Test BaseClient initialization fails without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ApiError) as exc_info:
                BaseClient()
            
            assert "api_key" in str(exc_info.value.body).lower()

    def test_base_client_with_environment(self, mock_api_key):
        """Test BaseClient with specific environment."""
        client = BaseClient(
            api_key=mock_api_key,
            environment=DeepgramClientEnvironment.PRODUCTION
        )
        
        assert client is not None

    def test_base_client_with_custom_headers(self, mock_api_key):
        """Test BaseClient with custom headers."""
        headers = {"X-Custom-Header": "test-value"}
        client = BaseClient(api_key=mock_api_key, headers=headers)
        
        assert client is not None

    def test_base_client_with_timeout(self, mock_api_key):
        """Test BaseClient with custom timeout."""
        client = BaseClient(api_key=mock_api_key, timeout=120.0)
        
        assert client is not None

    def test_base_client_with_follow_redirects(self, mock_api_key):
        """Test BaseClient with follow_redirects setting."""
        client = BaseClient(api_key=mock_api_key, follow_redirects=False)
        
        assert client is not None

    def test_base_client_with_custom_httpx_client(self, mock_api_key):
        """Test BaseClient with custom httpx client."""
        custom_client = httpx.Client(timeout=30.0)
        client = BaseClient(api_key=mock_api_key, httpx_client=custom_client)
        
        assert client is not None

    def test_base_client_property_access(self, mock_api_key):
        """Test BaseClient property access."""
        client = BaseClient(api_key=mock_api_key)
        
        # Test that all properties are accessible
        assert client.agent is not None
        assert client.auth is not None
        assert client.listen is not None
        assert client.manage is not None
        assert client.read is not None
        assert client.self_hosted is not None
        assert client.speak is not None

    def test_base_client_timeout_defaulting(self, mock_api_key):
        """Test BaseClient timeout defaulting behavior."""
        # Test with no timeout specified
        client = BaseClient(api_key=mock_api_key)
        assert client is not None
        
        # Test with custom httpx client that has timeout
        custom_client = httpx.Client(timeout=45.0)
        client = BaseClient(api_key=mock_api_key, httpx_client=custom_client)
        assert client is not None


class TestAsyncBaseClient:
    """Test cases for AsyncBaseClient."""

    def test_async_base_client_initialization(self, mock_api_key):
        """Test AsyncBaseClient initialization."""
        client = AsyncBaseClient(api_key=mock_api_key)
        
        assert client is not None
        assert client._client_wrapper is not None

    def test_async_base_client_initialization_without_api_key(self):
        """Test AsyncBaseClient initialization fails without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ApiError) as exc_info:
                AsyncBaseClient()
            
            assert "api_key" in str(exc_info.value.body).lower()

    def test_async_base_client_with_environment(self, mock_api_key):
        """Test AsyncBaseClient with specific environment."""
        client = AsyncBaseClient(
            api_key=mock_api_key,
            environment=DeepgramClientEnvironment.PRODUCTION
        )
        
        assert client is not None

    def test_async_base_client_with_custom_headers(self, mock_api_key):
        """Test AsyncBaseClient with custom headers."""
        headers = {"X-Custom-Header": "test-value"}
        client = AsyncBaseClient(api_key=mock_api_key, headers=headers)
        
        assert client is not None

    def test_async_base_client_with_timeout(self, mock_api_key):
        """Test AsyncBaseClient with custom timeout."""
        client = AsyncBaseClient(api_key=mock_api_key, timeout=120.0)
        
        assert client is not None

    def test_async_base_client_with_follow_redirects(self, mock_api_key):
        """Test AsyncBaseClient with follow_redirects setting."""
        client = AsyncBaseClient(api_key=mock_api_key, follow_redirects=False)
        
        assert client is not None

    def test_async_base_client_with_custom_httpx_client(self, mock_api_key):
        """Test AsyncBaseClient with custom httpx async client."""
        custom_client = httpx.AsyncClient(timeout=30.0)
        client = AsyncBaseClient(api_key=mock_api_key, httpx_client=custom_client)
        
        assert client is not None

    def test_async_base_client_property_access(self, mock_api_key):
        """Test AsyncBaseClient property access."""
        client = AsyncBaseClient(api_key=mock_api_key)
        
        # Test that all properties are accessible
        assert client.agent is not None
        assert client.auth is not None
        assert client.listen is not None
        assert client.manage is not None
        assert client.read is not None
        assert client.self_hosted is not None
        assert client.speak is not None

    def test_async_base_client_timeout_defaulting(self, mock_api_key):
        """Test AsyncBaseClient timeout defaulting behavior."""
        # Test with no timeout specified
        client = AsyncBaseClient(api_key=mock_api_key)
        assert client is not None
        
        # Test with custom httpx client that has timeout
        custom_client = httpx.AsyncClient(timeout=45.0)
        client = AsyncBaseClient(api_key=mock_api_key, httpx_client=custom_client)
        assert client is not None


class TestBaseClientWrapperIntegration:
    """Test BaseClient integration with client wrapper."""

    def test_sync_client_wrapper_creation(self, mock_api_key):
        """Test synchronous client wrapper creation."""
        client = BaseClient(api_key=mock_api_key)
        
        wrapper = client._client_wrapper
        assert wrapper is not None
        assert hasattr(wrapper, 'get_environment')
        assert hasattr(wrapper, 'get_headers')
        assert hasattr(wrapper, 'api_key')

    def test_async_client_wrapper_creation(self, mock_api_key):
        """Test asynchronous client wrapper creation."""
        client = AsyncBaseClient(api_key=mock_api_key)
        
        wrapper = client._client_wrapper
        assert wrapper is not None
        assert hasattr(wrapper, 'get_environment')
        assert hasattr(wrapper, 'get_headers')
        assert hasattr(wrapper, 'api_key')

    def test_client_wrapper_environment_access(self, mock_api_key):
        """Test client wrapper environment access."""
        client = BaseClient(
            api_key=mock_api_key,
            environment=DeepgramClientEnvironment.PRODUCTION
        )
        
        environment = client._client_wrapper.get_environment()
        assert environment is not None
        assert hasattr(environment, 'production')

    def test_client_wrapper_headers_access(self, mock_api_key):
        """Test client wrapper headers access."""
        custom_headers = {"X-Test-Header": "test-value"}
        client = BaseClient(api_key=mock_api_key, headers=custom_headers)
        
        headers = client._client_wrapper.get_headers()
        assert isinstance(headers, dict)
        assert "X-Test-Header" in headers
        assert headers["X-Test-Header"] == "test-value"

    def test_client_wrapper_api_key_access(self, mock_api_key):
        """Test client wrapper API key access."""
        client = BaseClient(api_key=mock_api_key)
        
        api_key = client._client_wrapper.api_key
        assert api_key == mock_api_key
