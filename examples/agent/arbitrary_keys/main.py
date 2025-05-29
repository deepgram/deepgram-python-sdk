# Copyright 2025 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# Import dependencies and set up the main function
import requests
import wave
import io
import time
import os
import json
import threading
from datetime import datetime

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    AgentKeepAlive,
)
from deepgram.clients.agent.v1.websocket.options import SettingsOptions

def main():
    try:
        # Initialize the Voice Agent
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is not set")
        print(f"API Key found:")

        # Initialize Deepgram client
        config = DeepgramClientOptions(
            options={
                "keepalive": "true",
                # "speaker_playback": "true",
            },
        )
        deepgram = DeepgramClient(api_key, config)
        connection = deepgram.agent.websocket.v("1")
        print("Created WebSocket connection...")

        # 4. Configure the Agent
        options = SettingsOptions()
        # Audio input configuration
        options.audio.input.encoding = "linear16"
        options.audio.input.sample_rate = 24000
        # Audio output configuration
        options.audio.output.encoding = "linear16"
        options.audio.output.sample_rate = 24000
        options.audio.output.container = "wav"
        # Agent configuration
        options.agent.language = "en"
        options.agent.listen.provider.type = "deepgram"
        options.agent.listen.provider.model = "nova-3"
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = "You are a friendly AI assistant."
        options.agent.speak.provider.type = "deepgram"
        options.agent.speak.provider.model = "aura-2-thalia-en"
        options.agent.greeting = "Hello! How can I help you today?"
        options.agent.speak.provider.arbitrary_key = "test"

        def on_welcome(self, welcome, **kwargs):
            print(f"Welcome message received: {welcome}")
            with open("chatlog.txt", 'a') as chatlog:
                chatlog.write(f"Welcome message: {welcome}\n")

        def on_settings_applied(self, settings_applied, **kwargs):
            print(f"Settings applied: {settings_applied}")
            with open("chatlog.txt", 'a') as chatlog:
                chatlog.write(f"Settings applied: {settings_applied}\n")

        def on_error(self, error, **kwargs):
            print(f"Error received: {error}")
            with open("chatlog.txt", 'a') as chatlog:
                chatlog.write(f"Error: {error}\n")

        # Register handlers
        connection.on(AgentWebSocketEvents.Welcome, on_welcome)
        connection.on(AgentWebSocketEvents.SettingsApplied, on_settings_applied)
        connection.on(AgentWebSocketEvents.Error, on_error)
        print("Event handlers registered")

        # Start the connection
        print("Starting WebSocket connection...")
        print(options)
        if not connection.start(options):
            print("Failed to start connection")
            return
        print("WebSocket connection started successfully")

        # Cleanup
        connection.finish()
        print("Finished")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
