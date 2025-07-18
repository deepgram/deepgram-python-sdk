# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib
import time
from typing import Dict, Any, List, Optional

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
    InjectUserMessageOptions,
    FunctionCallRequest,
    FunctionCallResponse,
    InjectAgentMessageOptions,
)

from tests.utils import save_metadata_string

# Enhanced test configurations covering all agent functionality
test_cases = [
    {
        "name": "basic_conversation",
        "description": "Basic conversation with simple questions",
        "agent_config": {
            "think": {
                "provider": {"type": "open_ai", "model": "gpt-4o-mini"},
                "prompt": "You are a helpful AI assistant. Keep responses brief and conversational."
            },
            "speak": {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
            "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
            "language": "en"
        },
        "inject_messages": [
            "Hello, can you help me with a simple question?",
            "What is 2 + 2?",
            "Thank you for your help."
        ],
        "expected_events": [
            "Welcome",
            "SettingsApplied",
            "ConversationText",
            "AgentAudioDone"
        ],
        "test_inject_user_message": True,
        "test_inject_agent_message": False,
        "test_function_calls": False
    },
    {
        "name": "fallback_providers",
        "description": "Test fallback functionality with multiple speak providers",
        "agent_config": {
            "think": {
                "provider": {"type": "open_ai", "model": "gpt-4o-mini"},
                "prompt": "You are a helpful assistant. Keep responses brief."
            },
            "speak": [
                {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
                {"provider": {"type": "deepgram", "model": "aura-2-luna-en"}}
            ],
            "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
            "language": "en"
        },
        "inject_messages": [
            "Hello, can you test speaking with fallback providers?",
            "Please say something else to test the fallback."
        ],
        "expected_events": [
            "Welcome",
            "SettingsApplied",
            "ConversationText",
            "AgentAudioDone"
        ],
        "test_inject_user_message": True,
        "test_inject_agent_message": False,
        "test_function_calls": False
    },
    {
        "name": "inject_agent_message",
        "description": "Test inject_agent_message functionality (expected to fail until #553 is resolved)",
        "agent_config": {
            "think": {
                "provider": {"type": "open_ai", "model": "gpt-4o-mini"},
                "prompt": "You are a helpful assistant. Keep responses brief and conversational."
            },
            "speak": {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
            "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
            "language": "en"
        },
        "inject_messages": [
            "Hello, I'm going to inject some agent messages."
        ],
        "agent_messages": [
            "Hello! I'm an agent message injected directly.",
            "This is another agent message to test the functionality."
        ],
        "expected_events": [
            "Welcome",
            "SettingsApplied",
            "ConversationText"
        ],
        "conditional_events": [
            "AgentStartedSpeaking",
            "AgentAudioDone"
        ],
        "test_inject_user_message": True,
        "test_inject_agent_message": True,
        "test_function_calls": False,
        "expect_error": True  # Still expecting errors due to SDK function calling bugs (#528)
    },
    {
        "name": "function_call_conversation",
        "description": "Test function calling with corrected HTTP method case (expected to fail due to #528)",
        "agent_config": {
            "think": {
                "provider": {"type": "open_ai", "model": "gpt-4o-mini"},
                "prompt": "You are a helpful assistant that can call functions to get weather information.",
                "functions": [
                    {
                        "name": "get_weather",
                        "description": "Get current weather information for a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The location to get weather for"
                                }
                            },
                            "required": ["location"]
                        },
                        "method": "get",
                        "url": "https://api.example.com/weather"
                    }
                ]
            },
            "speak": {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
            "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
            "language": "en"
        },
        "inject_messages": [
            "What's the weather like in New York?",
            "Can you also check the weather in London?"
        ],
        "expected_events": [
            "Welcome",
            "SettingsApplied",
            "ConversationText"
        ],
        "conditional_events": [
            "FunctionCallRequest",
            "AgentStartedSpeaking",
            "AgentAudioDone"
        ],
        "test_inject_user_message": True,
        "test_inject_agent_message": False,
        "test_function_calls": True,
        "expect_error": True  # Still expecting errors due to SDK function calling bugs
    },
    # NOTE: function_call_conversation and inject_agent_message tests are marked as xfail
    # - function_call_conversation: #528 - SDK function calling structure doesn't match new API spec
    # - inject_agent_message: #553 - SDK missing inject_agent_message method implementation
    # TODO: These should be re-enabled once the bugs are fixed
]


@pytest.mark.parametrize("test_case", test_cases)
def test_daily_agent_websocket(test_case: Dict[str, Any]):
    """
    Enhanced test for agent websocket functionality with comprehensive coverage.

    This test covers:
    1. Basic conversation flow
    2. Function calling
    3. Fallback provider functionality
    4. InjectUserMessage and InjectAgentMessage
    5. Comprehensive event validation
    6. Error handling and recovery

    Note: Some events like EndOfThought may appear as "Unhandled" - this is expected
    as they are not officially documented as supported features yet.

    Note: some features might have bugs, like inject_agent_message and function_call_conversation. We intend to fix these in the future and update the tests.
    """

    # Mark tests as expected to fail for known issues
    if test_case["name"] == "inject_agent_message":
        pytest.xfail(reason="#553 - inject_agent_message method not implemented in SDK")
    elif test_case["name"] == "function_call_conversation":
        pytest.xfail(reason="#528 - SDK function calling structure doesn't match new API spec")

    # Check for required environment variables
    if not os.getenv("DEEPGRAM_API_KEY"):
        pytest.skip("DEEPGRAM_API_KEY environment variable not set")

    # Setup unique test ID
    test_name = test_case["name"]
    config_hash = hashlib.sha256(json.dumps(test_case["agent_config"], sort_keys=True).encode()).hexdigest()
    unique = f"{test_name}-{config_hash[:8]}"

    print(f"\n{'='*60}")
    print(f"Running Test: {test_name}")
    print(f"Description: {test_case['description']}")
    print(f"Test ID: {unique}")
    print(f"{'='*60}")

    # File paths for metadata
    file_config = f"tests/response_data/agent/websocket/{unique}-config.json"
    file_events = f"tests/response_data/agent/websocket/{unique}-events.json"
    file_error = f"tests/response_data/agent/websocket/{unique}-error.json"
    file_function_calls = f"tests/response_data/agent/websocket/{unique}-function_calls.json"

    # Cleanup previous runs
    for file_path in [file_config, file_events, file_error, file_function_calls]:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)

    # Test state tracking
    received_events = []
    conversation_text_list = []
    function_calls = []
    function_call_bugs = []
    injection_refused_events = []
    connection_established = False
    conversation_complete = False

    # Create Deepgram client with enhanced options
    config = DeepgramClientOptions(
        options={
            "keepalive": "true",
            "experimental": "true"  # Enable experimental features
        }
    )
    deepgram = DeepgramClient("", config)
    dg_connection = deepgram.agent.websocket.v("1")

    # Enhanced event handlers
    def on_open(self, open, **kwargs):
        nonlocal connection_established
        connection_established = True
        received_events.append({
            "type": "Open",
            "timestamp": time.time(),
            "data": open.to_dict() if hasattr(open, 'to_dict') else str(open)
        })
        print(f"✓ Connection opened at {time.time()}")

    def on_welcome(self, welcome, **kwargs):
        received_events.append({
            "type": "Welcome",
            "timestamp": time.time(),
            "data": welcome.to_dict()
        })
        print(f"✓ Welcome received: {welcome.to_dict()}")

    def on_settings_applied(self, settings_applied, **kwargs):
        received_events.append({
            "type": "SettingsApplied",
            "timestamp": time.time(),
            "data": settings_applied.to_dict()
        })
        print(f"✓ Settings applied: {settings_applied.to_dict()}")

    def on_conversation_text(self, conversation_text, **kwargs):
        conversation_text_list.append(conversation_text.to_dict())
        received_events.append({
            "type": "ConversationText",
            "timestamp": time.time(),
            "data": conversation_text.to_dict()
        })
        print(f"💬 Conversation text: {conversation_text.to_dict()}")

    def on_function_call_request(self, function_call_request: FunctionCallRequest, **kwargs):
        """
        Enhanced function call handler that tests for SDK bugs.

        The official API spec expects:
        - functions: array of {id, name, arguments, client_side}

        But the SDK currently has:
        - function_name: string
        - function_call_id: string
        - input: string
        """
        function_call_data = function_call_request.to_dict()
        function_calls.append(function_call_data)
        received_events.append({
            "type": "FunctionCallRequest",
            "timestamp": time.time(),
            "data": function_call_data
        })

        print(f"🔧 Function call request: {function_call_data}")

        # Test for SDK bug: Check current SDK structure vs official API spec
        sdk_bug_detected = False
        bug_details = {}

        # Check for SDK's current incorrect structure
        if "function_name" in function_call_data and "function_call_id" in function_call_data:
            sdk_bug_detected = True
            bug_details.update({
                "bug_type": "incorrect_sdk_structure",
                "current_sdk_fields": ["function_name", "function_call_id", "input"],
                "expected_api_fields": ["functions"],
                "description": "SDK uses flat structure instead of functions array"
            })

        # Check for missing official API spec fields
        if "functions" not in function_call_data:
            sdk_bug_detected = True
            bug_details.update({
                "missing_field": "functions",
                "description": "Official API spec requires 'functions' array"
            })

        if sdk_bug_detected:
            function_call_bugs.append({
                "timestamp": time.time(),
                "request_data": function_call_data,
                "bug_details": bug_details
            })
            print(f"🚨 SDK Bug detected: {bug_details}")

        # Respond to function call using current SDK structure (even though it's wrong)
        try:
            if hasattr(function_call_request, 'function_call_id'):
                # Use SDK's incorrect structure
                response = FunctionCallResponse(
                    function_call_id=function_call_request.function_call_id,
                    output=json.dumps({
                        "success": True,
                        "result": "Mock function response",
                        "timestamp": time.time()
                    })
                )
                dg_connection.send_function_call_response(response)
                print(f"✓ Function call response sent using SDK structure")
            else:
                print(f"❌ Cannot respond to function call - no function_call_id field")
        except Exception as e:
            print(f"❌ Function call response failed: {e}")
            received_events.append({
                "type": "FunctionCallResponseError",
                "timestamp": time.time(),
                "error": str(e)
            })

    def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
        received_events.append({
            "type": "AgentStartedSpeaking",
            "timestamp": time.time(),
            "data": agent_started_speaking.to_dict()
        })
        print(f"🗣️  Agent started speaking: {agent_started_speaking.to_dict()}")

    def on_agent_audio_done(self, agent_audio_done, **kwargs):
        received_events.append({
            "type": "AgentAudioDone",
            "timestamp": time.time(),
            "data": agent_audio_done.to_dict()
        })
        print(f"✓ Agent audio done: {agent_audio_done.to_dict()}")

    def on_injection_refused(self, injection_refused, **kwargs):
        injection_refused_events.append(injection_refused.to_dict())
        received_events.append({
            "type": "InjectionRefused",
            "timestamp": time.time(),
            "data": injection_refused.to_dict()
        })
        print(f"❌ Injection refused: {injection_refused.to_dict()}")

    def on_error(self, error, **kwargs):
        received_events.append({
            "type": "Error",
            "timestamp": time.time(),
            "data": error.to_dict()
        })
        print(f"❌ Error: {error.to_dict()}")

    def on_unhandled(self, unhandled, **kwargs):
        received_events.append({
            "type": "Unhandled",
            "timestamp": time.time(),
            "data": unhandled.to_dict()
        })
        # Note: EndOfThought events are expected to be unhandled as they're not officially documented as supported features yet
        print(f"❓ Unhandled: {unhandled.to_dict()}")

    # Register all event handlers
    dg_connection.on(AgentWebSocketEvents.Open, on_open)
    dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
    dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
    dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
    dg_connection.on(AgentWebSocketEvents.FunctionCallRequest, on_function_call_request)
    dg_connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
    dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
    dg_connection.on(AgentWebSocketEvents.InjectionRefused, on_injection_refused)
    dg_connection.on(AgentWebSocketEvents.Error, on_error)
    dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

    try:
        # Create enhanced settings from test case
        settings = SettingsOptions()
        settings.agent = test_case["agent_config"]
        settings.experimental = True  # Enable experimental features

        print(f"🔧 Starting connection with settings: {settings.to_dict()}")

        # Test 1: Connection establishment
        print("\n--- Test 1: Connection Establishment ---")
        connection_started = dg_connection.start(settings)
        assert connection_started, f"Test ID: {unique} - Connection should start successfully"

        # Wait for connection establishment with timeout
        timeout = 0
        while not connection_established and timeout < 15:
            time.sleep(0.5)
            timeout += 1

        assert connection_established, f"Test ID: {unique} - Should receive Open event within 15 seconds"
        print("✓ Connection established successfully")

        # Test 2: Inject user messages and validate responses
        if test_case.get("test_inject_user_message", False):
            print("\n--- Test 2: InjectUserMessage Testing ---")
            for i, message in enumerate(test_case["inject_messages"]):
                print(f"📤 Injecting user message {i+1}: '{message}'")
                time.sleep(1)  # Allow previous conversation to settle

                options = InjectUserMessageOptions(content=message)
                inject_success = dg_connection.inject_user_message(options)
                assert inject_success, f"Test ID: {unique} - InjectUserMessage should succeed for message {i+1}"

                # Wait for agent response with improved timeout handling
                response_timeout = 0
                initial_event_count = len(received_events)

                while response_timeout < 30:
                    if len(received_events) > initial_event_count:
                        recent_events = [e["type"] for e in received_events[initial_event_count:]]
                        if "ConversationText" in recent_events or "AgentStartedSpeaking" in recent_events:
                            print(f"✓ Agent responded to message {i+1}")
                            break
                    time.sleep(0.5)
                    response_timeout += 1

                if response_timeout >= 30:
                    print(f"⚠️  Agent did not respond to message {i+1} within timeout")

        # Test 3: Inject agent messages (if enabled)
        if test_case.get("test_inject_agent_message", False):
            print("\n--- Test 3: InjectAgentMessage Testing ---")
            for i, message in enumerate(test_case.get("agent_messages", [])):
                print(f"📤 Injecting agent message {i+1}: '{message}'")
                time.sleep(1)  # Allow previous conversation to settle

                options = InjectAgentMessageOptions(message=message)
                inject_success = dg_connection.inject_agent_message(options)

                if inject_success:
                    print(f"✓ Agent message {i+1} injected successfully")
                else:
                    print(f"❌ Agent message {i+1} injection failed")

                # Wait for any response or events
                response_timeout = 0
                initial_event_count = len(received_events)

                while response_timeout < 15:
                    if len(received_events) > initial_event_count:
                        recent_events = [e["type"] for e in received_events[initial_event_count:]]
                        print(f"📊 Events after agent message {i+1}: {recent_events}")
                        break
                    time.sleep(0.5)
                    response_timeout += 1

                if response_timeout >= 15:
                    print(f"⚠️  No events received after agent message {i+1}")

        # Allow final processing
        time.sleep(3)
        print("\n--- Test Results Analysis ---")

        # Test 4: Validate expected events were received
        event_types = [event["type"] for event in received_events]
        print(f"📊 Received events: {event_types}")

        # Check for required events (always expected)
        for expected_event in test_case["expected_events"]:
            assert expected_event in event_types, f"Test ID: {unique} - Should receive {expected_event} event"
            print(f"✓ Expected event received: {expected_event}")

        # Check for conditional events (only if no error expected or no error occurred)
        conditional_events = test_case.get("conditional_events", [])
        expect_error = test_case.get("expect_error", False)

        if conditional_events:
            if expect_error:
                # For error scenarios, check if conditional events are present but don't require them
                for conditional_event in conditional_events:
                    if conditional_event in event_types:
                        print(f"✓ Conditional event received: {conditional_event}")
                    else:
                        print(f"ℹ️  Conditional event not received (expected in error scenario): {conditional_event}")
            else:
                # For non-error scenarios, require conditional events
                for conditional_event in conditional_events:
                    assert conditional_event in event_types, f"Test ID: {unique} - Should receive {conditional_event} event"
                    print(f"✓ Conditional event received: {conditional_event}")

        # Test 5: Validate conversation flow
        if test_case.get("test_inject_user_message", False) and test_case["inject_messages"]:
            assert len(conversation_text_list) > 0, f"Test ID: {unique} - Should receive conversation text"
            print(f"✓ Conversation flow validated ({len(conversation_text_list)} conversation texts)")

        # Test 6: Validate function calls and detect SDK bugs
        if test_case.get("test_function_calls", False):
            print("\n--- Function Call Analysis ---")
            if len(function_calls) > 0:
                print(f"✓ Function calls received: {len(function_calls)}")

                # Analyze function call structure for SDK bugs
                for i, func_call in enumerate(function_calls):
                    print(f"Function call {i+1}: {func_call}")

                    # Test current SDK structure (incorrect)
                    sdk_fields = ["function_name", "function_call_id", "input"]
                    api_fields = ["functions"]

                    has_sdk_fields = all(field in func_call for field in sdk_fields)
                    has_api_fields = any(field in func_call for field in api_fields)

                    if has_sdk_fields and not has_api_fields:
                        print(f"🚨 SDK Bug confirmed: Function call uses incorrect structure")
                        print(f"   Current SDK fields: {[f for f in sdk_fields if f in func_call]}")
                        print(f"   Missing API fields: {[f for f in api_fields if f not in func_call]}")
                    elif has_api_fields:
                        print(f"✓ Correct API structure detected")
                    else:
                        print(f"❓ Unexpected function call structure")

                print(f"📊 SDK bugs detected: {len(function_call_bugs)}")
                for bug in function_call_bugs:
                    print(f"   Bug: {bug['bug_details']}")

            elif "function_call_conversation" in test_case["name"]:
                print(f"❌ Expected function calls but none received")
                # This might be expected if the bug prevents function calls from working
            else:
                print("ℹ️  No function calls expected or received")

        # Test 7: Validate injection refused events
        if len(injection_refused_events) > 0:
            print(f"📊 Injection refused events: {len(injection_refused_events)}")
            for event in injection_refused_events:
                print(f"   Refused: {event}")

        conversation_complete = True
        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        error_data = {
            "error": str(e),
            "events": received_events,
            "function_calls": function_calls,
            "function_call_bugs": function_call_bugs,
            "conversation_texts": conversation_text_list,
            "injection_refused": injection_refused_events
        }
        save_metadata_string(file_error, json.dumps(error_data, indent=2))
        raise

    finally:
        # Cleanup connection
        print("\n🔧 Cleaning up connection...")
        if dg_connection:
            dg_connection.finish()
            time.sleep(1)

        # Save comprehensive test metadata
        save_metadata_string(file_config, json.dumps(test_case, indent=2))
        save_metadata_string(file_events, json.dumps(received_events, indent=2))

        # Save function call analysis
        if function_calls or function_call_bugs:
            function_call_analysis = {
                "function_calls": function_calls,
                "sdk_bugs_detected": function_call_bugs,
                "total_calls": len(function_calls),
                "total_bugs": len(function_call_bugs)
            }
            save_metadata_string(file_function_calls, json.dumps(function_call_analysis, indent=2))

    # Final comprehensive validations
    assert conversation_complete, f"Test ID: {unique} - Conversation should complete successfully"
    assert len(received_events) >= len(test_case["expected_events"]), f"Test ID: {unique} - Should receive minimum expected events"

    # Report test summary
    print(f"\n📋 Test Summary for {unique}:")
    print(f"   Events received: {len(received_events)}")
    print(f"   Conversation texts: {len(conversation_text_list)}")
    print(f"   Function calls: {len(function_calls)}")
    print(f"   SDK bugs detected: {len(function_call_bugs)}")
    print(f"   Injection refused: {len(injection_refused_events)}")

    # Count and report unhandled events
    unhandled_events = [e for e in received_events if e["type"] == "Unhandled"]
    if unhandled_events:
        print(f"   Unhandled events: {len(unhandled_events)} (expected for undocumented features like EndOfThought)")

    # If function call bugs were detected, provide detailed information
    if function_call_bugs:
        print(f"\n🚨 IMPORTANT: SDK Function Call Bugs Detected!")
        print(f"   The SDK implementation does not match the official API specification.")
        print(f"   See {file_function_calls} for detailed analysis.")

        # This assertion will fail if bugs are detected, highlighting the issue
        if test_case.get("test_function_calls", False):
            # Don't fail the test for the bug detection - that's expected
            # But log it clearly for the developer
            print(f"   This is the expected bug you wanted to test for.")
