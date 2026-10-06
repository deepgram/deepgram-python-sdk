import importlib.util
import sys
import threading
import types
from pathlib import Path

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
