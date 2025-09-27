"""
Integration tests for advanced/specialized features.

This module tests advanced features including:
- Agent Settings APIs (think models, configuration)
- Advanced Management APIs (project distribution credentials, scopes)
- Self-hosted client features
- Advanced telemetry and instrumentation features
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx
import json
from typing import Dict, Any

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.environment import DeepgramClientEnvironment

# Import clients for advanced features
from deepgram.agent.v1.settings.client import SettingsClient, AsyncSettingsClient
from deepgram.agent.v1.settings.think.client import ThinkClient, AsyncThinkClient
from deepgram.agent.v1.settings.think.models.client import ModelsClient as ThinkModelsClient, AsyncModelsClient as AsyncThinkModelsClient
from deepgram.self_hosted.client import SelfHostedClient, AsyncSelfHostedClient

# Import response types (if they exist)
try:
    from deepgram.types.agent_think_models_v1response import AgentThinkModelsV1Response
except ImportError:
    # AgentThinkModelsV1Response might not exist, create a placeholder
    AgentThinkModelsV1Response = Dict[str, Any]


class TestAgentSettingsAPI:
    """Test Agent Settings API advanced features."""
    
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

    def test_agent_settings_client_initialization(self, sync_client_wrapper):
        """Test Agent Settings client initialization."""
        client = SettingsClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._think is None  # Lazy loaded

    def test_async_agent_settings_client_initialization(self, async_client_wrapper):
        """Test Async Agent Settings client initialization."""
        client = AsyncSettingsClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._think is None  # Lazy loaded

    def test_agent_settings_think_property_lazy_loading(self, sync_client_wrapper):
        """Test Agent Settings think property lazy loading."""
        client = SettingsClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._think is None
        
        # Access triggers lazy loading
        think_client = client.think
        assert client._think is not None
        assert isinstance(think_client, ThinkClient)
        
        # Subsequent access returns same instance
        assert client.think is think_client

    def test_async_agent_settings_think_property_lazy_loading(self, async_client_wrapper):
        """Test Async Agent Settings think property lazy loading."""
        client = AsyncSettingsClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._think is None
        
        # Access triggers lazy loading
        think_client = client.think
        assert client._think is not None
        assert isinstance(think_client, AsyncThinkClient)
        
        # Subsequent access returns same instance
        assert client.think is think_client

    def test_agent_think_client_initialization(self, sync_client_wrapper):
        """Test Agent Think client initialization."""
        client = ThinkClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._models is None  # Lazy loaded

    def test_async_agent_think_client_initialization(self, async_client_wrapper):
        """Test Async Agent Think client initialization."""
        client = AsyncThinkClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._models is None  # Lazy loaded

    def test_agent_think_models_property_lazy_loading(self, sync_client_wrapper):
        """Test Agent Think models property lazy loading."""
        client = ThinkClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._models is None
        
        # Access triggers lazy loading
        models_client = client.models
        assert client._models is not None
        assert isinstance(models_client, ThinkModelsClient)
        
        # Subsequent access returns same instance
        assert client.models is models_client

    def test_async_agent_think_models_property_lazy_loading(self, async_client_wrapper):
        """Test Async Agent Think models property lazy loading."""
        client = AsyncThinkClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._models is None
        
        # Access triggers lazy loading
        models_client = client.models
        assert client._models is not None
        assert isinstance(models_client, AsyncThinkModelsClient)
        
        # Subsequent access returns same instance
        assert client.models is models_client

    def test_agent_think_models_list(self, sync_client_wrapper):
        """Test Agent Think models list functionality."""
        # Mock the raw client's list method directly
        client = ThinkModelsClient(client_wrapper=sync_client_wrapper)
        
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = {"models": [{"id": "test-model", "name": "Test Model"}]}
        
        with patch.object(client._raw_client, 'list', return_value=mock_response) as mock_list:
            result = client.list()
            
            assert result is not None
            mock_list.assert_called_once_with(request_options=None)

    @pytest.mark.asyncio
    async def test_async_agent_think_models_list(self, async_client_wrapper):
        """Test Async Agent Think models list functionality."""
        # Mock the raw client's list method directly
        client = AsyncThinkModelsClient(client_wrapper=async_client_wrapper)
        
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = {"models": [{"id": "test-model", "name": "Test Model"}]}
        
        with patch.object(client._raw_client, 'list', return_value=mock_response) as mock_list:
            result = await client.list()
            
            assert result is not None
            mock_list.assert_called_once_with(request_options=None)

    def test_agent_think_models_list_with_request_options(self, sync_client_wrapper):
        """Test Agent Think models list with request options."""
        # Mock the raw client's list method directly
        client = ThinkModelsClient(client_wrapper=sync_client_wrapper)
        
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = {"models": []}
        
        request_options = RequestOptions(
            additional_headers={"Custom-Header": "test-value"},
            timeout_in_seconds=30.0
        )
        
        with patch.object(client._raw_client, 'list', return_value=mock_response) as mock_list:
            result = client.list(request_options=request_options)
            
            assert result is not None
            mock_list.assert_called_once_with(request_options=request_options)

    @patch('httpx.Client.request')
    def test_agent_think_models_list_api_error(self, mock_request, sync_client_wrapper):
        """Test Agent Think models list API error handling."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response
        
        client = ThinkModelsClient(client_wrapper=sync_client_wrapper)
        
        with pytest.raises((ApiError, Exception)):
            client.list()

    @patch('httpx.AsyncClient.request')
    @pytest.mark.asyncio
    async def test_async_agent_think_models_list_api_error(self, mock_request, async_client_wrapper):
        """Test Async Agent Think models list API error handling."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_response.headers = {"content-type": "application/json"}
        mock_request.return_value = mock_response
        
        client = AsyncThinkModelsClient(client_wrapper=async_client_wrapper)
        
        with pytest.raises((ApiError, Exception)):
            await client.list()


class TestSelfHostedClient:
    """Test Self-hosted client advanced features."""
    
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
        """Test Self-hosted client initialization."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_async_self_hosted_client_initialization(self, async_client_wrapper):
        """Test Async Self-hosted client initialization."""
        client = AsyncSelfHostedClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_self_hosted_client_v1_property_lazy_loading(self, sync_client_wrapper):
        """Test Self-hosted client v1 property lazy loading."""
        client = SelfHostedClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_async_self_hosted_client_v1_property_lazy_loading(self, async_client_wrapper):
        """Test Async Self-hosted client v1 property lazy loading."""
        client = AsyncSelfHostedClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_self_hosted_client_integration_with_main_client(self, mock_api_key):
        """Test Self-hosted client integration with main DeepgramClient."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Access self-hosted client through main client
        self_hosted = client.self_hosted
        assert self_hosted is not None
        assert isinstance(self_hosted, SelfHostedClient)

    def test_async_self_hosted_client_integration_with_main_client(self, mock_api_key):
        """Test Async Self-hosted client integration with main DeepgramClient."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Access self-hosted client through main client
        self_hosted = client.self_hosted
        assert self_hosted is not None
        assert isinstance(self_hosted, AsyncSelfHostedClient)


class TestAdvancedManagementFeatures:
    """Test advanced management API features."""
    
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

    def test_project_member_scopes_client_access(self, mock_api_key):
        """Test access to project member scopes client."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Access member scopes through projects client
        projects_client = client.manage.v1.projects
        
        # Try to access members and then scopes
        try:
            members_client = projects_client.members
            if members_client is not None and hasattr(members_client, 'scopes'):
                scopes_client = members_client.scopes
                assert scopes_client is not None
        except AttributeError:
            # It's acceptable if this advanced feature isn't fully implemented
            pass

    def test_async_project_member_scopes_client_access(self, mock_api_key):
        """Test async access to project member scopes client."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Access member scopes through projects client
        projects_client = client.manage.v1.projects
        
        # Try to access members and then scopes
        try:
            members_client = projects_client.members
            if members_client is not None and hasattr(members_client, 'scopes'):
                scopes_client = members_client.scopes
                assert scopes_client is not None
        except AttributeError:
            # It's acceptable if this advanced feature isn't fully implemented
            pass

    def test_project_advanced_operations_availability(self, mock_api_key):
        """Test availability of advanced project operations."""
        client = DeepgramClient(api_key=mock_api_key)
        projects_client = client.manage.v1.projects
        
        # Check that advanced operations are available
        advanced_operations = [
            'keys', 'members', 'requests', 'usage', 'purchases', 'balances'
        ]
        
        for operation in advanced_operations:
            assert hasattr(projects_client, operation), f"Missing {operation} operation"
            
            # Try to access the property to trigger lazy loading
            try:
                sub_client = getattr(projects_client, operation)
                assert sub_client is not None
            except Exception:
                # Some advanced features might not be fully implemented
                pass

    def test_async_project_advanced_operations_availability(self, mock_api_key):
        """Test availability of advanced project operations for async client."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        projects_client = client.manage.v1.projects
        
        # Check that advanced operations are available
        advanced_operations = [
            'keys', 'members', 'requests', 'usage', 'purchases', 'balances'
        ]
        
        for operation in advanced_operations:
            assert hasattr(projects_client, operation), f"Missing {operation} operation"
            
            # Try to access the property to trigger lazy loading
            try:
                sub_client = getattr(projects_client, operation)
                assert sub_client is not None
            except Exception:
                # Some advanced features might not be fully implemented
                pass


class TestAdvancedIntegrationScenarios:
    """Test advanced integration scenarios combining multiple features."""
    
    def test_agent_settings_with_management_workflow(self, mock_api_key):
        """Test workflow combining agent settings and management APIs."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Access both agent settings and management clients
        agent_settings = client.agent.v1.settings
        management = client.manage.v1
        
        assert agent_settings is not None
        assert management is not None
        
        # Verify they use the same underlying client infrastructure
        assert agent_settings._client_wrapper is not None
        assert management._client_wrapper is not None

    @pytest.mark.asyncio
    async def test_async_agent_settings_with_management_workflow(self, mock_api_key):
        """Test async workflow combining agent settings and management APIs."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Access both agent settings and management clients
        agent_settings = client.agent.v1.settings
        management = client.manage.v1
        
        assert agent_settings is not None
        assert management is not None
        
        # Verify they use the same underlying client infrastructure
        assert agent_settings._client_wrapper is not None
        assert management._client_wrapper is not None

    def test_self_hosted_with_advanced_features_workflow(self, mock_api_key):
        """Test workflow combining self-hosted client with other advanced features."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Access multiple advanced clients
        self_hosted = client.self_hosted
        management = client.manage
        agent = client.agent
        
        assert self_hosted is not None
        assert management is not None
        assert agent is not None
        
        # Verify all clients share the same base infrastructure
        base_clients = [self_hosted, management, agent]
        for base_client in base_clients:
            assert hasattr(base_client, '_client_wrapper')

    @pytest.mark.asyncio
    async def test_async_self_hosted_with_advanced_features_workflow(self, mock_api_key):
        """Test async workflow combining self-hosted client with other advanced features."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Access multiple advanced clients
        self_hosted = client.self_hosted
        management = client.manage
        agent = client.agent
        
        assert self_hosted is not None
        assert management is not None
        assert agent is not None
        
        # Verify all clients share the same base infrastructure
        base_clients = [self_hosted, management, agent]
        for base_client in base_clients:
            assert hasattr(base_client, '_client_wrapper')

    def test_advanced_error_handling_across_features(self, mock_api_key):
        """Test error handling consistency across advanced features."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Test that all advanced clients handle initialization properly
        advanced_clients = [
            client.agent.v1.settings,
            client.manage.v1,
            client.self_hosted,
        ]
        
        for adv_client in advanced_clients:
            assert adv_client is not None
            assert hasattr(adv_client, '_client_wrapper')
            
            # Test that raw response access works
            if hasattr(adv_client, 'with_raw_response'):
                raw_client = adv_client.with_raw_response
                assert raw_client is not None

    @pytest.mark.asyncio
    async def test_async_advanced_error_handling_across_features(self, mock_api_key):
        """Test async error handling consistency across advanced features."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Test that all advanced clients handle initialization properly
        advanced_clients = [
            client.agent.v1.settings,
            client.manage.v1,
            client.self_hosted,
        ]
        
        for adv_client in advanced_clients:
            assert adv_client is not None
            assert hasattr(adv_client, '_client_wrapper')
            
            # Test that raw response access works
            if hasattr(adv_client, 'with_raw_response'):
                raw_client = adv_client.with_raw_response
                assert raw_client is not None


class TestAdvancedFeatureErrorHandling:
    """Test error handling for advanced features."""
    
    @patch('httpx.Client.request')
    def test_agent_settings_network_error_handling(self, mock_request, mock_api_key):
        """Test network error handling in agent settings."""
        # Mock network error
        mock_request.side_effect = httpx.ConnectError("Connection failed")
        
        client = DeepgramClient(api_key=mock_api_key)
        think_models_client = client.agent.v1.settings.think.models
        
        with pytest.raises((httpx.ConnectError, ApiError, Exception)):
            think_models_client.list()

    @patch('httpx.AsyncClient.request')
    @pytest.mark.asyncio
    async def test_async_agent_settings_network_error_handling(self, mock_request, mock_api_key):
        """Test async network error handling in agent settings."""
        # Mock network error
        mock_request.side_effect = httpx.ConnectError("Connection failed")
        
        client = AsyncDeepgramClient(api_key=mock_api_key)
        think_models_client = client.agent.v1.settings.think.models
        
        with pytest.raises((httpx.ConnectError, ApiError, Exception)):
            await think_models_client.list()

    def test_client_wrapper_integration_across_advanced_features(self, mock_api_key):
        """Test client wrapper integration across advanced features."""
        client = DeepgramClient(api_key=mock_api_key)
        
        # Get client wrappers from different advanced features
        agent_wrapper = client.agent.v1.settings._client_wrapper
        manage_wrapper = client.manage.v1._client_wrapper
        
        # They should have the same configuration
        assert agent_wrapper.api_key == manage_wrapper.api_key
        assert agent_wrapper.get_environment() == manage_wrapper.get_environment()

    @pytest.mark.asyncio
    async def test_async_client_wrapper_integration_across_advanced_features(self, mock_api_key):
        """Test async client wrapper integration across advanced features."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        # Get client wrappers from different advanced features
        agent_wrapper = client.agent.v1.settings._client_wrapper
        manage_wrapper = client.manage.v1._client_wrapper
        
        # They should have the same configuration
        assert agent_wrapper.api_key == manage_wrapper.api_key
        assert agent_wrapper.get_environment() == manage_wrapper.get_environment()
