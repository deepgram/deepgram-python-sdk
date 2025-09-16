# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import random
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
    FunctionCallRequest,
    FunctionCallResponse,
    HistoryConversationMessage,
    HistoryFunctionCallsMessage,
    Context,
    Flags,
)

# Mock weather data for demo purposes
WEATHER_DATA = {
    "new york": {"temperature": 72, "condition": "sunny", "humidity": 45},
    "london": {"temperature": 18, "condition": "cloudy", "humidity": 80},
    "tokyo": {"temperature": 25, "condition": "rainy", "humidity": 90},
    "paris": {"temperature": 20, "condition": "partly cloudy", "humidity": 60},
    "sydney": {"temperature": 28, "condition": "sunny", "humidity": 50},
}

def get_weather(location, unit="fahrenheit"):
    """
    Mock weather function that returns simulated weather data.
    In a real application, this would call an actual weather API.
    """
    location_key = location.lower()

    if location_key not in WEATHER_DATA:
        # Return random weather for unknown locations
        temp_c = random.randint(10, 35)
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy"]
        weather = {
            "temperature": temp_c,
            "condition": random.choice(conditions),
            "humidity": random.randint(30, 90)
        }
    else:
        weather = WEATHER_DATA[location_key].copy()

    # Convert temperature if needed
    if unit.lower() == "fahrenheit":
        if location_key not in WEATHER_DATA:  # Convert from Celsius
            weather["temperature"] = int(weather["temperature"] * 9/5 + 32)
        # WEATHER_DATA is already in Fahrenheit for known locations
    else:  # Celsius
        if location_key in WEATHER_DATA:  # Convert from Fahrenheit
            weather["temperature"] = int((weather["temperature"] - 32) * 5/9)

    return {
        "location": location,
        "temperature": weather["temperature"],
        "unit": unit,
        "condition": weather["condition"],
        "humidity": weather["humidity"],
        "description": f"The weather in {location} is {weather['condition']} with a temperature of {weather['temperature']}°{'F' if unit.lower() == 'fahrenheit' else 'C'} and {weather['humidity']}% humidity."
    }


def main():
    try:
        print("🌤️  Starting Agent History & Weather Function Calling Demo")
        print("=" * 60)

        # Initialize Deepgram client with enhanced options
        config: DeepgramClientOptions = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "microphone_record": "true",
                "speaker_playback": "true",
            },
            verbose=verboselogs.INFO,
        )

        deepgram: DeepgramClient = DeepgramClient("", config)
        dg_connection = deepgram.agent.websocket.v("1")

        # Create initial conversation history for context
        conversation_history = [
            HistoryConversationMessage(
                role="user",
                content="Hello, I'm looking for weather information."
            ),
            HistoryConversationMessage(
                role="assistant",
                content="Hello! I'm your weather assistant with access to current weather data. I can help you get weather information for any location worldwide. What city would you like to know about?"
            )
        ]

        def on_open(self, open, **kwargs):
            print(f"🔌 Connection opened: {open}")

        def on_binary_data(self, data, **kwargs):
            # Handle audio data if needed
            pass

        def on_welcome(self, welcome, **kwargs):
            print(f"👋 Welcome received: {welcome}")

        def on_settings_applied(self, settings_applied, **kwargs):
            print(f"⚙️  Settings applied: {settings_applied}")

        def on_conversation_text(self, conversation_text, **kwargs):
            print(f"💬 Conversation: {conversation_text}")

        def on_user_started_speaking(self, user_started_speaking, **kwargs):
            print(f"🎤 User started speaking: {user_started_speaking}")

        def on_agent_thinking(self, agent_thinking, **kwargs):
            print(f"🤔 Agent thinking: {agent_thinking}")

        def on_history(self, history, **kwargs):
            """
            Handle History events for both conversation context and function call history.
            This is a first-class event, NOT an unhandled event.
            """
            print(f"📚 History event received: {type(history)}")

            # Check if this is conversation history or function call history
            if hasattr(history, 'role') and hasattr(history, 'content'):
                # This is conversation history
                print(f"📚 Conversation History payload:")
                print(f"   Type: {getattr(history, 'type', 'History')}")
                print(f"   Role: {history.role}")
                print(f"   Content: {history.content}")
                print()
            elif hasattr(history, 'function_calls'):
                # This is function call history
                print(f"📚 Function Call History payload:")
                print(f"   Type: {getattr(history, 'type', 'History')}")
                print(f"   Function calls: {len(history.function_calls) if history.function_calls else 0}")
                if history.function_calls:
                    for i, call in enumerate(history.function_calls):
                        print(f"   Call {i+1}:")
                        print(f"     ID: {call.id}")
                        print(f"     Name: {call.name}")
                        print(f"     Client Side: {call.client_side}")
                        print(f"     Arguments: {call.arguments}")
                        print(f"     Response: {call.response[:100]}..." if len(call.response) > 100 else f"     Response: {call.response}")
                print()
            else:
                print(f"📚 Unknown History payload format: {history}")

        def on_function_call_request(self, function_call_request: FunctionCallRequest, **kwargs):
            """
            Handle function call requests from the agent.
            This will generate new History events automatically.
            """
            # FunctionCallRequest contains a list of functions - usually just one
            if not function_call_request.functions or len(function_call_request.functions) == 0:
                print("❌ No functions in FunctionCallRequest")
                return

            # Get the first (and usually only) function call
            function_call = function_call_request.functions[0]

            print(f"🔧 Function Call Request: {function_call.name}")
            print(f"   ID: {function_call.id}")
            print(f"   Arguments: {function_call.arguments}")
            print(f"   Client Side: {function_call.client_side}")

            try:
                # Parse the function arguments
                args = json.loads(function_call.arguments)

                if function_call.name == "get_weather":
                    # Call our weather function
                    location = args.get("location", "")
                    unit = args.get("unit", "fahrenheit")

                    weather_data = get_weather(location, unit)

                    # Send the response back
                    response = FunctionCallResponse(
                        id=function_call.id,
                        name=function_call.name,
                        content=json.dumps(weather_data)
                    )

                    print(f"📞 Sending weather response for {location}: {weather_data['description']}")
                    dg_connection.send(response.to_json())
                else:
                    # Unknown function
                    response = FunctionCallResponse(
                        id=function_call.id,
                        name=function_call.name,
                        content=json.dumps({"error": f"Unknown function: {function_call.name}"})
                    )
                    dg_connection.send(response.to_json())

            except json.JSONDecodeError as e:
                print(f"❌ Error parsing function arguments: {e}")
                response = FunctionCallResponse(
                    id=function_call.id,
                    name=function_call.name,
                    content=json.dumps({"error": "Invalid JSON in function arguments"})
                )
                dg_connection.send(response.to_json())
            except Exception as e:
                print(f"❌ Error in function call: {e}")
                response = FunctionCallResponse(
                    id=function_call.id,
                    name=function_call.name,
                    content=json.dumps({"error": str(e)})
                )
                dg_connection.send(response.to_json())

        def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
            print(f"🗣️  Agent started speaking: {agent_started_speaking}")

        def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print(f"🔇 Agent audio done: {agent_audio_done}")

        def on_close(self, close, **kwargs):
            print(f"🔌 Connection closed: {close}")

        def on_error(self, error, **kwargs):
            print(f"❌ Error: {error}")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"❓ Unhandled event: {unhandled}")

        # Register event handlers
        dg_connection.on(AgentWebSocketEvents.Open, on_open)
        dg_connection.on(AgentWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
        dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
        dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
        dg_connection.on(AgentWebSocketEvents.UserStartedSpeaking, on_user_started_speaking)
        dg_connection.on(AgentWebSocketEvents.AgentThinking, on_agent_thinking)
        dg_connection.on(AgentWebSocketEvents.History, on_history)  # First-class History event handler
        dg_connection.on(AgentWebSocketEvents.FunctionCallRequest, on_function_call_request)
        dg_connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
        dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        dg_connection.on(AgentWebSocketEvents.Close, on_close)
        dg_connection.on(AgentWebSocketEvents.Error, on_error)
        dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

        # Configure agent settings with history and function calling
        options: SettingsOptions = SettingsOptions()

        # Enable history feature for conversation context
        options.flags = Flags(history=True)

        # Agent tags for analytics
        options.tags = ["history-example", "function-calling", "weather-demo"]

        # Audio configuration
        options.audio.input.encoding = "linear16"
        options.audio.input.sample_rate = 16000

        # Agent language and context
        options.agent.language = "en"

        # Provide conversation context/history
        options.agent.context = Context(messages=conversation_history)

        # Configure listen provider
        options.agent.listen.provider.type = "deepgram"
        options.agent.listen.provider.model = "nova-2"

        # Configure speak provider
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-asteria-en"

        # Configure the thinking/LLM provider with function calling
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"

        # Define available functions using OpenAPI-like schema
        options.agent.think.functions = [
            {
                "name": "get_weather",
                "description": "Get the current weather conditions for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location to get weather for (e.g., 'New York', 'London', 'Tokyo')"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["fahrenheit", "celsius"],
                            "description": "Temperature unit preference",
                            "default": "fahrenheit"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]

        options.agent.think.prompt = (
            "You are a helpful weather assistant with access to current weather data. "
            "Use the get_weather function to provide accurate, up-to-date weather information when users ask about weather conditions. "
            "Always be conversational and provide context about the weather conditions."
        )

        options.greeting = (
            "Hello! I'm your weather assistant with access to current weather data. "
            "I remember our previous conversations and can help you with weather information for any location. "
            "What would you like to know?"
        )

        # Start the connection
        print("🚀 Starting connection with history and function calling enabled...")
        print("Configuration:")
        print(f"  - History enabled: {options.flags.history}")
        print(f"  - Provider: {options.agent.think.provider.type} ({options.agent.think.provider.model})")
        print(f"  - Functions: {len(options.agent.think.functions)} available")
        print(f"  - Initial context: {len(conversation_history)} messages")
        print()

        if dg_connection.start(options) is False:
            print("❌ Failed to start connection")
            return

        print("✅ Connection started successfully!")
        print()
        print("🎯 Expected Features:")
        print("  📚 History events for conversation context")
        print("  📚 History events for function call context")
        print("  🔧 Function calling with weather data")
        print("  📞 Live function calls generate new history events")
        print()
        print("💡 Try saying: 'What's the weather in New York?' or 'How's the weather in Tokyo in Celsius?'")
        print()
        print("Press Enter to stop...")
        input()

        # Close the connection
        dg_connection.finish()
        print("🔌 Connection closed. Demo finished!")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
