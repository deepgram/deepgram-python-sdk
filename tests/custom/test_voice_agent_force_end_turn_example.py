import importlib.util
import sys
import threading
import types
from pathlib import Path

import pytest

EXAMPLE_PATH = Path(__file__).parents[2] / "examples" / "32-voice-agent-force-end-turn.py"


class RejectionDuringGraceWait(threading.Event):
    def __init__(self):
        super().__init__()
        self.wait_calls = 0

    def wait(self, _timeout):
        self.wait_calls += 1
        self.set()
        return True


def load_example(monkeypatch):
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv)

    spec = importlib.util.spec_from_file_location("voice_agent_force_end_turn_example", EXAMPLE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_audio_done_waits_for_late_force_end_turn_rejection(monkeypatch):
    example = load_example(monkeypatch)
    agent_finished = threading.Event()
    force_end_turn_rejected = RejectionDuringGraceWait()
    agent_finished.set()

    assert not example.wait_for_force_end_turn_outcome(
        agent_finished,
        force_end_turn_rejected,
        timeout_seconds=1,
    )
    assert force_end_turn_rejected.wait_calls == 1


def test_force_end_turn_rejection_leaves_context_before_raising(monkeypatch):
    example = load_example(monkeypatch)

    class FakeAgent:
        def __init__(self):
            self.message_handler = None
            self.user_started = False

        def on(self, event, callback):
            if event == example.EventType.MESSAGE:
                self.message_handler = callback

        def start_listening(self):
            pass

        def send_settings(self, _settings):
            pass

        def send_media(self, _audio):
            if not self.user_started:
                self.user_started = True
                self.message_handler(types.SimpleNamespace(type="UserStartedSpeaking"))

        def send_force_end_turn(self):
            self.message_handler(types.SimpleNamespace(type="AgentAudioDone"))
            self.message_handler(
                types.SimpleNamespace(
                    type="Warning",
                    code="FORCE_END_TURN_UNSUPPORTED",
                    description="ForceEndTurn is unsupported",
                )
            )

    class FakeAgentContext:
        def __init__(self):
            self.agent = FakeAgent()
            self.exit_exception_type = None

        def __enter__(self):
            return self.agent

        def __exit__(self, exc_type, _exc_value, _traceback):
            self.exit_exception_type = exc_type

    context = FakeAgentContext()

    class FakeDeepgramClient:
        def __init__(self):
            self.agent = types.SimpleNamespace(v1=types.SimpleNamespace(connect=lambda: context))

    monkeypatch.setattr(example, "DeepgramClient", FakeDeepgramClient)

    with pytest.raises(RuntimeError, match="FORCE_END_TURN_UNSUPPORTED"):
        example.main()

    assert context.exit_exception_type is None
