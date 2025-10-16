"""Integration tests for Manage client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx
import json

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.environment import DeepgramClientEnvironment

from deepgram.manage.client import ManageClient, AsyncManageClient
from deepgram.manage.v1.client import V1Client as ManageV1Client, AsyncV1Client as ManageAsyncV1Client
from deepgram.manage.v1.projects.client import ProjectsClient, AsyncProjectsClient
from deepgram.manage.v1.models.client import ModelsClient, AsyncModelsClient

# Import response types for mocking
from deepgram.types.list_projects_v1response import ListProjectsV1Response
from deepgram.types.get_project_v1response import GetProjectV1Response
from deepgram.types.list_models_v1response import ListModelsV1Response
from deepgram.types.get_model_v1response import GetModelV1Response
from deepgram.types.get_model_v1response_batch import GetModelV1ResponseBatch
from deepgram.types.get_model_v1response_metadata import GetModelV1ResponseMetadata


class TestManageClient:
    """Test cases for Manage Client."""

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

    def test_manage_client_initialization(self, sync_client_wrapper):
        """Test ManageClient initialization."""
        client = ManageClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_async_manage_client_initialization(self, async_client_wrapper):
        """Test AsyncManageClient initialization."""
        client = AsyncManageClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_manage_client_v1_property_lazy_loading(self, sync_client_wrapper):
        """Test ManageClient v1 property lazy loading."""
        client = ManageClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, ManageV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_async_manage_client_v1_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncManageClient v1 property lazy loading."""
        client = AsyncManageClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, ManageAsyncV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_manage_client_raw_response_access(self, sync_client_wrapper):
        """Test ManageClient raw response access."""
        client = ManageClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_manage_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncManageClient raw response access."""
        client = AsyncManageClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_manage_client_integration_with_main_client(self, mock_api_key):
        """Test ManageClient integration with main DeepgramClient."""
        client = DeepgramClient(api_key=mock_api_key)
        
        manage_client = client.manage
        assert manage_client is not None
        assert isinstance(manage_client, ManageClient)

    def test_async_manage_client_integration_with_main_client(self, mock_api_key):
        """Test AsyncManageClient integration with main AsyncDeepgramClient."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        manage_client = client.manage
        assert manage_client is not None
        assert isinstance(manage_client, AsyncManageClient)


class TestManageV1Client:
    """Test cases for Manage V1 Client."""

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

    def test_manage_v1_client_initialization(self, sync_client_wrapper):
        """Test ManageV1Client initialization."""
        client = ManageV1Client(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._projects is None  # Lazy loaded
        assert client._models is None  # Lazy loaded

    def test_async_manage_v1_client_initialization(self, async_client_wrapper):
        """Test AsyncManageV1Client initialization."""
        client = ManageAsyncV1Client(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._projects is None  # Lazy loaded
        assert client._models is None  # Lazy loaded

    def test_manage_v1_client_projects_property_lazy_loading(self, sync_client_wrapper):
        """Test ManageV1Client projects property lazy loading."""
        client = ManageV1Client(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._projects is None
        
        # Access triggers lazy loading
        projects_client = client.projects
        assert client._projects is not None
        assert isinstance(projects_client, ProjectsClient)
        
        # Subsequent access returns same instance
        assert client.projects is projects_client

    def test_async_manage_v1_client_projects_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncManageV1Client projects property lazy loading."""
        client = ManageAsyncV1Client(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._projects is None
        
        # Access triggers lazy loading
        projects_client = client.projects
        assert client._projects is not None
        assert isinstance(projects_client, AsyncProjectsClient)
        
        # Subsequent access returns same instance
        assert client.projects is projects_client

    def test_manage_v1_client_models_property_lazy_loading(self, sync_client_wrapper):
        """Test ManageV1Client models property lazy loading."""
        client = ManageV1Client(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._models is None
        
        # Access triggers lazy loading
        models_client = client.models
        assert client._models is not None
        assert isinstance(models_client, ModelsClient)
        
        # Subsequent access returns same instance
        assert client.models is models_client

    def test_async_manage_v1_client_models_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncManageV1Client models property lazy loading."""
        client = ManageAsyncV1Client(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._models is None
        
        # Access triggers lazy loading
        models_client = client.models
        assert client._models is not None
        assert isinstance(models_client, AsyncModelsClient)
        
        # Subsequent access returns same instance
        assert client.models is models_client


class TestProjectsClient:
    """Test cases for Projects Client."""

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
    def mock_projects_list_response(self):
        """Mock projects list response data."""
        return {
            "projects": [
                {
                    "project_id": "project-123",
                    "name": "Test Project 1",
                    "company": "Test Company"
                },
                {
                    "project_id": "project-456", 
                    "name": "Test Project 2",
                    "company": "Test Company"
                }
            ]
        }

    @pytest.fixture
    def mock_project_get_response(self):
        """Mock project get response data."""
        return {
            "project_id": "project-123",
            "name": "Test Project",
            "company": "Test Company"
        }

    def test_projects_client_initialization(self, sync_client_wrapper):
        """Test ProjectsClient initialization."""
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_async_projects_client_initialization(self, async_client_wrapper):
        """Test AsyncProjectsClient initialization."""
        client = AsyncProjectsClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_projects_client_raw_response_access(self, sync_client_wrapper):
        """Test ProjectsClient raw response access."""
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_projects_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncProjectsClient raw response access."""
        client = AsyncProjectsClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.list')
    def test_projects_client_list(self, mock_list, sync_client_wrapper, mock_projects_list_response):
        """Test ProjectsClient list method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = ListProjectsV1Response(**mock_projects_list_response)
        mock_list.return_value = mock_response
        
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        result = client.list()
        
        assert result is not None
        assert isinstance(result, ListProjectsV1Response)
        assert len(result.projects) == 2
        assert result.projects[0].project_id == "project-123"
        
        # Verify raw client was called with correct parameters
        mock_list.assert_called_once_with(request_options=None)

    @patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.get')
    def test_projects_client_get(self, mock_get, sync_client_wrapper, mock_project_get_response):
        """Test ProjectsClient get method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = GetProjectV1Response(**mock_project_get_response)
        mock_get.return_value = mock_response
        
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        project_id = "project-123"
        result = client.get(project_id)
        
        assert result is not None
        assert isinstance(result, GetProjectV1Response)
        assert result.project_id == project_id
        
        # Verify raw client was called with correct parameters
        mock_get.assert_called_once_with(
            project_id,
            limit=None,
            page=None,
            request_options=None
        )

    @patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.list')
    def test_projects_client_list_with_request_options(self, mock_list, sync_client_wrapper, mock_projects_list_response):
        """Test ProjectsClient list with request options."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = ListProjectsV1Response(**mock_projects_list_response)
        mock_list.return_value = mock_response
        
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        request_options = RequestOptions(
            additional_headers={"X-Custom-Header": "test-value"}
        )
        result = client.list(request_options=request_options)
        
        assert result is not None
        assert isinstance(result, ListProjectsV1Response)
        
        # Verify raw client was called with request options
        mock_list.assert_called_once_with(request_options=request_options)

    @patch('deepgram.manage.v1.projects.raw_client.AsyncRawProjectsClient.list')
    @pytest.mark.asyncio
    async def test_async_projects_client_list(self, mock_list, async_client_wrapper, mock_projects_list_response):
        """Test AsyncProjectsClient list method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = ListProjectsV1Response(**mock_projects_list_response)
        mock_list.return_value = mock_response
        
        client = AsyncProjectsClient(client_wrapper=async_client_wrapper)
        
        result = await client.list()
        
        assert result is not None
        assert isinstance(result, ListProjectsV1Response)
        assert len(result.projects) == 2
        assert result.projects[0].project_id == "project-123"
        
        # Verify async raw client was called with correct parameters
        mock_list.assert_called_once_with(request_options=None)

    @patch('deepgram.manage.v1.projects.raw_client.AsyncRawProjectsClient.get')
    @pytest.mark.asyncio
    async def test_async_projects_client_get(self, mock_get, async_client_wrapper, mock_project_get_response):
        """Test AsyncProjectsClient get method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = GetProjectV1Response(**mock_project_get_response)
        mock_get.return_value = mock_response
        
        client = AsyncProjectsClient(client_wrapper=async_client_wrapper)
        
        project_id = "project-456"
        result = await client.get(project_id, limit=10, page=1)
        
        assert result is not None
        assert isinstance(result, GetProjectV1Response)
        assert result.project_id == "project-123"  # From mock response
        
        # Verify async raw client was called with correct parameters
        mock_get.assert_called_once_with(
            project_id,
            limit=10,
            page=1,
            request_options=None
        )


class TestModelsClient:
    """Test cases for Models Client."""

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
    def mock_models_list_response(self):
        """Mock models list response data."""
        return {
            "models": [
                {
                    "model_id": "nova-2-general",
                    "name": "Nova 2 General",
                    "canonical_name": "nova-2-general",
                    "architecture": "nova-2",
                    "language": "en",
                    "version": "2024-01-09",
                    "uuid": "uuid-123",
                    "batch": False,
                    "streaming": True
                },
                {
                    "model_id": "nova-2-medical",
                    "name": "Nova 2 Medical",
                    "canonical_name": "nova-2-medical",
                    "architecture": "nova-2",
                    "language": "en",
                    "version": "2024-01-09",
                    "uuid": "uuid-456",
                    "batch": True,
                    "streaming": True
                }
            ]
        }

    @pytest.fixture
    def mock_model_get_response(self):
        """Mock model get response data."""
        return {
            "model_id": "nova-2-general",
            "name": "Nova 2 General",
            "canonical_name": "nova-2-general",
            "architecture": "nova-2",
            "language": "en",
            "version": "2024-01-09",
            "uuid": "uuid-123",
            "batch": False,
            "streaming": True
        }

    def test_models_client_initialization(self, sync_client_wrapper):
        """Test ModelsClient initialization."""
        client = ModelsClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_async_models_client_initialization(self, async_client_wrapper):
        """Test AsyncModelsClient initialization."""
        client = AsyncModelsClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_models_client_raw_response_access(self, sync_client_wrapper):
        """Test ModelsClient raw response access."""
        client = ModelsClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_models_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncModelsClient raw response access."""
        client = AsyncModelsClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.manage.v1.models.raw_client.RawModelsClient.list')
    def test_models_client_list(self, mock_list, sync_client_wrapper, mock_models_list_response):
        """Test ModelsClient list method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = ListModelsV1Response(**mock_models_list_response)
        mock_list.return_value = mock_response
        
        client = ModelsClient(client_wrapper=sync_client_wrapper)
        
        result = client.list()
        
        assert result is not None
        assert isinstance(result, ListModelsV1Response)
        assert len(result.models) == 2
        assert result.models[0]["model_id"] == "nova-2-general"
        
        # Verify raw client was called with correct parameters
        mock_list.assert_called_once_with(include_outdated=None, request_options=None)

    @patch('deepgram.manage.v1.models.raw_client.RawModelsClient.list')
    def test_models_client_list_include_outdated(self, mock_list, sync_client_wrapper, mock_models_list_response):
        """Test ModelsClient list with include_outdated parameter."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = ListModelsV1Response(**mock_models_list_response)
        mock_list.return_value = mock_response
        
        client = ModelsClient(client_wrapper=sync_client_wrapper)
        
        result = client.list(include_outdated=True)
        
        assert result is not None
        assert isinstance(result, ListModelsV1Response)
        
        # Verify raw client was called with include_outdated parameter
        mock_list.assert_called_once_with(include_outdated=True, request_options=None)

    @patch('deepgram.manage.v1.models.raw_client.RawModelsClient.get')
    def test_models_client_get(self, mock_get, sync_client_wrapper, mock_model_get_response):
        """Test ModelsClient get method."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = Mock(spec=GetModelV1ResponseBatch)
        # Set attributes from mock data
        for key, value in mock_model_get_response.items():
            setattr(mock_response.data, key, value)
        mock_get.return_value = mock_response
        
        client = ModelsClient(client_wrapper=sync_client_wrapper)
        
        model_id = "nova-2-general"
        result = client.get(model_id)
        
        assert result is not None
        assert isinstance(result, (GetModelV1ResponseBatch, GetModelV1ResponseMetadata))
        assert result.model_id == model_id
        
        # Verify raw client was called with correct parameters
        mock_get.assert_called_once_with(model_id, request_options=None)

    @patch('deepgram.manage.v1.models.raw_client.AsyncRawModelsClient.list')
    @pytest.mark.asyncio
    async def test_async_models_client_list(self, mock_list, async_client_wrapper, mock_models_list_response):
        """Test AsyncModelsClient list method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = ListModelsV1Response(**mock_models_list_response)
        mock_list.return_value = mock_response
        
        client = AsyncModelsClient(client_wrapper=async_client_wrapper)
        
        result = await client.list(include_outdated=False)
        
        assert result is not None
        assert isinstance(result, ListModelsV1Response)
        assert len(result.models) == 2
        assert result.models[1]["model_id"] == "nova-2-medical"
        
        # Verify async raw client was called with correct parameters
        mock_list.assert_called_once_with(include_outdated=False, request_options=None)

    @patch('deepgram.manage.v1.models.raw_client.AsyncRawModelsClient.get')
    @pytest.mark.asyncio
    async def test_async_models_client_get(self, mock_get, async_client_wrapper, mock_model_get_response):
        """Test AsyncModelsClient get method."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = Mock(spec=GetModelV1ResponseBatch)
        # Set attributes from mock data
        for key, value in mock_model_get_response.items():
            setattr(mock_response.data, key, value)
        mock_get.return_value = mock_response
        
        client = AsyncModelsClient(client_wrapper=async_client_wrapper)
        
        model_id = "nova-2-medical"
        result = await client.get(model_id)
        
        assert result is not None
        assert isinstance(result, (GetModelV1ResponseBatch, GetModelV1ResponseMetadata))
        assert result.model_id == "nova-2-general"  # From mock response
        
        # Verify async raw client was called with correct parameters
        mock_get.assert_called_once_with(model_id, request_options=None)


class TestManageIntegrationScenarios:
    """Test Manage integration scenarios."""

    def test_complete_manage_workflow_sync(self, mock_api_key):
        """Test complete Manage workflow using sync client."""
        with patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.list') as mock_list:
            # Mock the response
            mock_response = Mock()
            mock_response.data = Mock(spec=ListProjectsV1Response)
            mock_project = Mock()
            mock_project.project_id = "project-123"
            mock_project.name = "Test Project"
            mock_project.company = "Test Company"
            mock_response.data.projects = [mock_project]
            mock_list.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Access nested manage functionality
            result = client.manage.v1.projects.list()
            
            assert result is not None
            assert isinstance(result, ListProjectsV1Response)
            assert len(result.projects) == 1
            
            # Verify the call was made
            mock_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_manage_workflow_async(self, mock_api_key):
        """Test complete Manage workflow using async client."""
        with patch('deepgram.manage.v1.models.raw_client.AsyncRawModelsClient.list') as mock_list:
            # Mock the async response
            mock_response = Mock()
            mock_response.data = ListModelsV1Response(
                models=[
                    Mock(model_id="nova-2-general", name="Nova 2 General")
                ]
            )
            mock_list.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Access nested manage functionality
            result = await client.manage.v1.models.list()
            
            assert result is not None
            assert isinstance(result, ListModelsV1Response)
            assert len(result.models) == 1
            
            # Verify the call was made
            mock_list.assert_called_once()

    def test_manage_client_property_isolation(self, mock_api_key):
        """Test that manage clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        manage1 = client1.manage
        manage2 = client2.manage
        
        # Verify they are different instances
        assert manage1 is not manage2
        assert manage1._client_wrapper is not manage2._client_wrapper
        
        # Verify nested clients are also different
        projects1 = manage1.v1.projects
        projects2 = manage2.v1.projects
        
        assert projects1 is not projects2

    def test_manage_nested_client_access(self, mock_api_key):
        """Test accessing deeply nested manage clients."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Test access to v1 clients
        manage_v1_projects = client.manage.v1.projects
        manage_v1_models = client.manage.v1.models
        
        # Verify all are properly initialized
        assert manage_v1_projects is not None
        assert manage_v1_models is not None
        
        # Verify they are different client types
        assert type(manage_v1_projects).__name__ == 'ProjectsClient'
        assert type(manage_v1_models).__name__ == 'ModelsClient'


class TestManageErrorHandling:
    """Test Manage client error handling."""

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

    @patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.list')
    def test_projects_client_api_error_handling(self, mock_list, sync_client_wrapper):
        """Test ProjectsClient API error handling."""
        # Mock an API error
        mock_list.side_effect = ApiError(
            status_code=403,
            headers={},
            body="Insufficient permissions"
        )
        
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            client.list()
        
        assert exc_info.value.status_code == 403
        assert "Insufficient permissions" in str(exc_info.value.body)

    @patch('deepgram.manage.v1.models.raw_client.AsyncRawModelsClient.get')
    @pytest.mark.asyncio
    async def test_async_models_client_api_error_handling(self, mock_get, async_client_wrapper):
        """Test AsyncModelsClient API error handling."""
        # Mock an API error
        mock_get.side_effect = ApiError(
            status_code=404,
            headers={},
            body="Model not found"
        )
        
        client = AsyncModelsClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises(ApiError) as exc_info:
            await client.get("non-existent-model")
        
        assert exc_info.value.status_code == 404
        assert "Model not found" in str(exc_info.value.body)

    @patch('deepgram.manage.v1.projects.raw_client.RawProjectsClient.get')
    def test_projects_client_network_error_handling(self, mock_get, sync_client_wrapper):
        """Test ProjectsClient network error handling."""
        # Mock a network error
        mock_get.side_effect = httpx.ConnectError("Connection failed")
        
        client = ProjectsClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises(httpx.ConnectError):
            client.get("project-123")

    def test_client_wrapper_integration(self, sync_client_wrapper):
        """Test integration with client wrapper."""
        client = ManageClient(client_wrapper=sync_client_wrapper)
        
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
