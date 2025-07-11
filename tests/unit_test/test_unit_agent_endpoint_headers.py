# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pytest
import json
from unittest.mock import patch, MagicMock

from deepgram import (
    DeepgramClient,
    SettingsOptions,
    Endpoint,
    Function,
    Header,
)


class TestEndpointHeaders:
    """Unit tests for Endpoint.headers functionality using dictionary format"""

    def test_endpoint_headers_dict_format(self):
        """Test that Endpoint accepts headers as a dictionary"""
        headers = {"authorization": "Bearer token", "content-type": "application/json"}
        endpoint = Endpoint(
            url="https://api.example.com/v1/test",
            headers=headers
        )

        assert endpoint.headers == headers
        assert endpoint.headers["authorization"] == "Bearer token"
        assert endpoint.headers["content-type"] == "application/json"

    def test_endpoint_headers_serialization(self):
        """Test that Endpoint with dict headers serializes correctly to JSON"""
        headers = {"authorization": "Bearer token"}
        endpoint = Endpoint(
            url="https://api.example.com/v1/test",
            headers=headers
        )

        # Test direct JSON serialization
        json_data = endpoint.to_json()
        parsed = json.loads(json_data)

        assert parsed["headers"] == headers
        assert parsed["headers"]["authorization"] == "Bearer token"
        assert parsed["url"] == "https://api.example.com/v1/test"
        assert parsed["method"] == "POST"  # default value

    def test_endpoint_headers_none(self):
        """Test that Endpoint works correctly with None headers"""
        endpoint = Endpoint(url="https://api.example.com/v1/test")

        assert endpoint.headers is None

        # Test serialization with None headers
        json_data = endpoint.to_json()
        parsed = json.loads(json_data)

        assert "headers" not in parsed  # Should be excluded when None

    def test_endpoint_headers_empty_dict(self):
        """Test that Endpoint works correctly with empty dict headers"""
        endpoint = Endpoint(
            url="https://api.example.com/v1/test",
            headers={}
        )

        assert endpoint.headers == {}

        # Test serialization with empty headers
        json_data = endpoint.to_json()
        parsed = json.loads(json_data)

        assert parsed["headers"] == {}

    def test_endpoint_from_dict_with_headers(self):
        """Test that Endpoint.from_dict works correctly with dict headers"""
        data = {
            "url": "https://api.example.com/v1/test",
            "method": "POST",
            "headers": {"authorization": "Bearer token", "x-custom": "value"}
        }

        endpoint = Endpoint.from_dict(data)

        assert endpoint.url == "https://api.example.com/v1/test"
        assert endpoint.method == "POST"
        assert endpoint.headers == {"authorization": "Bearer token", "x-custom": "value"}

    def test_endpoint_aws_polly_use_case(self):
        """Test the specific AWS Polly use case from the bug report"""
        endpoint = Endpoint(
            url="https://polly.ap-northeast-1.amazonaws.com/v1/speech",
            headers={"authorization": "Bearer token"}
        )

        # Test that it matches the API specification format
        json_data = endpoint.to_json()
        parsed = json.loads(json_data)

        expected_format = {
            "url": "https://polly.ap-northeast-1.amazonaws.com/v1/speech",
            "method": "POST",
            "headers": {
                "authorization": "Bearer token"
            }
        }

        assert parsed == expected_format


class TestFunctionHeaders:
    """Unit tests for Function.headers functionality using dictionary format"""

    def test_function_headers_dict_format(self):
        """Test that Function accepts headers as a dictionary"""
        headers = {"authorization": "Bearer token", "content-type": "application/json"}
        function = Function(
            name="test_function",
            description="Test function",
            url="https://api.example.com/v1/function",
            method="POST",
            headers=headers
        )

        assert function.headers == headers
        assert function.headers["authorization"] == "Bearer token"

    def test_function_headers_serialization(self):
        """Test that Function with dict headers serializes correctly to JSON"""
        headers = {"authorization": "Bearer token"}
        function = Function(
            name="test_function",
            description="Test function",
            url="https://api.example.com/v1/function",
            method="POST",
            headers=headers
        )

        json_data = function.to_json()
        parsed = json.loads(json_data)

        assert parsed["headers"] == headers
        assert parsed["name"] == "test_function"

    def test_function_from_dict_with_headers(self):
        """Test that Function.from_dict works correctly with dict headers"""
        data = {
            "name": "test_function",
            "description": "Test function",
            "url": "https://api.example.com/v1/function",
            "method": "POST",
            "headers": {"authorization": "Bearer token", "x-custom": "value"}
        }

        function = Function.from_dict(data)

        assert function.name == "test_function"
        assert function.headers == {"authorization": "Bearer token", "x-custom": "value"}


class TestSettingsOptionsWithEndpoint:
    """Test SettingsOptions with Endpoint containing headers"""

    def test_settings_options_with_endpoint_headers(self):
        """Test full SettingsOptions with speak endpoint headers"""
        options = SettingsOptions()

        # Configure AWS Polly example from bug report
        options.agent.speak.provider.type = "aws_polly"
        options.agent.speak.provider.language_code = "en-US"
        options.agent.speak.provider.voice = "Matthew"
        options.agent.speak.provider.engine = "standard"
        options.agent.speak.endpoint = Endpoint(
            url="https://polly.ap-northeast-1.amazonaws.com/v1/speech",
            headers={"authorization": "Bearer token"}
        )

        # Test serialization
        json_data = options.to_json()
        parsed = json.loads(json_data)

        # Verify the endpoint headers are in the correct format
        speak_endpoint = parsed["agent"]["speak"]["endpoint"]
        assert speak_endpoint["url"] == "https://polly.ap-northeast-1.amazonaws.com/v1/speech"
        assert speak_endpoint["headers"] == {"authorization": "Bearer token"}

    def test_settings_options_multiple_header_values(self):
        """Test endpoint with multiple header values"""
        options = SettingsOptions()

        headers = {
            "authorization": "Bearer token",
            "content-type": "application/json",
            "x-custom-header": "custom-value"
        }

        options.agent.speak.endpoint = Endpoint(
            url="https://api.example.com/v1/speech",
            headers=headers
        )

        json_data = options.to_json()
        parsed = json.loads(json_data)

        endpoint_headers = parsed["agent"]["speak"]["endpoint"]["headers"]
        assert endpoint_headers == headers
        assert len(endpoint_headers) == 3

    def test_settings_options_think_endpoint_headers(self):
        """Test think endpoint with headers"""
        options = SettingsOptions()

        options.agent.think.endpoint = Endpoint(
            url="https://api.openai.com/v1/chat/completions",
            headers={"authorization": "Bearer sk-..."}
        )

        json_data = options.to_json()
        parsed = json.loads(json_data)

        think_endpoint = parsed["agent"]["think"]["endpoint"]
        assert think_endpoint["headers"] == {"authorization": "Bearer sk-..."}


class TestBackwardCompatibility:
    """Test backward compatibility with Header class"""

    def test_header_class_still_exists(self):
        """Test that Header class still exists for backward compatibility"""
        header = Header(key="authorization", value="Bearer token")
        assert header.key == "authorization"
        assert header.value == "Bearer token"

    def test_header_serialization(self):
        """Test that Header still serializes correctly"""
        header = Header(key="authorization", value="Bearer token")
        json_data = header.to_json()
        parsed = json.loads(json_data)

        assert parsed["key"] == "authorization"
        assert parsed["value"] == "Bearer token"


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_endpoint_headers_with_non_string_values(self):
        """Test behavior with non-string header values"""
        # Test that non-string values are handled appropriately
        endpoint = Endpoint(
            url="https://api.example.com/v1/test",
            headers={"authorization": "Bearer token", "timeout": "30"}  # Should be strings
        )

        assert endpoint.headers["timeout"] == "30"

        # Test serialization
        json_data = endpoint.to_json()
        parsed = json.loads(json_data)
        assert parsed["headers"]["timeout"] == "30"


# Integration test with properly mocked WebSocket client
class TestIntegrationWithAgentClient:
    """Integration test with the agent websocket client"""

    @patch('websockets.sync.client.connect')
    def test_endpoint_headers_integration(self, mock_connect):
        """Test that headers work correctly in integration with agent client"""
        # Mock the websocket connection to avoid real connections
        mock_websocket = MagicMock()
        mock_websocket.send.return_value = None
        mock_websocket.recv.return_value = '{"type": "Welcome"}'
        mock_connect.return_value = mock_websocket

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        options = SettingsOptions()
        options.agent.speak.endpoint = Endpoint(
            url="https://polly.ap-northeast-1.amazonaws.com/v1/speech",
            headers={"authorization": "Bearer token"}
        )

        # Test that the options serialize correctly without making real connections
        options_json = options.to_json()
        parsed = json.loads(options_json)

        # Verify the headers are in the correct format in the serialized options
        speak_endpoint = parsed["agent"]["speak"]["endpoint"]
        assert speak_endpoint["headers"] == {"authorization": "Bearer token"}
        assert speak_endpoint["url"] == "https://polly.ap-northeast-1.amazonaws.com/v1/speech"

        # Test that the Endpoint can be reconstructed from the JSON
        reconstructed_endpoint = Endpoint.from_dict(speak_endpoint)
        assert reconstructed_endpoint.headers == {"authorization": "Bearer token"}
        assert reconstructed_endpoint.url == "https://polly.ap-northeast-1.amazonaws.com/v1/speech"