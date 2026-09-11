"""Manual live-API check for listen v2 force-end-turn and the end-of-turn controls.

`send_force_end_turn()` ends the current turn on demand instead of waiting for Flux to
decide. `ListenV2TurnInfo.trigger` then reports *what* ended the turn, and that field is
what makes the end-of-turn controls legible:

    model    Flux's own end-of-turn detection fired
    manual   a ForceEndTurn message ended the turn
    timeout  eot_timeout_ms elapsed after speech

The unit tests mock the websocket, so they pin the frame the SDK sends and nothing about
what the server does with it. This script covers the rest, in three steps:

    1. ForceEndTurn ends an in-progress turn -> trigger="manual", connection survives
    2. eot_threshold=0.7 with trailing silence -> record the observed trigger
    3. eot_threshold=1.0 with trailing silence -> record the observed trigger

`eot_threshold=1.0` does not guarantee that Flux will suppress natural end-of-turn
detection, so the final two checks report server behavior instead of asserting a
manual-only outcome.

ForceEndTurn is gated per deployment. Where it is not enabled the server replies
UNPARSABLE_CLIENT_MESSAGE ("not enabled on this deployment") and closes the connection;
this script reports SKIP rather than failing. Point it at a deployment that has the
feature with DEEPGRAM_BASE_URL.

Requires DEEPGRAM_API_KEY. Run with:

    python tests/manual/listen/v2/force_end_turn/main.py
    DEEPGRAM_BASE_URL=wss://<host> python tests/manual/listen/v2/force_end_turn/main.py
"""

import os
import threading
import time
import wave
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

print("Starting listen v2 force-end-turn manual test")
load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.environment import DeepgramClientEnvironment

SAMPLE_RATE = 44100
CHUNK_BYTES = SAMPLE_RATE // 10 * 2  # 100ms of 16-bit mono PCM

script_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(script_dir, "..", "..", "..", "fixtures", "audio.wav")


def load_audio(speech_seconds: float, silence_seconds: float) -> bytes:
    """Return raw PCM: the first N seconds of the fixture, then digital silence.

    The trailing silence matters — Flux's end-of-turn detection and eot_timeout_ms both
    key off a pause, so continuous speech never exercises either one.
    """
    with wave.open(audio_path, "rb") as src:
        frames = src.readframes(int(speech_seconds * src.getframerate()))
        width = src.getsampwidth() * src.getnchannels()
        silence = b"\x00" * int(silence_seconds * src.getframerate() * width)
    return frames + silence


def _client_environment() -> DeepgramClientEnvironment:
    """TEST ONLY: target a non-prod host by exporting DEEPGRAM_BASE_URL=wss://<host>.
    Defaults to production."""
    base = os.environ.get("DEEPGRAM_BASE_URL")
    if not base:
        return DeepgramClientEnvironment.PRODUCTION
    base = base.replace("https://", "wss://").replace("http://", "ws://")
    https = base.replace("wss://", "https://").replace("ws://", "http://")
    return DeepgramClientEnvironment(base=https, production=base, agent=base, agent_rest=https)


def build_client() -> DeepgramClient:
    environment = _client_environment()
    print(f"  Target: {environment.production}")
    return DeepgramClient(environment=environment)


def run(
    client: DeepgramClient,
    audio: bytes,
    *,
    force: bool = False,
    eot_threshold: Optional[str] = None,
) -> Tuple[List[Any], List[str], bool]:
    """Stream audio, optionally forcing the turn to end, and collect every EndOfTurn."""
    end_of_turns: List[Any] = []
    errors: List[str] = []
    gated = False
    started = threading.Event()

    def on_message(message: Any) -> None:
        nonlocal gated
        msg_type = getattr(message, "type", None)
        if msg_type == "TurnInfo":
            event = getattr(message, "event", None)
            if event == "StartOfTurn":
                started.set()
            elif event == "EndOfTurn":
                end_of_turns.append(message)
        elif getattr(message, "code", None):
            code = getattr(message, "code", "")
            if code == "UNPARSABLE_CLIENT_MESSAGE":
                gated = True
            errors.append(f"{code}: {getattr(message, 'description', '')}")

    kwargs: Dict[str, Any] = {
        "model": "flux-general-en",
        "encoding": "linear16",
        "sample_rate": str(SAMPLE_RATE),
    }
    if eot_threshold is not None:
        kwargs["eot_threshold"] = eot_threshold

    try:
        with client.listen.v2.connect(**kwargs) as connection:
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.ERROR, lambda error: errors.append(f"transport: {error}"))
            threading.Thread(target=connection.start_listening, daemon=True).start()

            forced = False
            for offset in range(0, len(audio), CHUNK_BYTES):
                # A deployment without ForceEndTurn does not just refuse the message, it
                # closes the socket — so every later send raises. Stop streaming instead
                # of letting that escape, so the caller can report the gate.
                try:
                    connection.send_media(audio[offset : offset + CHUNK_BYTES])
                except Exception as e:  # noqa: BLE001
                    if not gated:
                        errors.append(f"send failed: {type(e).__name__}: {e}")
                    break
                time.sleep(0.1)
                # Only force once a turn is genuinely open — forcing before StartOfTurn
                # would have nothing to end.
                if force and not forced and started.is_set():
                    try:
                        connection.send_force_end_turn()
                    except Exception as e:  # noqa: BLE001
                        errors.append(f"send_force_end_turn failed: {type(e).__name__}: {e}")
                        break
                    forced = True
            time.sleep(3)
    except Exception as e:  # noqa: BLE001
        # The context manager's exit closes a socket the server already tore down.
        if not gated:
            errors.append(f"{type(e).__name__}: {e}")

    return end_of_turns, errors, gated


def main() -> None:
    if not os.environ.get("DEEPGRAM_API_KEY"):
        print("  SKIP: DEEPGRAM_API_KEY not set")
        return

    client = build_client()
    speech_only = load_audio(speech_seconds=6, silence_seconds=0)
    speech_then_silence = load_audio(speech_seconds=5, silence_seconds=14)

    print("\n[1/3] ForceEndTurn ends an in-progress turn with trigger='manual'")
    end_of_turns, errors, gated = run(client, speech_only, force=True)
    if gated:
        print("  SKIP: ForceEndTurn is not enabled on this deployment")
        print(f"        ({errors[0]})")
        print("        Set DEEPGRAM_BASE_URL to a deployment that has the feature.")
        return
    if errors:
        raise AssertionError(errors[0])
    triggers = [getattr(t, "trigger", None) for t in end_of_turns]
    assert "manual" in triggers, f"expected trigger='manual', saw {triggers}"
    forced_turn = next(t for t in end_of_turns if getattr(t, "trigger", None) == "manual")
    print(f"  PASS: trigger='manual' (end_of_turn_confidence={forced_turn.end_of_turn_confidence})")
    print(f"        transcript: {forced_turn.transcript!r}")

    for step, threshold in enumerate(("0.7", "1.0"), start=2):
        print(f"\n[{step}/3] eot_threshold={threshold} with trailing silence")
        end_of_turns, errors, _ = run(client, speech_then_silence, eot_threshold=threshold)
        if errors:
            raise AssertionError(errors[0])
        triggers = [getattr(turn, "trigger", None) for turn in end_of_turns]
        print(f"  OBSERVED: EndOfTurn triggers={triggers}")

    print("\nForce-end-turn manual test completed.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"  FAIL: {e}")
        raise SystemExit(1)
