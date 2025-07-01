# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

"""
Example demonstrating Voice Agent with multiple TTS providers for fallback support.

This example shows how to configure multiple TTS providers in an array format,
allowing the agent to automatically fall back to alternative providers if the
primary provider fails or is unavailable.
"""

from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
    Speak,
    Endpoint,
    Header,
)

global warning_notice
warning_notice = True


def main():
    try:
        print("Starting Voice Agent with Fallback TTS Providers...")

        config: DeepgramClientOptions = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "microphone_record": "true",
                "speaker_playback": "true",
            },
            verbose=verboselogs.SPAM,
        )

        deepgram: DeepgramClient = DeepgramClient("", config)
        dg_connection = deepgram.agent.websocket.v("1")

        def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        def on_binary_data(self, data, **kwargs):
            global warning_notice
            if warning_notice:
                print("Received binary data from TTS provider")
                print("Audio will be played automatically with speaker_playback=true")
                warning_notice = False

        def on_welcome(self, welcome, **kwargs):
            print(f"\n\n{welcome}\n\n")

        def on_settings_applied(self, settings_applied, **kwargs):
            print(f"\n\nSettings Applied - Multiple TTS providers configured:\n{settings_applied}\n\n")

        def on_conversation_text(self, conversation_text, **kwargs):
            print(f"\n\n{conversation_text}\n\n")

        def on_user_started_speaking(self, user_started_speaking, **kwargs):
            print(f"\n\n{user_started_speaking}\n\n")

        def on_agent_thinking(self, agent_thinking, **kwargs):
            print(f"\n\n{agent_thinking}\n\n")

        def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
            print(f"\n\n{agent_started_speaking}\n\n")

        def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print(f"\n\n{agent_audio_done}\n\n")

        def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\nError (may trigger TTS fallback): {error}\n\n")

        def on_unhandled(self, unhandled, **kwargs):
            print(f"\n\n{unhandled}\n\n")

        # Register event handlers
        dg_connection.on(AgentWebSocketEvents.Open, on_open)
        dg_connection.on(AgentWebSocketEvents.AudioData, on_binary_data)
        dg_connection.on(AgentWebSocketEvents.Welcome, on_welcome)
        dg_connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
        dg_connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
        dg_connection.on(AgentWebSocketEvents.UserStartedSpeaking, on_user_started_speaking)
        dg_connection.on(AgentWebSocketEvents.AgentThinking, on_agent_thinking)
        dg_connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
        dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        dg_connection.on(AgentWebSocketEvents.Close, on_close)
        dg_connection.on(AgentWebSocketEvents.Error, on_error)
        dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

        # Configure TTS providers for fallback support
        print("Configuring TTS providers with fallback...")

        # Primary TTS Provider: Deepgram Aura
        primary_tts = Speak()
        primary_tts.provider.type = "deepgram"
        primary_tts.provider.model = "aura-2-zeus-en"

        # Fallback TTS Provider: OpenAI TTS
        fallback_tts = Speak()
        fallback_tts.provider.type = "open_ai"
        fallback_tts.provider.model = "tts-1"
        fallback_tts.provider.voice = "shimmer"

        # Configure custom endpoint for OpenAI
        fallback_tts.endpoint = Endpoint()
        fallback_tts.endpoint.url = "https://api.openai.com/v1/audio/speech"
        fallback_tts.endpoint.headers = [
            Header(key="authorization", value="Bearer {{OPENAI_API_KEY}}")
        ]

        # Configure agent settings
        options: SettingsOptions = SettingsOptions()
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = (
            "You are a helpful AI assistant with fallback TTS providers for reliable speech output. "
            "If one provider fails, another will automatically take over."
        )
        options.agent.listen.provider.type = "deepgram"
        options.agent.listen.provider.model = "nova-3"
        options.agent.listen.provider.keyterms = ["hello", "goodbye", "fallback"]

        # Configure multiple TTS providers (array format)
        options.agent.speak = [primary_tts, fallback_tts]

        options.agent.language = "en"
        options.greeting = (
            "Hello! I'm your AI assistant with fallback TTS providers. "
            "I can automatically switch between Deepgram and OpenAI for reliable voice output."
        )

        print("TTS Providers configured:")
        print(f"1. Primary: {primary_tts.provider.type} - {primary_tts.provider.model}")
        print(f"2. Fallback: {fallback_tts.provider.type} - {fallback_tts.provider.model}")

        # Start the connection
        if dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        print("\n\n=== Voice Agent with Fallback TTS Started ===")
        print("The agent is now running with primary and fallback TTS providers.")
        print("If the primary provider fails, it will automatically fall back to the secondary.")
        print("Press Enter to stop...\n\n")
        input()

        # Close the connection
        dg_connection.finish()
        print("Finished - Fallback TTS example completed")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()