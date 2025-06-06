# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import time
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    AgentKeepAlive,
)
from deepgram.clients.agent.v1.websocket.options import (
    SettingsOptions,
    AWSPollyCredentials,
    Endpoint,
    SpeakProvider,
)

def main():
    try:
        # Initialize the Voice Agent
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is not set")
        print("API Key found")

        # Initialize Deepgram client
        config = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "microphone_record": "true",
                "speaker_playback": "true",
            },
        )
        deepgram = DeepgramClient(api_key, config)
        connection = deepgram.agent.websocket.v("1")
        print("Created WebSocket connection...")

        # Define event handlers
        def on_open(self, open_response, **kwargs):
            print(f"\nConnection opened: {open_response}\n")

        def on_welcome(self, welcome, **kwargs):
            print(f"\nWelcome message: {welcome}\n")

        def on_settings_applied(self, settings_applied, **kwargs):
            print(f"\nSettings applied: {settings_applied}\n")

        def on_conversation_text(self, conversation_text, **kwargs):
            print(f"\nConversation: {conversation_text}\n")

        def on_user_started_speaking(self, user_started_speaking, **kwargs):
            print(f"\nUser started speaking: {user_started_speaking}\n")

        def on_agent_thinking(self, agent_thinking, **kwargs):
            print(f"\nAgent is thinking: {agent_thinking}\n")

        def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
            print(f"\nAgent started speaking: {agent_started_speaking}\n")

        def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print(f"\nAgent finished speaking: {agent_audio_done}\n")

        def on_error(self, error, **kwargs):
            print(f"\nError occurred: {error}\n")

        def on_close(self, close, **kwargs):
            print(f"\nConnection closed: {close}\n")

        # Register event handlers
        connection.on(AgentWebSocketEvents.Open, on_open)
        connection.on(AgentWebSocketEvents.Welcome, on_welcome)
        connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
        connection.on(AgentWebSocketEvents.ConversationText, on_conversation_text)
        connection.on(AgentWebSocketEvents.UserStartedSpeaking, on_user_started_speaking)
        connection.on(AgentWebSocketEvents.AgentThinking, on_agent_thinking)
        connection.on(AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking)
        connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        connection.on(AgentWebSocketEvents.Error, on_error)
        connection.on(AgentWebSocketEvents.Close, on_close)

        # Configure the Agent with AWS Polly
        options = SettingsOptions()

        # [Previous configuration code remains the same...]
        # Audio input configuration
        options.audio.input.encoding = "linear16"
        options.audio.input.sample_rate = 24000

        # Audio output configuration
        options.audio.output.encoding = "mp3"  # AWS Polly outputs MP3
        options.audio.output.sample_rate = 24000
        options.audio.output.container = "mp3"

        # Agent configuration
        options.agent.language = "en"

        # Configure Listen provider (Deepgram)
        options.agent.listen.provider.type = "deepgram"
        options.agent.listen.provider.model = "nova-3"
        options.agent.listen.provider.keyterms = ["hello", "goodbye"]  # Optional keyterms

        # Configure Think provider (OpenAI)
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = "You are a friendly AI assistant."

        # Configure Speak provider (AWS Polly)
        options.agent.speak.provider = SpeakProvider(
            type="aws_polly",
            voice="Matthew",
            language_code="en-US",
            engine="standard",
            credentials=AWSPollyCredentials(
                type="IAM",
                region="us-east-1",
                access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
                secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            )
        )

        # Configure AWS Polly endpoint
        options.agent.speak.endpoint = Endpoint(
            url="https://polly.us-east-1.amazonaws.com/v1/speech" # use your correct AWS region
        )

        # Optional greeting message
        options.agent.greeting = "Hello! I'm your AI assistant powered by AWS Polly."

        # Start the connection
        print("Starting connection...")
        if not connection.start(options):
            print("Failed to start connection")
            return

        print("Connection started successfully!")
        print("Press Ctrl+C to exit...")

        # Keep the connection alive
        while True:
            time.sleep(1)
            keep_alive = AgentKeepAlive()
            connection.send(keep_alive.to_json())

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.finish()
            print("Connection closed")

if __name__ == "__main__":
    main()