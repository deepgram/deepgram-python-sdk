# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib
import time
from typing import Dict, Any

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
    InjectUserMessageOptions,
    FunctionCallRequest,
    FunctionCallResponse,
)

from tests.utils import save_metadata_string

# Test configurations
test_cases = [
    {
        "name": "basic_conversation",
        "agent_config": {
            "think": {
                "provider": {"type": "open_ai", "model": "gpt-4o-mini"},
                "prompt": "You are a helpful AI assistant. Keep responses brief."
            },
            "speak": {"provider": {"type": "deepgram", "model": "aura-2-thalia-en"}},
            "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
            "language": "en"
        },
        "inject_messages": [
            "Hello, can you help me with a simple question?",
            "What is 2 + 2?"
        ],
        "expected_events": [
            "Welcome",
            "SettingsApplied",
            "ConversationText",
            "AgentAudioDone"
        ]
    }
]


@pytest.mark.parametrize("test_case", test_cases)
def test_daily_agent_websocket(test_case: Dict[str, Any]):
    """Test agent websocket functionality with real API calls"""

    # Setup unique test ID
    test_name = test_case["name"]
    config_hash = hashlib.sha256(json.dumps(test_case["agent_config"], sort_keys=True).encode()).hexdigest()
    unique = f"{test_name}-{config_hash[:8]}"

    # File paths for metadata
    file_config = f"tests/response_data/agent/websocket/{unique}-config.json"
    file_events = f"tests/response_data/agent/websocket/{unique}-events.json"
    file_error = f"tests/response_data/agent/websocket/{unique}-error.json"

    # Cleanup previous runs
    for file_path in [file_config, file_events, file_error]:
        with contextlib.suppress(FileNotFoundError):
            os.remove(file_path)

    # Test state tracking
    received_events = []
    conversation_text_list = []
    function_calls = []
    connection_established = False
    conversation_complete = False

    # Create Deepgram client
    config = DeepgramClientOptions(
        options={"keepalive": "true", "speaker_playback": "true"}
    )
    deepgram = DeepgramClient("", config)
    dg_connection = deepgram.agent.websocket.v("1")

    # Event handlers
    def on_open(self, open, **kwargs):
        nonlocal connection_established
        connection_established = True
        received_events.append({"type": "Open", "timestamp": time.time()})

    def on_welcome(self, welcome, **kwargs):
        received_events.append({"type": "Welcome", "data": welcome.to_dict()})

    def on_settings_applied(self, settings_applied, **kwargs):
        received_events.append({"type": "SettingsApplied", "data": settings_applied.to_dict()})

    def on_conversation_text(self, conversation_text, **kwargs):
        conversation_text_list.append(conversation_text.to_dict())
        received_events.append({"type": "ConversationText", "data": conversation_text.to_dict()})

    def on_function_call_request(self, function_call_request: FunctionCallRequest, **kwargs):
        function_calls.append(function_call_request.to_dict())
        received_events.append({"type": "FunctionCallRequest", "data": function_call_request.to_dict()})

        # Automatically respond to function calls
        response = FunctionCallResponse(
            function_call_id=function_call_request.function_call_id,
            output=json.dumps({"temperature": "72°F", "condition": "sunny"})
        )
        dg_connection.send_function_call_response(response)

    def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
        received_events.append({"type": "AgentStartedSpeaking", "data": agent_started_speaking.to_dict()})

    def on_agent_audio_done(self, agent_audio_done, **kwargs):
        received_events.append({"type": "AgentAudioDone", "data": agent_audio_done.to_dict()})

    def on_error(self, error, **kwargs):
        received_events.append({"type": "Error", "data": error.to_dict()})

    # Register event handlers
    dg_connection.on(AgentWebSocketEvents.Open, on_open)
    dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
    dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
    dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
    dg_connection.on(AgentWebSocketEvents.FunctionCallRequest, on_function_call_request)
    dg_connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
    dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
    dg_connection.on(AgentWebSocketEvents.Error, on_error)

    try:
        # Create settings from test case
        settings = SettingsOptions()
        settings.agent = test_case["agent_config"]

        # Test 1: Connection establishment
        connection_started = dg_connection.start(settings)
        assert connection_started, f"Test ID: {unique} - Connection should start successfully"

        # Wait for connection establishment
        timeout = 0
        while not connection_established and timeout < 10:
            time.sleep(0.5)
            timeout += 1

        assert connection_established, f"Test ID: {unique} - Should receive Open event"

        # Test 2: Inject user messages and validate responses
        for i, message in enumerate(test_case["inject_messages"]):
            time.sleep(1)  # Allow previous conversation to settle

            options = InjectUserMessageOptions(content=message)
            inject_success = dg_connection.inject_user_message(options)
            assert inject_success, f"Test ID: {unique} - InjectUserMessage should succeed for message {i+1}"

            # Wait for agent response (up to 15 seconds per message)
            response_timeout = 0
            initial_event_count = len(received_events)

            while response_timeout < 30:
                if len(received_events) > initial_event_count:
                    # New events received, check if we got expected responses
                    recent_events = [e["type"] for e in received_events[initial_event_count:]]
                    if "ConversationText" in recent_events or "AgentStartedSpeaking" in recent_events:
                        break
                time.sleep(0.5)
                response_timeout += 1

        # Allow final processing
        time.sleep(2)

        # Test 3: Validate expected events were received
        event_types = [event["type"] for event in received_events]
        print(f"Test ID: {unique} - Received events: {event_types}")

        for expected_event in test_case["expected_events"]:
            assert expected_event in event_types, f"Test ID: {unique} - Should receive {expected_event} event"

        # Test 4: Validate conversation flow
        if test_case["inject_messages"]:
            assert len(conversation_text_list) > 0, f"Test ID: {unique} - Should receive conversation text"

        # Test 5: Validate function calls (if expected)
        if "function_call_conversation" in test_case["name"]:
            assert len(function_calls) > 0, f"Test ID: {unique} - Should receive function call requests"

            # Validate function call structure
            for func_call in function_calls:
                assert "function_name" in func_call, "Function call should have function_name"
                assert "function_call_id" in func_call, "Function call should have function_call_id"

        conversation_complete = True

    except Exception as e:
        error_data = {"error": str(e), "events": received_events}
        save_metadata_string(file_error, json.dumps(error_data, indent=2))
        raise

    finally:
        # Cleanup connection
        if dg_connection:
            dg_connection.finish()
            time.sleep(1)

        # Save test metadata
        save_metadata_string(file_config, json.dumps(test_case, indent=2))
        save_metadata_string(file_events, json.dumps(received_events, indent=2))

    # Final validations
    assert conversation_complete, f"Test ID: {unique} - Conversation should complete successfully"
    assert len(received_events) >= len(test_case["expected_events"]), f"Test ID: {unique} - Should receive minimum expected events"
