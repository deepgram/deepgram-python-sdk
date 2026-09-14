"""
Example: Force an active Voice Agent turn to end.

ForceEndTurn requires a Deepgram V2 (Flux) listen provider. It sends the
control message after the server reports UserStartedSpeaking, then waits for
the agent response. The example streams the first two seconds of the bundled
WAV fixture and does not capture microphone audio.
"""

import threading
import time
from pathlib import Path

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V2,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
)
from deepgram.core.events import EventType
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

load_dotenv()

AUDIO_PATH = Path(__file__).parent / "fixtures" / "audio.wav"


def main() -> None:
    user_started = threading.Event()
    agent_finished = threading.Event()

    settings = AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=44100)),
        agent=AgentV1SettingsAgent(
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider_V2(type="deepgram", model="flux-general-en")
            ),
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini"),
                prompt="Reply briefly.",
            ),
            speak=SpeakSettingsV1(
                provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
            ),
        ),
    )

    with DeepgramClient().agent.v1.connect() as agent:

        def on_message(message: object) -> None:
            message_type = getattr(message, "type", None)
            if message_type == "UserStartedSpeaking":
                user_started.set()
                print("UserStartedSpeaking received")
            elif message_type == "ConversationText":
                print(f"[{message.role}] {message.content}")
            elif message_type == "AgentAudioDone":
                agent_finished.set()
                print("AgentAudioDone received")
            elif message_type in {"Warning", "Error"}:
                print(f"{message_type}: {message.code} - {message.description}")

        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.ERROR, lambda error: print(f"Connection error: {error}"))
        threading.Thread(target=agent.start_listening, daemon=True).start()

        agent.send_settings(settings)
        with AUDIO_PATH.open("rb") as audio_file:
            audio_file.read(44)
            audio = audio_file.read(44100 * 2 * 2)

        for start in range(0, len(audio), 44100 // 10 * 2):
            agent.send_media(audio[start : start + 44100 // 10 * 2])
            time.sleep(0.1)
            if user_started.is_set():
                break

        if not user_started.is_set():
            raise TimeoutError("Timed out waiting for UserStartedSpeaking")

        print("Sending ForceEndTurn")
        agent.send_force_end_turn()
        if not agent_finished.wait(15):
            raise TimeoutError("Timed out waiting for the agent response")


if __name__ == "__main__":
    main()
