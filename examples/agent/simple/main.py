# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
    FunctionCallRequest,
    FunctionCallResponse,
)

# Add debug prints for imports
print("Checking imports...")
try:
    from deepgram import FunctionCallRequest

    print("Successfully imported FunctionCallRequest")
except ImportError as e:
    print(f"Failed to import FunctionCallRequest: {e}")

try:
    from deepgram import FunctionCallResponse

    print("Successfully imported FunctionCallResponse")
except ImportError as e:
    print(f"Failed to import FunctionCallResponse: {e}")

global warning_notice
warning_notice = True


def main():
    try:
        print("Starting main function...")
        config: DeepgramClientOptions = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "microphone_record": "true",
                "speaker_playback": "true",
            },
            # verbose=verboselogs.DEBUG,
        )
        print("Created DeepgramClientOptions...")

        deepgram: DeepgramClient = DeepgramClient("", config)
        print("Created DeepgramClient...")

        dg_connection = deepgram.agent.websocket.v("1")
        print("Created WebSocket connection...")

        def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        def on_binary_data(self, data, **kwargs):
            global warning_notice
            if warning_notice:
                print("Received binary data")
                print("You can do something with the binary data here")
                print("OR")
                print(
                    "If you want to simply play the audio, set speaker_playback to true in the options for DeepgramClientOptions"
                )
                warning_notice = False

        def on_welcome(self, welcome, **kwargs):
            print(f"\n\n{welcome}\n\n")

        def on_settings_applied(self, settings_applied, **kwargs):
            print(f"\n\n{settings_applied}\n\n")

        def on_conversation_text(self, conversation_text, **kwargs):
            print(f"\n\n{conversation_text}\n\n")

        def on_user_started_speaking(self, user_started_speaking, **kwargs):
            print(f"\n\n{user_started_speaking}\n\n")

        def on_agent_thinking(self, agent_thinking, **kwargs):
            print(f"\n\n{agent_thinking}\n\n")

        def on_function_call_request(
            self, function_call_request: FunctionCallRequest, **kwargs
        ):
            print(f"\n\nFunction Call Request: {function_call_request}\n\n")
            try:
                response = FunctionCallResponse(
                    function_call_id=function_call_request.function_call_id,
                    output="Function response here",
                )
                dg_connection.send_function_call_response(response)
            except Exception as e:
                print(f"Error in function call: {e}")

        def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
            print(f"\n\n{agent_started_speaking}\n\n")

        def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print(f"\n\n{agent_audio_done}\n\n")

        def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"\n\n{unhandled}\n\n")

        dg_connection.on(AgentWebSocketEvents.Open, on_open)
        dg_connection.on(AgentWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
        dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
        dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
        dg_connection.on(
            AgentWebSocketEvents.UserStartedSpeaking, on_user_started_speaking
        )
        dg_connection.on(AgentWebSocketEvents.AgentThinking, on_agent_thinking)
        dg_connection.on(
            AgentWebSocketEvents.FunctionCallRequest, on_function_call_request
        )
        dg_connection.on(
            AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking
        )
        dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        dg_connection.on(AgentWebSocketEvents.Close, on_close)
        dg_connection.on(AgentWebSocketEvents.Error, on_error)
        dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

        # connect to websocket
        options: SettingsOptions = SettingsOptions()
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = "You are a helpful AI assistant."
        options.greeting = "Hello, this is a text to speech example using Deepgram."
        options.agent.listen.provider.keyterms = ["hello", "goodbye"]
        options.agent.listen.provider.model = "nova-3"
        options.agent.listen.provider.type = "deepgram"
        options.agent.language = "en"
        if dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        print("\n\nPress Enter to stop...\n\n")
        input()

        # Close the connection
        dg_connection.finish()

        print("Finished")

    except ImportError as e:
        print(f"Import Error Details: {e}")
        print(f"Error occurred in module: {getattr(e, 'name', 'unknown')}")
        print(f"Path that failed: {getattr(e, 'path', 'unknown')}")
    except Exception as e:
        print(f"Unexpected error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Error occurred in: {__file__}")


if __name__ == "__main__":
    main()
