# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from signal import SIGINT, SIGTERM
import asyncio
import time
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    AgentWebSocketEvents,
    SettingsOptions,
)

TTS_TEXT = "Hello, this is a text to speech example using Deepgram."

global warning_notice
warning_notice = True


async def main():
    try:
        loop = asyncio.get_event_loop()

        for signal in (SIGTERM, SIGINT):
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(shutdown(signal, loop, dg_connection)),
            )

        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        config: DeepgramClientOptions = DeepgramClientOptions(
            options={
                "keepalive": "true",
                "microphone_record": "true",
                "speaker_playback": "true",
            },
            # verbose=verboselogs.DEBUG,
        )
        deepgram: DeepgramClient = DeepgramClient("", config)

        # Create a websocket connection to Deepgram
        dg_connection = deepgram.agent.asyncwebsocket.v("1")

        async def on_open(self, open, **kwargs):
            print(f"\n\n{open}\n\n")

        async def on_binary_data(self, data, **kwargs):
            global warning_notice
            if warning_notice:
                print("Received binary data")
                print("You can do something with the binary data here")
                print("OR")
                print(
                    "If you want to simply play the audio, set speaker_playback to true in the options for DeepgramClientOptions"
                )
                warning_notice = False

        async def on_welcome(self, welcome, **kwargs):
            print(f"\n\n{welcome}\n\n")

        async def on_settings_applied(self, settings_applied, **kwargs):
            print(f"\n\n{settings_applied}\n\n")

        async def on_conversation_text(self, conversation_text, **kwargs):
            print(f"\n\n{conversation_text}\n\n")

        async def on_user_started_speaking(self, user_started_speaking, **kwargs):
            print(f"\n\n{user_started_speaking}\n\n")

        async def on_agent_thinking(self, agent_thinking, **kwargs):
            print(f"\n\n{agent_thinking}\n\n")

        async def on_agent_started_speaking(self, agent_started_speaking, **kwargs):
            print(f"\n\n{agent_started_speaking}\n\n")

        async def on_agent_audio_done(self, agent_audio_done, **kwargs):
            print(f"\n\n{agent_audio_done}\n\n")

        async def on_close(self, close, **kwargs):
            print(f"\n\n{close}\n\n")

        async def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        async def on_unhandled(self, unhandled, **kwargs):
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
            AgentWebSocketEvents.AgentStartedSpeaking, on_agent_started_speaking
        )
        dg_connection.on(AgentWebSocketEvents.AgentAudioDone, on_agent_audio_done)
        dg_connection.on(AgentWebSocketEvents.Close, on_close)
        dg_connection.on(AgentWebSocketEvents.Error, on_error)
        dg_connection.on(AgentWebSocketEvents.Unhandled, on_unhandled)

        # connect to websocket
        options = SettingsOptions()
        options.agent.think.provider.type = "open_ai"
        options.agent.think.provider.model = "gpt-4o-mini"
        options.agent.think.prompt = "You are a helpful AI assistant."
        options.greeting = "Hello, this is a text to speech example using Deepgram."
        options.agent.listen.provider.keyterms = ["hello", "goodbye"]
        options.agent.listen.provider.model = "nova-3"
        options.agent.listen.provider.type = "deepgram"
        options.agent.language = "en"


        print("\n\nPress Enter to stop...\n\n")
        if await dg_connection.start(options) is False:
            print("Failed to start connection")
            return

        # wait until cancelled
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            # This block will be executed when the shutdown coroutine cancels all tasks
            pass
        finally:
            await dg_connection.finish()

        print("Finished")

    except ValueError as e:
        print(f"Invalid value encountered: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def shutdown(signal, loop, dg_connection):
    print(f"Received exit signal {signal.name}...")
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")


asyncio.run(main())
