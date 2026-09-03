"""
Example: Record a Voice Agent session as JSON

This stores received transcripts, function-call events, and latency reports in
JSON after a successful session. Pass `--output` to choose a persistent
destination; otherwise the example writes a permission-restricted temporary
file. Those fields can contain sensitive data. Apply your application's
consent, redaction, retention, and storage policies before using this pattern
in production.

The recorder does not capture audio or manufacture fields that the server did
not send, such as audio references or unavailable latency measurements.
"""

import argparse
import json
import tempfile
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.agent.v1.types import (
    AgentV1InjectUserMessage,
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V1,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
)
from deepgram.core.events import EventType
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

load_dotenv()

USER_MESSAGE = "What does the first all-female spacewalk symbolize?"


def _serialize_event(message: Any) -> dict[str, Any]:
    if hasattr(message, "model_dump"):
        return message.model_dump(mode="json")
    return json.loads(message.json())


def _write_session_record(recorder: "SessionRecorder", output_path: Path | None) -> Path:
    record = json.dumps(recorder.to_dict(), indent=2)
    if output_path is not None:
        output_path.write_text(record, encoding="utf-8")
        return output_path

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", prefix="voice-agent-session-", suffix=".json", delete=False
    ) as output_file:
        output_file.write(record)
        return Path(output_file.name)


@dataclass
class SessionRecorder:
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ended_at: str | None = None
    conversation: list[dict[str, Any]] = field(default_factory=list)
    function_calls: list[dict[str, Any]] = field(default_factory=list)
    latency_reports: list[dict[str, Any]] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(self, message: Any) -> None:
        if isinstance(message, bytes):
            return

        event = _serialize_event(message)
        with self._lock:
            if event.get("type") == "ConversationText":
                self.conversation.append(event)
            elif event.get("type") in {"FunctionCallRequest", "FunctionCallResponse"}:
                self.function_calls.append(event)
            elif event.get("type") == "LatencyReport":
                self.latency_reports.append(event)

    def finish(self) -> None:
        with self._lock:
            self.ended_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "started_at": self.started_at,
                "ended_at": self.ended_at,
                "conversation": list(self.conversation),
                "function_calls": list(self.function_calls),
                "latency_reports": list(self.latency_reports),
            }


def main() -> None:
    parser = argparse.ArgumentParser(description="Record selected Voice Agent events as JSON.")
    parser.add_argument("--output", type=Path, help="Persistent path for the completed session record.")
    args = parser.parse_args()

    recorder = SessionRecorder()
    settings_applied_event = threading.Event()
    assistant_response_event = threading.Event()

    with DeepgramClient().agent.v1.connect() as agent:
        settings = AgentV1Settings(
            audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
            agent=AgentV1SettingsAgent(
                listen=AgentV1SettingsAgentListen(
                    provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3")
                ),
                think=ThinkSettingsV1(
                    provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini", temperature=0.7),
                    prompt="You are a helpful AI assistant. Keep your responses brief.",
                ),
                speak=SpeakSettingsV1(
                    provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
                ),
            ),
        )

        def on_message(message: Any) -> None:
            recorder.record(message)
            if isinstance(message, bytes):
                return

            if getattr(message, "type", None) == "SettingsApplied":
                settings_applied_event.set()
            elif getattr(message, "type", None) == "ConversationText":
                role = getattr(message, "role", "unknown")
                print(f"[{role}] {message.content}")
                if role == "assistant":
                    assistant_response_event.set()

        agent.on(EventType.MESSAGE, on_message)
        agent.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

        listener = threading.Thread(target=agent.start_listening, daemon=True)
        listener.start()

        agent.send_settings(settings)
        if not settings_applied_event.wait(10):
            raise TimeoutError("Timed out waiting for agent settings to apply")

        agent.send_inject_user_message(AgentV1InjectUserMessage(content=USER_MESSAGE))
        if not assistant_response_event.wait(30):
            raise TimeoutError("Timed out waiting for the agent to respond")

        time.sleep(2)

    recorder.finish()
    output_path = _write_session_record(recorder, args.output)
    print(f"Wrote completed session record to {output_path}")


if __name__ == "__main__":
    main()
