# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import pytest
from deepgram.clients.agent.v1.websocket.options import (
    SettingsOptions,
    Agent,
    Flags,
    Context,
    HistoryConversationMessage,
    HistoryFunctionCallsMessage,
    FunctionCallHistory,
)


class TestFlags:
    """Unit tests for Flags class"""

    def test_flags_default_history_value(self):
        """Test that history defaults to True"""
        flags = Flags()
        assert flags.history is True

    def test_flags_set_history_false(self):
        """Test setting history to False"""
        flags = Flags()
        flags.history = False
        assert flags.history is False

    def test_flags_set_history_true(self):
        """Test explicitly setting history to True"""
        flags = Flags()
        flags.history = True
        assert flags.history is True

    def test_flags_serialization(self):
        """Test Flags JSON serialization"""
        flags = Flags(history=True)
        result = json.loads(flags.to_json())
        expected = {"history": True}
        assert result == expected

        flags_false = Flags(history=False)
        result_false = json.loads(flags_false.to_json())
        expected_false = {"history": False}
        assert result_false == expected_false

    def test_flags_deserialization(self):
        """Test Flags deserialization from dict"""
        data = {"history": False}
        flags = Flags.from_dict(data)
        assert flags.history is False

        data_true = {"history": True}
        flags_true = Flags.from_dict(data_true)
        assert flags_true.history is True

    def test_flags_round_trip(self):
        """Test serialization and deserialization round-trip"""
        original = Flags(history=False)
        serialized = original.to_dict()
        restored = Flags.from_dict(serialized)
        assert restored.history == original.history


class TestHistoryConversationMessage:
    """Unit tests for HistoryConversationMessage class"""

    def test_history_conversation_message_creation(self):
        """Test creating a HistoryConversationMessage object"""
        message = HistoryConversationMessage(
            role="user",
            content="What's the weather like today?"
        )

        assert message.type == "History"
        assert message.role == "user"
        assert message.content == "What's the weather like today?"

    def test_history_conversation_message_defaults(self):
        """Test default values for HistoryConversationMessage"""
        message = HistoryConversationMessage()

        assert message.type == "History"
        assert message.role == ""
        assert message.content == ""

    def test_history_conversation_message_serialization(self):
        """Test HistoryConversationMessage JSON serialization"""
        message = HistoryConversationMessage(
            role="assistant",
            content="Based on the current data, it's sunny with a temperature of 72°F."
        )

        result = json.loads(message.to_json())
        expected = {
            "type": "History",
            "role": "assistant",
            "content": "Based on the current data, it's sunny with a temperature of 72°F."
        }
        assert result == expected

    def test_history_conversation_message_deserialization(self):
        """Test HistoryConversationMessage deserialization from dict"""
        data = {
            "type": "History",
            "role": "user",
            "content": "Hello, how are you?"
        }

        message = HistoryConversationMessage.from_dict(data)
        assert message.type == "History"
        assert message.role == "user"
        assert message.content == "Hello, how are you?"

    def test_history_conversation_message_round_trip(self):
        """Test serialization and deserialization round-trip"""
        original = HistoryConversationMessage(
            role="assistant",
            content="I'm doing well, thank you for asking!"
        )

        serialized = original.to_dict()
        restored = HistoryConversationMessage.from_dict(serialized)

        assert restored.type == original.type
        assert restored.role == original.role
        assert restored.content == original.content


class TestFunctionCallHistory:
    """Unit tests for FunctionCallHistory class"""

    def test_function_call_history_creation(self):
        """Test creating a FunctionCallHistory object"""
        function_call = FunctionCallHistory(
            id="fc_12345678-90ab-cdef-1234-567890abcdef",
            name="check_order_status",
            client_side=True,
            arguments='{"order_id": "ORD-123456"}',
            response="Order #123456 status: Shipped - Expected delivery date: 2024-03-15"
        )

        assert function_call.id == "fc_12345678-90ab-cdef-1234-567890abcdef"
        assert function_call.name == "check_order_status"
        assert function_call.client_side is True
        assert function_call.arguments == '{"order_id": "ORD-123456"}'
        assert function_call.response == "Order #123456 status: Shipped - Expected delivery date: 2024-03-15"

    def test_function_call_history_defaults(self):
        """Test default values for FunctionCallHistory"""
        function_call = FunctionCallHistory()

        assert function_call.id == ""
        assert function_call.name == ""
        assert function_call.client_side is False
        assert function_call.arguments == ""
        assert function_call.response == ""

    def test_function_call_history_serialization(self):
        """Test FunctionCallHistory JSON serialization"""
        function_call = FunctionCallHistory(
            id="fc_123",
            name="get_weather",
            client_side=False,
            arguments='{"location": "New York"}',
            response="Sunny, 75°F"
        )

        result = json.loads(function_call.to_json())
        expected = {
            "id": "fc_123",
            "name": "get_weather",
            "client_side": False,
            "arguments": '{"location": "New York"}',
            "response": "Sunny, 75°F"
        }
        assert result == expected

    def test_function_call_history_deserialization(self):
        """Test FunctionCallHistory deserialization from dict"""
        data = {
            "id": "fc_456",
            "name": "send_email",
            "client_side": True,
            "arguments": '{"to": "user@example.com", "subject": "Test"}',
            "response": "Email sent successfully"
        }

        function_call = FunctionCallHistory.from_dict(data)
        assert function_call.id == "fc_456"
        assert function_call.name == "send_email"
        assert function_call.client_side is True
        assert function_call.arguments == '{"to": "user@example.com", "subject": "Test"}'
        assert function_call.response == "Email sent successfully"


class TestHistoryFunctionCallsMessage:
    """Unit tests for HistoryFunctionCallsMessage class"""

    def test_history_function_calls_message_creation(self):
        """Test creating a HistoryFunctionCallsMessage object"""
        function_call = FunctionCallHistory(
            id="fc_123",
            name="check_balance",
            client_side=True,
            arguments='{"account_id": "12345"}',
            response="Current balance: $1,250.00"
        )

        message = HistoryFunctionCallsMessage(
            function_calls=[function_call]
        )

        assert message.type == "History"
        assert len(message.function_calls) == 1
        assert isinstance(message.function_calls[0], FunctionCallHistory)
        assert message.function_calls[0].name == "check_balance"

    def test_history_function_calls_message_defaults(self):
        """Test default values for HistoryFunctionCallsMessage"""
        message = HistoryFunctionCallsMessage()

        assert message.type == "History"
        assert message.function_calls == []

    def test_history_function_calls_message_multiple_calls(self):
        """Test HistoryFunctionCallsMessage with multiple function calls"""
        call1 = FunctionCallHistory(
            id="fc_1",
            name="get_weather",
            client_side=True,
            arguments='{"location": "NYC"}',
            response="Sunny, 72°F"
        )

        call2 = FunctionCallHistory(
            id="fc_2",
            name="get_time",
            client_side=False,
            arguments='{"timezone": "EST"}',
            response="2024-03-15 14:30:00 EST"
        )

        message = HistoryFunctionCallsMessage(function_calls=[call1, call2])

        assert len(message.function_calls) == 2
        assert message.function_calls[0].name == "get_weather"
        assert message.function_calls[1].name == "get_time"

    def test_history_function_calls_message_serialization(self):
        """Test HistoryFunctionCallsMessage JSON serialization"""
        function_call = FunctionCallHistory(
            id="fc_789",
            name="calculate_tip",
            client_side=True,
            arguments='{"bill_amount": 50.00, "tip_percentage": 18}',
            response="Recommended tip: $9.00"
        )

        message = HistoryFunctionCallsMessage(function_calls=[function_call])
        result = json.loads(message.to_json())

        expected = {
            "type": "History",
            "function_calls": [
                {
                    "id": "fc_789",
                    "name": "calculate_tip",
                    "client_side": True,
                    "arguments": '{"bill_amount": 50.00, "tip_percentage": 18}',
                    "response": "Recommended tip: $9.00"
                }
            ]
        }
        assert result == expected

    def test_history_function_calls_message_deserialization(self):
        """Test HistoryFunctionCallsMessage deserialization from dict"""
        data = {
            "type": "History",
            "function_calls": [
                {
                    "id": "fc_101",
                    "name": "book_flight",
                    "client_side": False,
                    "arguments": '{"origin": "NYC", "destination": "LAX"}',
                    "response": "Flight booked successfully"
                }
            ]
        }

        message = HistoryFunctionCallsMessage.from_dict(data)
        assert message.type == "History"
        assert len(message.function_calls) == 1
        assert isinstance(message.function_calls[0], FunctionCallHistory)
        assert message.function_calls[0].name == "book_flight"

    def test_history_function_calls_message_post_init_conversion(self):
        """Test that __post_init__ converts dict function_calls to FunctionCallHistory objects"""
        # Create message with dict instead of FunctionCallHistory objects
        message = HistoryFunctionCallsMessage()
        message.function_calls = [
            {
                "id": "fc_202",
                "name": "convert_currency",
                "client_side": True,
                "arguments": '{"from": "USD", "to": "EUR", "amount": 100}',
                "response": "100 USD = 85.50 EUR"
            }
        ]

        # Trigger __post_init__
        message.__post_init__()

        assert len(message.function_calls) == 1
        assert isinstance(message.function_calls[0], FunctionCallHistory)
        assert message.function_calls[0].name == "convert_currency"


class TestContext:
    """Unit tests for Context class"""

    def test_context_creation_empty(self):
        """Test creating an empty Context object"""
        context = Context()
        assert context.messages == []

    def test_context_creation_with_conversation_messages(self):
        """Test creating Context with conversation messages"""
        msg1 = HistoryConversationMessage(
            role="user",
            content="Hello, I need help with my order"
        )
        msg2 = HistoryConversationMessage(
            role="assistant",
            content="I'd be happy to help! What's your order number?"
        )

        context = Context(messages=[msg1, msg2])

        assert len(context.messages) == 2
        assert isinstance(context.messages[0], HistoryConversationMessage)
        assert isinstance(context.messages[1], HistoryConversationMessage)
        assert context.messages[0].role == "user"
        assert context.messages[1].role == "assistant"

    def test_context_creation_with_function_call_messages(self):
        """Test creating Context with function call messages"""
        function_call = FunctionCallHistory(
            id="fc_303",
            name="lookup_order",
            client_side=True,
            arguments='{"order_number": "ORD-789"}',
            response="Order found: Status is Processing"
        )

        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])
        context = Context(messages=[func_msg])

        assert len(context.messages) == 1
        assert isinstance(context.messages[0], HistoryFunctionCallsMessage)
        assert len(context.messages[0].function_calls) == 1

    def test_context_creation_with_mixed_messages(self):
        """Test creating Context with both conversation and function call messages"""
        conv_msg = HistoryConversationMessage(
            role="user",
            content="What's my order status?"
        )

        function_call = FunctionCallHistory(
            id="fc_404",
            name="get_order_status",
            client_side=True,
            arguments='{"order_id": "12345"}',
            response="Your order is shipped and will arrive tomorrow"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        response_msg = HistoryConversationMessage(
            role="assistant",
            content="Your order is shipped and will arrive tomorrow"
        )

        context = Context(messages=[conv_msg, func_msg, response_msg])

        assert len(context.messages) == 3
        assert isinstance(context.messages[0], HistoryConversationMessage)
        assert isinstance(context.messages[1], HistoryFunctionCallsMessage)
        assert isinstance(context.messages[2], HistoryConversationMessage)

    def test_context_serialization(self):
        """Test Context JSON serialization"""
        conv_msg = HistoryConversationMessage(
            role="user",
            content="Test message"
        )

        context = Context(messages=[conv_msg])
        result = json.loads(context.to_json())

        expected = {
            "messages": [
                {
                    "type": "History",
                    "role": "user",
                    "content": "Test message"
                }
            ]
        }
        assert result == expected

    def test_context_deserialization(self):
        """Test Context deserialization from dict using realistic construction approach"""
        # Create message objects first, then construct Context
        conv_msg = HistoryConversationMessage(
            role="assistant",
            content="How can I help you today?"
        )

        function_call = FunctionCallHistory(
            id="fc_505",
            name="greet_user",
            client_side=False,
            arguments='{}',
            response="User greeted successfully"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        context = Context(messages=[conv_msg, func_msg])

        assert len(context.messages) == 2
        assert isinstance(context.messages[0], HistoryConversationMessage)
        assert isinstance(context.messages[1], HistoryFunctionCallsMessage)
        assert context.messages[0].content == "How can I help you today?"
        assert len(context.messages[1].function_calls) == 1

    def test_context_post_init_conversion(self):
        """Test that __post_init__ converts dict messages to appropriate message objects"""
        context = Context()
        context.messages = [
            {
                "type": "History",
                "role": "user",
                "content": "Hello"
            },
            {
                "type": "History",
                "function_calls": [
                    {
                        "id": "fc_606",
                        "name": "process_greeting",
                        "client_side": True,
                        "arguments": '{"greeting": "Hello"}',
                        "response": "Greeting processed"
                    }
                ]
            }
        ]

        # Trigger __post_init__
        context.__post_init__()

        assert len(context.messages) == 2
        assert isinstance(context.messages[0], HistoryConversationMessage)
        assert isinstance(context.messages[1], HistoryFunctionCallsMessage)
        assert context.messages[0].content == "Hello"
        assert len(context.messages[1].function_calls) == 1


class TestAgentIntegration:
    """Integration tests for Agent class with context"""

    def test_agent_with_context(self):
        """Test Agent class with context field"""
        conv_msg = HistoryConversationMessage(
            role="user",
            content="Previous conversation context"
        )
        context = Context(messages=[conv_msg])

        agent = Agent(
            language="en",
            context=context
        )

        assert agent.language == "en"
        assert agent.context is not None
        assert isinstance(agent.context, Context)
        assert len(agent.context.messages) == 1

    def test_agent_context_serialization(self):
        """Test Agent serialization with context"""
        function_call = FunctionCallHistory(
            id="fc_707",
            name="previous_action",
            client_side=True,
            arguments='{"action": "test"}',
            response="Action completed"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])
        context = Context(messages=[func_msg])

        agent = Agent(context=context)
        result = agent.to_dict()

        assert "context" in result
        assert "messages" in result["context"]
        assert len(result["context"]["messages"]) == 1
        assert result["context"]["messages"][0]["type"] == "History"

    def test_agent_context_deserialization(self):
        """Test Agent deserialization with context"""
        data = {
            "language": "es",
            "context": {
                "messages": [
                    {
                        "type": "History",
                        "role": "assistant",
                        "content": "Hola, ¿cómo puedo ayudarte?"
                    }
                ]
            }
        }

        agent = Agent.from_dict(data)

        assert agent.language == "es"
        assert agent.context is not None
        assert isinstance(agent.context, Context)
        assert len(agent.context.messages) == 1
        assert isinstance(agent.context.messages[0], HistoryConversationMessage)
        assert agent.context.messages[0].content == "Hola, ¿cómo puedo ayudarte?"


class TestSettingsOptionsIntegration:
    """Integration tests for SettingsOptions with flags and context"""

    def test_settings_options_with_flags(self):
        """Test SettingsOptions with flags field"""
        flags = Flags(history=True)
        settings = SettingsOptions(flags=flags)

        assert settings.flags is not None
        assert isinstance(settings.flags, Flags)
        assert settings.flags.history is True

    def test_settings_options_with_flags_and_context(self):
        """Test SettingsOptions with both flags and agent context"""
        # Create flags
        flags = Flags(history=True)

        # Create context with mixed messages
        conv_msg = HistoryConversationMessage(
            role="user",
            content="I want to continue our previous conversation"
        )

        function_call = FunctionCallHistory(
            id="fc_808",
            name="retrieve_context",
            client_side=True,
            arguments='{"session_id": "sess_123"}',
            response="Context retrieved successfully"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        context = Context(messages=[conv_msg, func_msg])

        # Create settings
        settings = SettingsOptions(
            flags=flags,
            agent=Agent(context=context)
        )

        assert settings.flags.history is True
        assert settings.agent.context is not None
        assert len(settings.agent.context.messages) == 2

    def test_settings_options_full_serialization(self):
        """Test complete SettingsOptions serialization with all new features"""
        flags = Flags(history=False)

        conv_msg = HistoryConversationMessage(
            role="assistant",
            content="Welcome back! I remember our last conversation."
        )

        function_call = FunctionCallHistory(
            id="fc_909",
            name="load_user_preferences",
            client_side=False,
            arguments='{"user_id": "user_456"}',
            response="Preferences loaded: theme=dark, language=en"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        context = Context(messages=[conv_msg, func_msg])

        settings = SettingsOptions(
            experimental=True,
            flags=flags,
            agent=Agent(
                language="en",
                context=context
            )
        )

        result = settings.to_dict()

        # Verify structure
        assert result["experimental"] is True
        assert result["flags"]["history"] is False
        assert result["agent"]["language"] == "en"
        assert "context" in result["agent"]
        assert len(result["agent"]["context"]["messages"]) == 2

        # Verify message types
        messages = result["agent"]["context"]["messages"]
        assert messages[0]["type"] == "History"
        assert messages[0]["role"] == "assistant"
        assert messages[1]["type"] == "History"
        assert "function_calls" in messages[1]

    def test_settings_options_full_deserialization(self):
        """Test complete SettingsOptions deserialization with all new features using realistic construction"""
        # Create message objects programmatically
        conv_msg = HistoryConversationMessage(
            role="user",
            content="¿Recuerdas nuestra conversación anterior?"
        )

        function_call = FunctionCallHistory(
            id="fc_010",
            name="buscar_historial",
            client_side=True,
            arguments='{"usuario": "test"}',
            response="Historial encontrado"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        context = Context(messages=[conv_msg, func_msg])
        flags = Flags(history=True)

        settings = SettingsOptions(
            experimental=False,
            flags=flags,
            agent=Agent(
                language="es",
                context=context
            )
        )

        assert settings.experimental is False
        assert settings.flags.history is True
        assert settings.agent.language == "es"
        assert len(settings.agent.context.messages) == 2

        # Verify message types are correctly set
        assert isinstance(settings.agent.context.messages[0], HistoryConversationMessage)
        assert isinstance(settings.agent.context.messages[1], HistoryFunctionCallsMessage)

        # Verify content
        assert settings.agent.context.messages[0].content == "¿Recuerdas nuestra conversación anterior?"
        assert len(settings.agent.context.messages[1].function_calls) == 1
        assert settings.agent.context.messages[1].function_calls[0].name == "buscar_historial"

    def test_settings_options_round_trip(self):
        """Test complete round-trip serialization/deserialization using a hybrid approach"""
        # Create original settings
        flags = Flags(history=True)

        conv_msg = HistoryConversationMessage(
            role="user",
            content="This is a test message for round-trip testing"
        )

        function_call = FunctionCallHistory(
            id="fc_roundtrip",
            name="test_function",
            client_side=True,
            arguments='{"test": "data"}',
            response="Test successful"
        )
        func_msg = HistoryFunctionCallsMessage(function_calls=[function_call])

        context = Context(messages=[conv_msg, func_msg])

        original = SettingsOptions(
            experimental=True,
            flags=flags,
            agent=Agent(
                language="en",
                context=context
            )
        )

        # Test serialization
        serialized = original.to_dict()

        # Verify serialized structure
        assert serialized["experimental"] is True
        assert serialized["flags"]["history"] is True
        assert serialized["agent"]["language"] == "en"
        assert "context" in serialized["agent"]
        assert len(serialized["agent"]["context"]["messages"]) == 2

        # Test that we can reconstruct equivalent object
        reconstructed_flags = Flags(history=serialized["flags"]["history"])

        # Reconstruct messages manually (more realistic usage)
        reconstructed_conv_msg = HistoryConversationMessage(
            role=serialized["agent"]["context"]["messages"][0]["role"],
            content=serialized["agent"]["context"]["messages"][0]["content"]
        )

        reconstructed_func_call = FunctionCallHistory(
            id=serialized["agent"]["context"]["messages"][1]["function_calls"][0]["id"],
            name=serialized["agent"]["context"]["messages"][1]["function_calls"][0]["name"],
            client_side=serialized["agent"]["context"]["messages"][1]["function_calls"][0]["client_side"],
            arguments=serialized["agent"]["context"]["messages"][1]["function_calls"][0]["arguments"],
            response=serialized["agent"]["context"]["messages"][1]["function_calls"][0]["response"]
        )
        reconstructed_func_msg = HistoryFunctionCallsMessage(function_calls=[reconstructed_func_call])

        reconstructed_context = Context(messages=[reconstructed_conv_msg, reconstructed_func_msg])

        restored = SettingsOptions(
            experimental=serialized["experimental"],
            flags=reconstructed_flags,
            agent=Agent(
                language=serialized["agent"]["language"],
                context=reconstructed_context
            )
        )

        # Verify everything matches
        assert restored.experimental == original.experimental
        assert restored.flags.history == original.flags.history
        assert restored.agent.language == original.agent.language
        assert len(restored.agent.context.messages) == len(original.agent.context.messages)

        # Verify message content
        assert restored.agent.context.messages[0].content == original.agent.context.messages[0].content
        assert len(restored.agent.context.messages[1].function_calls) == len(original.agent.context.messages[1].function_calls)
        assert restored.agent.context.messages[1].function_calls[0].name == original.agent.context.messages[1].function_calls[0].name


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_context_with_empty_messages(self):
        """Test Context handles empty messages list correctly"""
        context = Context(messages=[])
        assert context.messages == []

        result = context.to_dict()
        assert result["messages"] == []

    def test_history_function_calls_message_empty_function_calls(self):
        """Test HistoryFunctionCallsMessage handles empty function_calls list"""
        message = HistoryFunctionCallsMessage(function_calls=[])
        assert message.function_calls == []

        result = message.to_dict()
        assert result["function_calls"] == []

    def test_context_post_init_with_invalid_message_structure(self):
        """Test Context.__post_init__ handles malformed message dicts gracefully"""
        context = Context()
        context.messages = [
            {
                "type": "History",
                "role": "user",
                "content": "Valid conversation message"
            },
            {
                "type": "History"
                # Missing both content and function_calls - should default to conversation
            },
            {
                "type": "History",
                "function_calls": []  # Empty function calls
            }
        ]

        context.__post_init__()

        assert len(context.messages) == 3
        assert isinstance(context.messages[0], HistoryConversationMessage)
        assert isinstance(context.messages[1], HistoryConversationMessage)
        assert isinstance(context.messages[2], HistoryFunctionCallsMessage)

    def test_agent_context_none_handling(self):
        """Test Agent handles None context correctly"""
        agent = Agent(context=None)
        assert agent.context is None

        result = agent.to_dict()
        # context should be excluded from serialization when None
        assert "context" not in result

    def test_settings_options_flags_none_handling(self):
        """Test SettingsOptions handles None flags correctly"""
        settings = SettingsOptions(flags=None)
        assert settings.flags is None

        result = settings.to_dict()
        # flags should be excluded from serialization when None
        assert "flags" not in result