# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pytest
from unittest.mock import patch, MagicMock

from deepgram import DeepgramClient


class TestGrantTokenTTL:
    """Test the TTL functionality for grant_token"""

    def test_grant_token_default_ttl(self):
        """Test grant_token with default TTL (no ttl_seconds specified)"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-access-token-default"
        mock_response.expires_in = 30

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token without ttl_seconds
            response = api_client.auth.v("1").grant_token()

            assert response.access_token == "mock-access-token-default"
            assert response.expires_in == 30
            assert mock_grant_token.called

    def test_grant_token_custom_ttl(self):
        """Test grant_token with custom TTL values"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-access-token-custom"
        mock_response.expires_in = 300

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token with custom ttl_seconds
            response = api_client.auth.v("1").grant_token(ttl_seconds=300)

            assert response.access_token == "mock-access-token-custom"
            assert response.expires_in == 300
            assert mock_grant_token.called

    def test_grant_token_ttl_validation_valid_values(self):
        """Test that valid TTL values are accepted"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-access-token-valid"
        mock_response.expires_in = 1800

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Test valid boundary values
            valid_values = [1, 30, 300, 1800, 3600]

            for ttl in valid_values:
                response = api_client.auth.v("1").grant_token(ttl_seconds=ttl)
                assert response.access_token == "mock-access-token-valid"

    def test_grant_token_ttl_validation_invalid_values(self):
        """Test that invalid TTL values raise ValueError"""
        # Create client with mock API key
        api_client = DeepgramClient(api_key="mock-api-key")

        # Test invalid values
        invalid_values = [0, -1, 3601, 10000, "300", 30.5, None]

        for invalid_ttl in invalid_values:
            if invalid_ttl is None:
                continue  # None should be valid (default)

            with pytest.raises(ValueError, match="ttl_seconds must be an integer between 1 and 3600"):
                api_client.auth.v("1").grant_token(ttl_seconds=invalid_ttl)

    def test_grant_token_workflow_with_custom_ttl(self):
        """Test the complete workflow from API key to access token with custom TTL"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-access-token-custom-workflow"
        mock_response.expires_in = 1800

        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Step 1: Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Step 2: Use API key to fetch access token with custom TTL
            response = api_client.auth.v("1").grant_token(ttl_seconds=1800)
            access_token = response.access_token
            expires_in = response.expires_in

            assert access_token == "mock-access-token-custom-workflow"
            assert expires_in == 1800
            assert mock_grant_token.called

            # Step 3: Create new client with the fetched access token
            bearer_client = DeepgramClient(access_token=access_token)
            bearer_auth_header = bearer_client._config.headers.get(
                'Authorization', '')

            assert bearer_auth_header == "Bearer mock-access-token-custom-workflow"

            # Verify both clients have correct auth headers
            assert api_client._config.headers.get(
                'Authorization') == "Token mock-api-key"
            assert bearer_client._config.headers.get(
                'Authorization') == "Bearer mock-access-token-custom-workflow"


class TestAsyncGrantTokenTTL:
    """Test the TTL functionality for async grant_token"""

    @pytest.mark.asyncio
    async def test_async_grant_token_default_ttl(self):
        """Test async grant_token with default TTL"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-async-access-token-default"
        mock_response.expires_in = 30

        with patch('deepgram.clients.auth.v1.async_client.AsyncAuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token without ttl_seconds
            response = await api_client.asyncauth.v("1").grant_token()

            assert response.access_token == "mock-async-access-token-default"
            assert response.expires_in == 30
            assert mock_grant_token.called

    @pytest.mark.asyncio
    async def test_async_grant_token_custom_ttl(self):
        """Test async grant_token with custom TTL values"""
        # Mock the grant_token response
        mock_response = MagicMock()
        mock_response.access_token = "mock-async-access-token-custom"
        mock_response.expires_in = 600

        with patch('deepgram.clients.auth.v1.async_client.AsyncAuthRESTClient.grant_token') as mock_grant_token:
            mock_grant_token.return_value = mock_response

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token with custom ttl_seconds
            response = await api_client.asyncauth.v("1").grant_token(ttl_seconds=600)

            assert response.access_token == "mock-async-access-token-custom"
            assert response.expires_in == 600
            assert mock_grant_token.called

    @pytest.mark.asyncio
    async def test_async_grant_token_ttl_validation_invalid_values(self):
        """Test that invalid TTL values raise ValueError in async client"""
        # Create client with mock API key
        api_client = DeepgramClient(api_key="mock-api-key")

        # Test invalid values
        invalid_values = [0, -1, 3601, 10000, "300", 30.5]

        for invalid_ttl in invalid_values:
            with pytest.raises(ValueError, match="ttl_seconds must be an integer between 1 and 3600"):
                await api_client.asyncauth.v("1").grant_token(ttl_seconds=invalid_ttl)


class TestGrantTokenRequestBody:
    """Test that the request body is properly formatted for TTL requests"""

    def test_grant_token_request_body_with_ttl(self):
        """Test that ttl_seconds is properly included in the request body"""
        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.post') as mock_post:
            mock_post.return_value = '{"access_token": "test-token", "expires_in": 300}'

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token with ttl_seconds
            api_client.auth.v("1").grant_token(ttl_seconds=300)

            # Verify the post method was called with the correct parameters
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args

            # Check that json parameter contains ttl_seconds
            assert 'json' in kwargs
            assert kwargs['json'] == {'ttl_seconds': 300}

            # Check that headers contain the authorization
            assert 'headers' in kwargs
            assert kwargs['headers']['Authorization'] == "Token mock-api-key"

    def test_grant_token_request_body_without_ttl(self):
        """Test that no request body is sent when ttl_seconds is not specified"""
        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.post') as mock_post:
            mock_post.return_value = '{"access_token": "test-token", "expires_in": 30}'

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token without ttl_seconds
            api_client.auth.v("1").grant_token()

            # Verify the post method was called with the correct parameters
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args

            # Check that json parameter is not included
            assert 'json' not in kwargs

            # Check that headers contain the authorization
            assert 'headers' in kwargs
            assert kwargs['headers']['Authorization'] == "Token mock-api-key"

    @pytest.mark.asyncio
    async def test_async_grant_token_request_body_with_ttl(self):
        """Test that ttl_seconds is properly included in the async request body"""
        with patch('deepgram.clients.auth.v1.async_client.AsyncAuthRESTClient.post') as mock_post:
            mock_post.return_value = '{"access_token": "test-token", "expires_in": 600}'

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Call grant_token with ttl_seconds
            await api_client.asyncauth.v("1").grant_token(ttl_seconds=600)

            # Verify the post method was called with the correct parameters
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args

            # Check that json parameter contains ttl_seconds
            assert 'json' in kwargs
            assert kwargs['json'] == {'ttl_seconds': 600}

            # Check that headers contain the authorization
            assert 'headers' in kwargs
            assert kwargs['headers']['Authorization'] == "Token mock-api-key"


class TestGrantTokenEdgeCases:
    """Test edge cases and error conditions for grant_token"""

    def test_grant_token_boundary_values(self):
        """Test TTL boundary values (1 and 3600 seconds)"""
        with patch('deepgram.clients.auth.v1.client.AuthRESTClient.post') as mock_post:
            mock_post.return_value = '{"access_token": "test-token", "expires_in": 1}'

            # Create client with mock API key
            api_client = DeepgramClient(api_key="mock-api-key")

            # Test minimum value (1 second)
            response = api_client.auth.v("1").grant_token(ttl_seconds=1)
            assert response.access_token == "test-token"

            # Test maximum value (3600 seconds)
            mock_post.return_value = '{"access_token": "test-token", "expires_in": 3600}'
            response = api_client.auth.v("1").grant_token(ttl_seconds=3600)
            assert response.access_token == "test-token"

            # Verify both calls were made
            assert mock_post.call_count == 2

    def test_grant_token_type_validation(self):
        """Test that non-integer types raise ValueError"""
        # Create client with mock API key - validation happens before any HTTP request
        api_client = DeepgramClient(api_key="mock-api-key")

        # Test various invalid types
        invalid_types = ["300", 30.5, [300], {"ttl": 300}, True, False]

        for invalid_type in invalid_types:
            with pytest.raises(ValueError, match="ttl_seconds must be an integer between 1 and 3600"):
                # This should raise ValueError in the validation step before making any HTTP request
                api_client.auth.v("1").grant_token(ttl_seconds=invalid_type)

    def test_grant_token_range_validation(self):
        """Test that out-of-range values raise ValueError"""
        # Create client with mock API key - validation happens before any HTTP request
        api_client = DeepgramClient(api_key="mock-api-key")

        # Test values outside the valid range
        invalid_ranges = [0, -1, -100, 3601, 10000, 86400]

        for invalid_value in invalid_ranges:
            with pytest.raises(ValueError, match="ttl_seconds must be an integer between 1 and 3600"):
                # This should raise ValueError in the validation step before making any HTTP request
                api_client.auth.v("1").grant_token(ttl_seconds=invalid_value)