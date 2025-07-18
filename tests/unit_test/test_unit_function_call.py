# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pytest
import json
from unittest.mock import patch, MagicMock

from deepgram import (
    DeepgramClient,
    FunctionCall,
    FunctionCallRequest,
    FunctionCallResponse,
)


class TestFunctionCall:
    """Unit tests for FunctionCall class"""

    def test_function_call_creation(self):
        """Test creating a FunctionCall object"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        assert function_call.id == "func_12345"
        assert function_call.name == "get_weather"
        assert function_call.arguments == '{"location": "New York", "unit": "fahrenheit"}'
        assert function_call.client_side is True

    def test_function_call_serialization(self):
        """Test FunctionCall JSON serialization"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        result = json.loads(function_call.to_json())
        expected = {
            "id": "func_12345",
            "name": "get_weather",
            "arguments": '{"location": "New York", "unit": "fahrenheit"}',
            "client_side": True
        }
        assert result == expected

    def test_function_call_deserialization(self):
        """Test FunctionCall JSON deserialization"""
        data = {
            "id": "func_12345",
            "name": "get_weather",
            "arguments": '{"location": "New York", "unit": "fahrenheit"}',
            "client_side": True
        }

        function_call = FunctionCall.from_dict(data)
        assert function_call.id == "func_12345"
        assert function_call.name == "get_weather"
        assert function_call.arguments == '{"location": "New York", "unit": "fahrenheit"}'
        assert function_call.client_side is True

    def test_function_call_getitem(self):
        """Test FunctionCall __getitem__ method"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        assert function_call["id"] == "func_12345"
        assert function_call["name"] == "get_weather"
        assert function_call["arguments"] == '{"location": "New York", "unit": "fahrenheit"}'
        assert function_call["client_side"] is True


class TestFunctionCallRequest:
    """Unit tests for FunctionCallRequest class"""

    def test_function_call_request_creation(self):
        """Test creating a FunctionCallRequest object"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call]
        )

        assert request.type == "FunctionCallRequest"
        assert len(request.functions) == 1
        assert request.functions[0].id == "func_12345"
        assert request.functions[0].name == "get_weather"

    def test_function_call_request_multiple_functions(self):
        """Test FunctionCallRequest with multiple functions"""
        function_call1 = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        function_call2 = FunctionCall(
            id="func_67890",
            name="get_time",
            arguments='{"timezone": "EST"}',
            client_side=False
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call1, function_call2]
        )

        assert request.type == "FunctionCallRequest"
        assert len(request.functions) == 2
        assert request.functions[0].id == "func_12345"
        assert request.functions[1].id == "func_67890"

    def test_function_call_request_serialization(self):
        """Test FunctionCallRequest JSON serialization"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call]
        )

        result = json.loads(request.to_json())
        expected = {
            "type": "FunctionCallRequest",
            "functions": [
                {
                    "id": "func_12345",
                    "name": "get_weather",
                    "arguments": '{"location": "New York", "unit": "fahrenheit"}',
                    "client_side": True
                }
            ]
        }
        assert result == expected

    def test_function_call_request_deserialization(self):
        """Test FunctionCallRequest JSON deserialization"""
        data = {
            "type": "FunctionCallRequest",
            "functions": [
                {
                    "id": "func_12345",
                    "name": "get_weather",
                    "arguments": '{"location": "New York", "unit": "fahrenheit"}',
                    "client_side": True
                }
            ]
        }

        request = FunctionCallRequest.from_dict(data)
        assert request.type == "FunctionCallRequest"
        assert len(request.functions) == 1
        assert isinstance(request.functions[0], FunctionCall)
        assert request.functions[0].id == "func_12345"
        assert request.functions[0].name == "get_weather"

    def test_function_call_request_getitem(self):
        """Test FunctionCallRequest __getitem__ method"""
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call]
        )

        assert request["type"] == "FunctionCallRequest"
        functions = request["functions"]
        assert len(functions) == 1
        assert isinstance(functions[0], FunctionCall)
        assert functions[0].id == "func_12345"

    def test_function_call_request_from_json(self):
        """Test FunctionCallRequest from_json method"""
        json_data = '''{
            "type": "FunctionCallRequest",
            "functions": [
                {
                    "id": "func_12345",
                    "name": "get_weather",
                    "arguments": "{\\"location\\": \\"New York\\", \\"unit\\": \\"fahrenheit\\"}",
                    "client_side": true
                }
            ]
        }'''

        request = FunctionCallRequest.from_json(json_data)
        assert request.type == "FunctionCallRequest"
        assert len(request.functions) == 1
        assert request.functions[0].id == "func_12345"
        assert request.functions[0].name == "get_weather"
        assert request.functions[0].client_side is True

    def test_function_call_request_post_init_dict_conversion(self):
        """Test that __post_init__ converts dict functions to FunctionCall objects"""
        # Create request with dict functions (simulating deserialization)
        dict_functions = [
            {
                "id": "func_12345",
                "name": "get_weather",
                "arguments": '{"location": "New York", "unit": "fahrenheit"}',
                "client_side": True
            },
            {
                "id": "func_67890",
                "name": "get_time",
                "arguments": '{"timezone": "EST"}',
                "client_side": False
            }
        ]

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=dict_functions
        )

        # After __post_init__, functions should be FunctionCall objects
        assert len(request.functions) == 2
        assert isinstance(request.functions[0], FunctionCall)
        assert isinstance(request.functions[1], FunctionCall)
        assert request.functions[0].id == "func_12345"
        assert request.functions[0].name == "get_weather"
        assert request.functions[1].id == "func_67890"
        assert request.functions[1].name == "get_time"

    def test_function_call_request_post_init_mixed_types(self):
        """Test that __post_init__ handles mixed dict and FunctionCall objects"""
        function_call_obj = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York", "unit": "fahrenheit"}',
            client_side=True
        )

        dict_function = {
            "id": "func_67890",
            "name": "get_time",
            "arguments": '{"timezone": "EST"}',
            "client_side": False
        }

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call_obj, dict_function]
        )

        # After __post_init__, all should be FunctionCall objects
        assert len(request.functions) == 2
        assert isinstance(request.functions[0], FunctionCall)
        assert isinstance(request.functions[1], FunctionCall)
        assert request.functions[0].id == "func_12345"
        assert request.functions[1].id == "func_67890"


class TestFunctionCallResponse:
    """Unit tests for FunctionCallResponse class"""

    def test_function_call_response_creation(self):
        """Test creating a FunctionCallResponse object"""
        response = FunctionCallResponse(
            id="func_12345",
            name="get_weather",
            content="The weather in New York is sunny with a temperature of 75°F."
        )

        assert response.type == "FunctionCallResponse"  # default value
        assert response.id == "func_12345"
        assert response.name == "get_weather"
        assert response.content == "The weather in New York is sunny with a temperature of 75°F."

    def test_function_call_response_defaults(self):
        """Test FunctionCallResponse with default values"""
        response = FunctionCallResponse()

        assert response.type == "FunctionCallResponse"
        assert response.id == ""
        assert response.name == ""
        assert response.content == ""

    def test_function_call_response_serialization(self):
        """Test FunctionCallResponse JSON serialization"""
        response = FunctionCallResponse(
            id="func_12345",
            name="get_weather",
            content="The weather in New York is sunny with a temperature of 75°F."
        )

        result = json.loads(response.to_json())
        expected = {
            "type": "FunctionCallResponse",
            "id": "func_12345",
            "name": "get_weather",
            "content": "The weather in New York is sunny with a temperature of 75°F."
        }
        assert result == expected

    def test_function_call_response_deserialization(self):
        """Test FunctionCallResponse JSON deserialization"""
        data = {
            "type": "FunctionCallResponse",
            "id": "func_12345",
            "name": "get_weather",
            "content": "The weather in New York is sunny with a temperature of 75°F."
        }

        response = FunctionCallResponse.from_dict(data)
        assert response.type == "FunctionCallResponse"
        assert response.id == "func_12345"
        assert response.name == "get_weather"
        assert response.content == "The weather in New York is sunny with a temperature of 75°F."

    def test_function_call_response_getitem(self):
        """Test FunctionCallResponse __getitem__ method"""
        response = FunctionCallResponse(
            id="func_12345",
            name="get_weather",
            content="The weather in New York is sunny with a temperature of 75°F."
        )

        assert response["type"] == "FunctionCallResponse"
        assert response["id"] == "func_12345"
        assert response["name"] == "get_weather"
        assert response["content"] == "The weather in New York is sunny with a temperature of 75°F."


class TestFunctionCallIntegration:
    """Integration tests for function call functionality"""

    def test_official_specification_compliance(self):
        """Test that the implementation matches the official specification"""
        # Test FunctionCallRequest structure
        function_call = FunctionCall(
            id="unique_id_123",
            name="calculate_sum",
            arguments='{"a": 5, "b": 3}',
            client_side=True
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call]
        )

        # Verify required fields are present
        assert hasattr(request, 'type')
        assert hasattr(request, 'functions')
        assert isinstance(request.functions, list)
        assert len(request.functions) > 0

        # Verify function structure
        func = request.functions[0]
        assert hasattr(func, 'id')
        assert hasattr(func, 'name')
        assert hasattr(func, 'arguments')
        assert hasattr(func, 'client_side')

        # Test FunctionCallResponse structure
        response = FunctionCallResponse(
            id="unique_id_123",
            name="calculate_sum",
            content="8"
        )

        # Verify required fields are present
        assert hasattr(response, 'type')
        assert hasattr(response, 'id')
        assert hasattr(response, 'name')
        assert hasattr(response, 'content')

    def test_backward_compatibility_check(self):
        """Test that old field names are no longer used"""
        # Ensure old FunctionCallRequest fields are not present
        function_call = FunctionCall(
            id="func_12345",
            name="get_weather",
            arguments='{"location": "New York"}',
            client_side=True
        )

        request = FunctionCallRequest(
            type="FunctionCallRequest",
            functions=[function_call]
        )

        # Old fields should not exist
        assert not hasattr(request, 'function_name')
        assert not hasattr(request, 'function_call_id')
        assert not hasattr(request, 'input')

        # Ensure old FunctionCallResponse fields are not present
        response = FunctionCallResponse(
            id="func_12345",
            name="get_weather",
            content="Sunny, 75°F"
        )

        # Old fields should not exist
        assert not hasattr(response, 'function_call_id')
        assert not hasattr(response, 'output')

    @patch('deepgram.clients.agent.v1.websocket.client.AgentWebSocketClient.send')
    def test_websocket_integration(self, mock_send):
        """Test that FunctionCallResponse can be sent via WebSocket"""
        mock_send.return_value = True

        client = DeepgramClient("fake-key")
        connection = client.agent.websocket.v("1")

        response = FunctionCallResponse(
            id="func_12345",
            name="get_weather",
            content="The weather in New York is sunny with a temperature of 75°F."
        )

        # This should work without errors - send using the generic send method
        result = connection.send(response.to_json())
        assert result is True
        mock_send.assert_called_once_with(response.to_json())

    def test_real_world_scenario(self):
        """Test a real-world function call scenario"""
        # Simulate receiving a function call request
        request_json = '''{
            "type": "FunctionCallRequest",
            "functions": [
                {
                    "id": "weather_12345",
                    "name": "get_current_weather",
                    "arguments": "{\\"location\\": \\"San Francisco\\", \\"unit\\": \\"celsius\\"}",
                    "client_side": true
                },
                {
                    "id": "time_67890",
                    "name": "get_current_time",
                    "arguments": "{\\"timezone\\": \\"PST\\"}",
                    "client_side": false
                }
            ]
        }'''

        # Parse the request
        request = FunctionCallRequest.from_json(request_json)

        # Verify we can access the functions
        assert len(request.functions) == 2

        weather_func = request.functions[0]
        assert weather_func.id == "weather_12345"
        assert weather_func.name == "get_current_weather"
        assert weather_func.client_side is True

        time_func = request.functions[1]
        assert time_func.id == "time_67890"
        assert time_func.name == "get_current_time"
        assert time_func.client_side is False

        # Simulate processing and creating responses
        weather_response = FunctionCallResponse(
            id="weather_12345",
            name="get_current_weather",
            content="The current weather in San Francisco is 18°C and cloudy."
        )

        time_response = FunctionCallResponse(
            id="time_67890",
            name="get_current_time",
            content="The current time in PST is 2:30 PM."
        )

        # Verify responses can be serialized
        weather_json = weather_response.to_json()
        time_json = time_response.to_json()

        # Verify they can be parsed back
        parsed_weather = FunctionCallResponse.from_json(weather_json)
        parsed_time = FunctionCallResponse.from_json(time_json)

        assert parsed_weather.id == "weather_12345"
        assert parsed_weather.content == "The current weather in San Francisco is 18°C and cloudy."
        assert parsed_time.id == "time_67890"
        assert parsed_time.content == "The current time in PST is 2:30 PM."


if __name__ == "__main__":
    pytest.main([__file__])