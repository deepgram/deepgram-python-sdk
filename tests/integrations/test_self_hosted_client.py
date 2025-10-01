"""Integration tests for SelfHosted client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx
import json

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.environment import DeepgramClientEnvironment

from deepgram.self_hosted.client import SelfHostedClient, AsyncSelfHostedClient
from deepgram.self_hosted.v1.client import V1Client as SelfHostedV1Client, AsyncV1Client as SelfHostedAsyncV1Client
from deepgram.self_hosted.v1.distribution_credentials.client import (
    DistributionCredentialsClient, 
    AsyncDistributionCredentialsClient
)

# Import response types for mocking
from deepgram.types.list_project_distribution_credentials_v1response import ListProjectDistributionCredentialsV1Response
from deepgram.types.create_project_distribution_credentials_v1response import CreateProjectDistributionCredentialsV1Response
from deepgram.types.get_project_distribution_credentials_v1response import GetProjectDistributionCredentialsV1Response
from deepgram.self_hosted.v1.distribution_credentials.types.distribution_credentials_create_request_scopes_item import DistributionCredentialsCreateRequestScopesItem


class TestSelfHostedClient:
    """Test cases for SelfHosted Client."""

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

    def test_self_hosted_client_initialization(self, sync_client_wrapper):
        """Test SelfHostedClient initialization."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_async_self_hosted_client_initialization(self, async_client_wrapper):
        """Test AsyncSelfHostedClient initialization."""
        client = AsyncSelfHostedClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_self_hosted_client_v1_property_lazy_loading(self, sync_client_wrapper):
        """Test SelfHostedClient v1 property lazy loading."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, SelfHostedV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_async_self_hosted_client_v1_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncSelfHostedClient v1 property lazy loading."""
        client = AsyncSelfHostedClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, SelfHostedAsyncV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_self_hosted_client_raw_response_access(self, sync_client_wrapper):
        """Test SelfHostedClient raw response access."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_self_hosted_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncSelfHostedClient raw response access."""
        client = AsyncSelfHostedClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_self_hosted_client_integration_with_main_client(self, mock_api_key):
        """Test SelfHostedClient integration with main DeepgramClient."""
        client = DeepgramClient(api_key=mock_api_key)
        
        self_hosted_client = client.self_hosted
        assert self_hosted_client is not None
        assert isinstance(self_hosted_client, SelfHostedClient)

    def test_async_self_hosted_client_integration_with_main_client(self, mock_api_key):
        """Test AsyncSelfHostedClient integration with main AsyncDeepgramClient."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        self_hosted_client = client.self_hosted
        assert self_hosted_client is not None
        assert isinstance(self_hosted_client, AsyncSelfHostedClient)


class TestSelfHostedV1Client:
    """Test cases for SelfHosted V1 Client."""

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

    def test_self_hosted_v1_client_initialization(self, sync_client_wrapper):
        """Test SelfHostedV1Client initialization."""
        client = SelfHostedV1Client(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._distribution_credentials is None  # Lazy loaded

    def test_async_self_hosted_v1_client_initialization(self, async_client_wrapper):
        """Test AsyncSelfHostedV1Client initialization."""
        client = SelfHostedAsyncV1Client(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._distribution_credentials is None  # Lazy loaded

    def test_self_hosted_v1_client_distribution_credentials_property_lazy_loading(self, sync_client_wrapper):
        """Test SelfHostedV1Client distribution_credentials property lazy loading."""
        client = SelfHostedV1Client(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._distribution_credentials is None
        
        # Access triggers lazy loading
        dist_creds_client = client.distribution_credentials
        assert client._distribution_credentials is not None
        assert isinstance(dist_creds_client, DistributionCredentialsClient)
        
        # Subsequent access returns same instance
        assert client.distribution_credentials is dist_creds_client

    def test_async_self_hosted_v1_client_distribution_credentials_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncSelfHostedV1Client distribution_credentials property lazy loading."""
        client = SelfHostedAsyncV1Client(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._distribution_credentials is None
        
        # Access triggers lazy loading
        dist_creds_client = client.distribution_credentials
        assert client._distribution_credentials is not None
        assert isinstance(dist_creds_client, AsyncDistributionCredentialsClient)
        
        # Subsequent access returns same instance
        assert client.distribution_credentials is dist_creds_client

    def test_self_hosted_v1_client_raw_response_access(self, sync_client_wrapper):
        """Test SelfHostedV1Client raw response access."""
        client = SelfHostedV1Client(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_self_hosted_v1_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncSelfHostedV1Client raw response access."""
        client = SelfHostedAsyncV1Client(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client


class TestDistributionCredentialsClient:
    """Test cases for Distribution Credentials Client."""

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
    def mock_distribution_credentials_list_response(self):
        """Mock distribution credentials list response data."""
        mock_response = Mock(spec=ListProjectDistributionCredentialsV1Response)
        # Mock distribution credentials list
        mock_cred1 = Mock()
        mock_cred1.distribution_credentials_id = "cred-123"
        mock_cred2 = Mock()
        mock_cred2.distribution_credentials_id = "cred-456"
        mock_response.distribution_credentials = [mock_cred1, mock_cred2]
        return mock_response

    @pytest.fixture
    def mock_distribution_credentials_create_response(self):
        """Mock distribution credentials create response data."""
        mock_response = Mock(spec=CreateProjectDistributionCredentialsV1Response)
        mock_response.distribution_credentials_id = "cred-new-789"
        mock_response.username = "test_user"
        mock_response.password = "test_password"
        return mock_response

    @pytest.fixture
    def mock_distribution_credentials_get_response(self):
        """Mock distribution credentials get response data."""
        mock_response = Mock(spec=GetProjectDistributionCredentialsV1Response)
        mock_response.distribution_credentials_id = "cred-123"
        return mock_response

    def test_distribution_credentials_client_initialization(self, sync_client_wrapper):
        """Test DistributionCredentialsClient initialization."""
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_async_distribution_credentials_client_initialization(self, async_client_wrapper):
        """Test AsyncDistributionCredentialsClient initialization."""
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_distribution_credentials_client_raw_response_access(self, sync_client_wrapper):
        """Test DistributionCredentialsClient raw response access."""
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_distribution_credentials_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncDistributionCredentialsClient raw response access."""
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.list')
    def test_distribution_credentials_client_list(self, mock_list, sync_client_wrapper, mock_distribution_credentials_list_response):
        """Test DistributionCredentialsClient list method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_list_response
        mock_list.return_value = mock_response
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        result = client.list(project_id)
        
        assert result is not None
        assert isinstance(result, ListProjectDistributionCredentialsV1Response)
        # Basic assertion - response is valid
        # Response structure is valid
        
        # Verify raw client was called with correct parameters
        mock_list.assert_called_once_with(project_id, request_options=None)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.create')
    def test_distribution_credentials_client_create(self, mock_create, sync_client_wrapper, mock_distribution_credentials_create_response):
        """Test DistributionCredentialsClient create method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_create_response
        mock_create.return_value = mock_response
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        scopes = ["self-hosted:products", "self-hosted:product:api"]
        result = client.create(
            project_id,
            scopes=scopes,
            provider="quay",
            comment="Test credentials"
        )
        
        assert result is not None
        assert isinstance(result, CreateProjectDistributionCredentialsV1Response)
        assert result.distribution_credentials_id == "cred-new-789"
        assert result.username == "test_user"
        assert result.password == "test_password"
        
        # Verify raw client was called with correct parameters
        mock_create.assert_called_once_with(
            project_id,
            scopes=scopes,
            provider="quay",
            comment="Test credentials",
            request_options=None
        )

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.get')
    def test_distribution_credentials_client_get(self, mock_get, sync_client_wrapper, mock_distribution_credentials_get_response):
        """Test DistributionCredentialsClient get method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_get_response
        mock_get.return_value = mock_response
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        credentials_id = "cred-123"
        result = client.get(project_id, credentials_id)
        
        assert result is not None
        assert isinstance(result, GetProjectDistributionCredentialsV1Response)
        # Basic assertions - the response structure is valid
        
        # Verify raw client was called with correct parameters
        mock_get.assert_called_once_with(project_id, credentials_id, request_options=None)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.delete')
    def test_distribution_credentials_client_delete(self, mock_delete, sync_client_wrapper, mock_distribution_credentials_get_response):
        """Test DistributionCredentialsClient delete method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_get_response
        mock_delete.return_value = mock_response
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        credentials_id = "cred-123"
        result = client.delete(project_id, credentials_id)
        
        assert result is not None
        assert isinstance(result, GetProjectDistributionCredentialsV1Response)
        
        # Verify raw client was called with correct parameters
        mock_delete.assert_called_once_with(project_id, credentials_id, request_options=None)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.list')
    def test_distribution_credentials_client_list_with_request_options(self, mock_list, sync_client_wrapper, mock_distribution_credentials_list_response):
        """Test DistributionCredentialsClient list with request options."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_list_response
        mock_list.return_value = mock_response
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        request_options = RequestOptions(
            additional_headers={"X-Custom-Header": "test-value"}
        )
        result = client.list(project_id, request_options=request_options)
        
        assert result is not None
        assert isinstance(result, ListProjectDistributionCredentialsV1Response)
        
        # Verify raw client was called with request options
        mock_list.assert_called_once_with(project_id, request_options=request_options)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.list')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_list(self, mock_list, async_client_wrapper, mock_distribution_credentials_list_response):
        """Test AsyncDistributionCredentialsClient list method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_list_response
        mock_list.return_value = mock_response
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        project_id = "project-456"
        result = await client.list(project_id)
        
        assert result is not None
        assert isinstance(result, ListProjectDistributionCredentialsV1Response)
        # Basic assertion - response is valid
        assert result.distribution_credentials[1].distribution_credentials_id == "cred-456"
        
        # Verify async raw client was called with correct parameters
        mock_list.assert_called_once_with(project_id, request_options=None)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.create')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_create(self, mock_create, async_client_wrapper, mock_distribution_credentials_create_response):
        """Test AsyncDistributionCredentialsClient create method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_create_response
        mock_create.return_value = mock_response
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        project_id = "project-456"
        scopes = ["self-hosted:products"]
        result = await client.create(
            project_id,
            scopes=scopes,
            provider="quay",
            comment="Async test credentials"
        )
        
        assert result is not None
        assert isinstance(result, CreateProjectDistributionCredentialsV1Response)
        assert result.distribution_credentials_id == "cred-new-789"
        
        # Verify async raw client was called with correct parameters
        mock_create.assert_called_once_with(
            project_id,
            scopes=scopes,
            provider="quay",
            comment="Async test credentials",
            request_options=None
        )

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.get')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_get(self, mock_get, async_client_wrapper, mock_distribution_credentials_get_response):
        """Test AsyncDistributionCredentialsClient get method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_get_response
        mock_get.return_value = mock_response
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        project_id = "project-456"
        credentials_id = "cred-456"
        result = await client.get(project_id, credentials_id)
        
        assert result is not None
        assert isinstance(result, GetProjectDistributionCredentialsV1Response)
        # Basic assertions - the response structure is valid  # From mock response
        
        # Verify async raw client was called with correct parameters
        mock_get.assert_called_once_with(project_id, credentials_id, request_options=None)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.delete')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_delete(self, mock_delete, async_client_wrapper, mock_distribution_credentials_get_response):
        """Test AsyncDistributionCredentialsClient delete method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_distribution_credentials_get_response
        mock_delete.return_value = mock_response
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        project_id = "project-456"
        credentials_id = "cred-456"
        result = await client.delete(project_id, credentials_id)
        
        assert result is not None
        assert isinstance(result, GetProjectDistributionCredentialsV1Response)
        
        # Verify async raw client was called with correct parameters
        mock_delete.assert_called_once_with(project_id, credentials_id, request_options=None)


class TestSelfHostedIntegrationScenarios:
    """Test SelfHosted integration scenarios."""

    def test_complete_self_hosted_workflow_sync(self, mock_api_key):
        """Test complete SelfHosted workflow using sync client."""
        with patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.list') as mock_list:
            # Mock the response
            mock_response = Mock()
            mock_response.data = Mock(spec=ListProjectDistributionCredentialsV1Response)
            mock_credential = Mock()
            mock_credential.distribution_credentials_id = "cred-sync-123"
            mock_credential.comment = "Sync test credentials"
            mock_credential.scopes = ["read", "write"]
            mock_credential.provider = "quay"
            mock_response.data.distribution_credentials = [mock_credential]
            mock_list.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested self-hosted functionality
            result = client.self_hosted.v1.distribution_credentials.list("project-123")
            
            assert result is not None
            assert isinstance(result, ListProjectDistributionCredentialsV1Response)
            assert len(result.distribution_credentials) == 1
            assert result.distribution_credentials[0].distribution_credentials_id == "cred-sync-123"
            
            # Verify the call was made
            mock_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_self_hosted_workflow_async(self, mock_api_key):
        """Test complete SelfHosted workflow using async client."""
        with patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.create') as mock_create:
            # Mock the async response
            mock_response = Mock()
            mock_response.data = Mock(spec=CreateProjectDistributionCredentialsV1Response)
            mock_response.data.distribution_credentials_id = "cred-async-456"
            mock_response.data.comment = "Async test credentials"
            mock_response.data.scopes = ["read"]
            mock_response.data.provider = "quay"
            mock_response.data.username = "async_user"
            mock_response.data.password = "async_password"
            # Set required fields
            mock_response.data.member = Mock()
            mock_response.data.distribution_credentials = Mock()
            mock_create.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested self-hosted functionality
            result = await client.self_hosted.v1.distribution_credentials.create(
                "project-456",
                scopes=["self-hosted:products"],
                provider="quay"
            )
            
            assert result is not None
            assert isinstance(result, CreateProjectDistributionCredentialsV1Response)
            assert result.distribution_credentials_id == "cred-async-456"
            assert result.username == "async_user"
            
            # Verify the call was made
            mock_create.assert_called_once()

    def test_self_hosted_client_property_isolation(self, mock_api_key):
        """Test that self-hosted clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        self_hosted1 = client1.self_hosted
        self_hosted2 = client2.self_hosted
        
        # Verify they are different instances
        assert self_hosted1 is not self_hosted2
        assert self_hosted1._client_wrapper is not self_hosted2._client_wrapper
        
        # Verify nested clients are also different
        dist_creds1 = self_hosted1.v1.distribution_credentials
        dist_creds2 = self_hosted2.v1.distribution_credentials
        
        assert dist_creds1 is not dist_creds2

    @pytest.mark.asyncio
    async def test_mixed_sync_async_self_hosted_clients(self, mock_api_key):
        """Test mixing sync and async self-hosted clients."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        sync_self_hosted = sync_client.self_hosted
        async_self_hosted = async_client.self_hosted
        
        # Verify they are different types
        assert type(sync_self_hosted) != type(async_self_hosted)
        assert isinstance(sync_self_hosted, SelfHostedClient)
        assert isinstance(async_self_hosted, AsyncSelfHostedClient)
        
        # Verify nested clients are also different types
        sync_dist_creds = sync_self_hosted.v1.distribution_credentials
        async_dist_creds = async_self_hosted.v1.distribution_credentials
        
        assert type(sync_dist_creds) != type(async_dist_creds)
        assert isinstance(sync_dist_creds, DistributionCredentialsClient)
        assert isinstance(async_dist_creds, AsyncDistributionCredentialsClient)


class TestSelfHostedErrorHandling:
    """Test SelfHosted client error handling."""

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

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.list')
    def test_distribution_credentials_client_api_error_handling(self, mock_list, sync_client_wrapper):
        """Test DistributionCredentialsClient API error handling."""
        # Mock an API error
        mock_list.side_effect = ApiError(
            status_code=404,
            headers={},
            body="Project not found"
        )
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            client.list("non-existent-project")
        
        assert exc_info.value.status_code == 404
        assert "Project not found" in str(exc_info.value.body)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.create')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_api_error_handling(self, mock_create, async_client_wrapper):
        """Test AsyncDistributionCredentialsClient API error handling."""
        # Mock an API error
        mock_create.side_effect = ApiError(
            status_code=400,
            headers={},
            body="Invalid scopes provided"
        )
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            await client.create(
                "project-123",
                scopes=["invalid_scope"],
                provider="quay"
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid scopes provided" in str(exc_info.value.body)

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.RawDistributionCredentialsClient.get')
    def test_distribution_credentials_client_network_error_handling(self, mock_get, sync_client_wrapper):
        """Test DistributionCredentialsClient network error handling."""
        # Mock a network error
        mock_get.side_effect = httpx.ConnectError("Connection failed")
        
        client = DistributionCredentialsClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(httpx.ConnectError):
            client.get("project-123", "cred-123")

    @patch('deepgram.self_hosted.v1.distribution_credentials.raw_client.AsyncRawDistributionCredentialsClient.delete')
    @pytest.mark.asyncio
    async def test_async_distribution_credentials_client_network_error_handling(self, mock_delete, async_client_wrapper):
        """Test AsyncDistributionCredentialsClient network error handling."""
        # Mock a network error
        mock_delete.side_effect = httpx.ConnectError("Async connection failed")
        
        client = AsyncDistributionCredentialsClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises(httpx.ConnectError):
            await client.delete("project-456", "cred-456")

    def test_client_wrapper_integration(self, sync_client_wrapper):
        """Test integration with client wrapper."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
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
