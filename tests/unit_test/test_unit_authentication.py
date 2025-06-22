# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import pytest
from unittest.mock import patch

from deepgram import DeepgramClient, DeepgramClientOptions, ClientOptionsFromEnv


class TestHeaderGeneration:
    """Test that correct Authorization headers are generated for different authentication methods"""

    def test_api_key_generates_token_header(self):
        """Test that API key generates 'Token' authorization header"""
        config = DeepgramClientOptions(api_key="test-api-key-123")
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token test-api-key-123"

    def test_access_token_generates_bearer_header(self):
        """Test that access token generates 'Bearer' authorization header"""
        config = DeepgramClientOptions(access_token="test-access-token-456")
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer test-access-token-456"

    def test_direct_client_api_key_header(self):
        """Test API key via direct client constructor"""
        client = DeepgramClient(api_key="direct-api-key")

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token direct-api-key"

    def test_direct_client_access_token_header(self):
        """Test access token via direct client constructor"""
        client = DeepgramClient(access_token="direct-access-token")

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer direct-access-token"

    @patch.dict(os.environ, {}, clear=True)
    def test_no_credentials_no_auth_header(self):
        """Test that no authorization header is set when no credentials are provided"""
        config = DeepgramClientOptions()
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == ""

    @patch.dict(os.environ, {}, clear=True)
    def test_empty_credentials_no_auth_header(self):
        """Test that empty credentials don't generate authorization headers"""
        config = DeepgramClientOptions(api_key="", access_token="")
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == ""


class TestCredentialPriority:
    """Test that API keys take precedence over access tokens for backward compatibility"""

    def test_access_token_priority_in_config(self):
        """Test API key takes priority in config object for backward compatibility"""
        config = DeepgramClientOptions(
            api_key="priority-api-key",
            access_token="should-be-ignored"
        )
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token priority-api-key"

    def test_access_token_priority_in_client_constructor(self):
        """Test API key takes priority in client constructor for backward compatibility"""
        client = DeepgramClient(
            api_key="priority-api-key",
            access_token="should-be-ignored"
        )

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token priority-api-key"

    def test_access_token_priority_mixed_sources(self):
        """Test access token priority with mixed initialization sources"""
        config = DeepgramClientOptions(api_key="config-api-key")
        client = DeepgramClient(
            access_token="param-access-token",
            config=config
        )

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer param-access-token"

    def test_api_key_used_when_no_access_token(self):
        """Test API key is used when access token is not provided"""
        client = DeepgramClient(api_key="fallback-api-key")

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token fallback-api-key"


class TestEnvironmentVariableResolution:
    """Test environment variable resolution and priority"""

    @patch.dict(os.environ, {'DEEPGRAM_ACCESS_TOKEN': 'env-access-token'}, clear=True)
    def test_access_token_env_var_priority(self):
        """Test that DEEPGRAM_ACCESS_TOKEN takes priority"""
        client = DeepgramClient()

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer env-access-token"

    @patch.dict(os.environ, {'DEEPGRAM_API_KEY': 'env-api-key'}, clear=True)
    def test_api_key_env_var_fallback(self):
        """Test that DEEPGRAM_API_KEY is used when access token is not available"""
        client = DeepgramClient()

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token env-api-key"

    @patch.dict(os.environ, {
        'DEEPGRAM_API_KEY': 'env-api-key',
        'DEEPGRAM_ACCESS_TOKEN': 'env-access-token'
    }, clear=True)
    def test_access_token_env_var_priority_over_api_key(self):
        """Test that DEEPGRAM_ACCESS_TOKEN takes priority over DEEPGRAM_API_KEY"""
        client = DeepgramClient()

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer env-access-token"

    @patch.dict(os.environ, {}, clear=True)
    def test_no_env_vars_no_auth_header(self):
        """Test that no auth header is set when no environment variables are present"""
        client = DeepgramClient()

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == ""

    @patch.dict(os.environ, {'DEEPGRAM_ACCESS_TOKEN': 'env-access-token'}, clear=True)
    def test_explicit_param_overrides_env_var(self):
        """Test that explicit parameters override environment variables"""
        client = DeepgramClient(api_key="explicit-api-key")

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token explicit-api-key"

    @patch.dict(os.environ, {'DEEPGRAM_API_KEY': 'env-api-key'}, clear=True)
    def test_explicit_access_token_overrides_env_api_key(self):
        """Test that explicit access token overrides environment API key"""
        client = DeepgramClient(access_token="explicit-access-token")

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer explicit-access-token"


class TestClientOptionsFromEnv:
    """Test ClientOptionsFromEnv class behavior"""

    @patch.dict(os.environ, {'DEEPGRAM_ACCESS_TOKEN': 'env-access-token'}, clear=True)
    def test_client_options_from_env_access_token(self):
        """Test ClientOptionsFromEnv with access token"""
        config = ClientOptionsFromEnv()
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer env-access-token"

    @patch.dict(os.environ, {'DEEPGRAM_API_KEY': 'env-api-key'}, clear=True)
    def test_client_options_from_env_api_key(self):
        """Test ClientOptionsFromEnv with API key"""
        config = ClientOptionsFromEnv()
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token env-api-key"

    @patch.dict(os.environ, {
        'DEEPGRAM_API_KEY': 'env-api-key',
        'DEEPGRAM_ACCESS_TOKEN': 'env-access-token'
    }, clear=True)
    def test_client_options_from_env_priority(self):
        """Test ClientOptionsFromEnv prioritizes access token over API key"""
        config = ClientOptionsFromEnv()
        client = DeepgramClient(config=config)

        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer env-access-token"

    @patch.dict(os.environ, {}, clear=True)
    def test_client_options_from_env_no_credentials_raises_error(self):
        """Test ClientOptionsFromEnv raises error when no credentials are available"""
        from deepgram.errors import DeepgramApiKeyError

        with pytest.raises(DeepgramApiKeyError, match="Neither Deepgram API KEY nor ACCESS TOKEN is set"):
            ClientOptionsFromEnv()


class TestAuthSwitching:
    """Test dynamic credential switching"""

    def test_switch_from_api_key_to_access_token(self):
        """Test switching from API key to access token"""
        config = DeepgramClientOptions(api_key="initial-api-key")
        client = DeepgramClient(config=config)

        # Verify initial state
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token initial-api-key"

        # Switch to access token
        client._config.set_access_token("switched-access-token")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer switched-access-token"

        # Verify API key was cleared
        assert client._config.api_key == ""

    def test_switch_from_access_token_to_api_key(self):
        """Test switching from access token to API key"""
        config = DeepgramClientOptions(access_token="initial-access-token")
        client = DeepgramClient(config=config)

        # Verify initial state
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer initial-access-token"

        # Switch to API key
        client._config.set_apikey("switched-api-key")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token switched-api-key"

        # Verify access token was cleared
        assert client._config.access_token == ""

    def test_multiple_auth_switches(self):
        """Test multiple authentication method switches"""
        config = DeepgramClientOptions(api_key="initial-api-key")
        client = DeepgramClient(config=config)

        # Initial state
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token initial-api-key"

        # Switch to access token
        client._config.set_access_token("first-access-token")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer first-access-token"

        # Switch back to API key
        client._config.set_apikey("second-api-key")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token second-api-key"

        # Switch to different access token
        client._config.set_access_token("second-access-token")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Bearer second-access-token"

    def test_switch_to_empty_credentials(self):
        """Test switching to empty credentials"""
        config = DeepgramClientOptions(api_key="initial-api-key")
        client = DeepgramClient(config=config)

        # Switch to empty access token
        client._config.set_access_token("")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == ""

        # Set API key again
        client._config.set_apikey("new-api-key")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token new-api-key"

        # Switch to empty API key
        client._config.set_apikey("")
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == ""


class TestErrorHandling:
    """Test error handling scenarios"""

    @patch.dict(os.environ, {}, clear=True)
    def test_no_credentials_warning_logged(self):
        """Test that appropriate warning is logged when no credentials are provided"""
        import logging

        with patch('deepgram.client.verboselogs.VerboseLogger') as mock_logger:
            mock_logger_instance = mock_logger.return_value
            DeepgramClient()

            # Check that warning was called
            mock_logger_instance.warning.assert_called_with(
                "WARNING: Neither API key nor access token is provided"
            )

    def test_mixed_initialization_with_config_and_params(self):
        """Test mixed initialization scenarios"""
        config = DeepgramClientOptions(api_key="config-api-key")
        client = DeepgramClient(api_key="param-api-key", config=config)

        # Parameter should override config
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token param-api-key"

    def test_config_credential_extraction(self):
        """Test credential extraction from existing config"""
        config = DeepgramClientOptions(
            api_key="config-api-key",
            access_token="config-access-token"
        )

        # No explicit credentials, should use config values
        client = DeepgramClient(config=config)

        # API key should take priority for backward compatibility
        auth_header = client._config.headers.get('Authorization', '')
        assert auth_header == "Token config-api-key"

    def test_header_preservation_across_updates(self):
        """Test that other headers are preserved during auth updates"""
        config = DeepgramClientOptions(
            api_key="test-key",
            headers={"Custom-Header": "custom-value"}
        )
        client = DeepgramClient(config=config)

        # Verify both auth and custom headers exist
        assert client._config.headers.get('Authorization') == "Token test-key"
        assert client._config.headers.get('Custom-Header') == "custom-value"
        assert client._config.headers.get('Accept') == "application/json"
        assert "User-Agent" in client._config.headers

        # Switch auth method and verify custom headers are preserved
        client._config.set_access_token("new-token")
        assert client._config.headers.get(
            'Authorization') == "Bearer new-token"
        assert client._config.headers.get('Custom-Header') == "custom-value"
        assert client._config.headers.get('Accept') == "application/json"


class TestGrantTokenWorkflow:
    """Test the complete API Key → Access Token → Bearer Auth workflow"""

    def test_api_key_to_access_token_workflow(self):
        """Test the complete workflow from API key to access token to bearer auth"""
        from unittest.mock import patch, MagicMock

        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-access-token-12345"
        mock_response.expires_in = 30

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Step 1: Create client with API key
            api_client = DeepgramClient(api_key="test-api-key")
            api_auth_header = api_client._config.headers.get(
                'Authorization', '')
            assert api_auth_header == "Token test-api-key"

            # Step 2: Use API key to fetch access token
            response = api_client.auth.v("1").grant_token()
            access_token = response.access_token
            expires_in = response.expires_in

            assert access_token == "mock-access-token-12345"
            assert expires_in == 30
            assert mock_grant_token.called

            # Step 3: Create new client with the fetched access token
            bearer_client = DeepgramClient(access_token=access_token)
            bearer_auth_header = bearer_client._config.headers.get(
                'Authorization', '')

            assert bearer_auth_header == "Bearer mock-access-token-12345"

            # Verify both clients have correct auth headers
            assert api_client._config.headers.get(
                'Authorization') == "Token test-api-key"
            assert bearer_client._config.headers.get(
                'Authorization') == "Bearer mock-access-token-12345"

    def test_grant_token_error_handling(self):
        """Test that grant_token errors are handled gracefully"""
        from unittest.mock import patch
        from deepgram.clients.common.v1.errors import DeepgramApiError

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.side_effect = DeepgramApiError(
                "Invalid credentials", 401)

            # Create client with API key
            api_client = DeepgramClient(api_key="invalid-api-key")

            # Verify initial auth header is correct
            api_auth_header = api_client._config.headers.get(
                'Authorization', '')
            assert api_auth_header == "Token invalid-api-key"

            # Attempt to get access token should raise error
            with pytest.raises(DeepgramApiError, match="Invalid credentials"):
                api_client.auth.v("1").grant_token()

    def test_access_token_client_independence(self):
        """Test that API key and access token clients work independently"""
        from unittest.mock import patch, MagicMock

        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "temporary-token-67890"
        mock_response.expires_in = 30

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create API client
            api_client = DeepgramClient(api_key="persistent-api-key")

            # Get access token
            response = api_client.auth.v("1").grant_token()
            access_token = response.access_token

            # Create bearer client
            bearer_client = DeepgramClient(access_token=access_token)

            # Modify one client - should not affect the other
            api_client._config.set_apikey("new-api-key")
            bearer_client._config.set_access_token("new-access-token")

            # Verify independence
            assert api_client._config.headers.get(
                'Authorization') == "Token new-api-key"
            assert bearer_client._config.headers.get(
                'Authorization') == "Bearer new-access-token"

            # Original tokens should be different
            assert api_client._config.api_key != bearer_client._config.access_token
