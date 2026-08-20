"""Async manual live-API check for listen v2 force-end-turn.

The async client has its own `send_force_end_turn()` on `AsyncListenV2SocketClient`, so it
needs its own live check — the sync script next door cannot cover this path. This mirrors
step 1 of `main.py`: force an in-progress turn to end and confirm the resulting EndOfTurn
reports trigger="manual". See `main.py` for the full end-of-turn control matrix.

ForceEndTurn is gated per deployment; where it is not enabled this reports SKIP rather
than failing. Point it at a deployment that has the feature with DEEPGRAM_BASE_URL.

Requires DEEPGRAM_API_KEY. Run with:

    python tests/manual/listen/v2/force_end_turn/async.py
    DEEPGRAM_BASE_URL=wss://<host> python tests/manual/listen/v2/force_end_turn/async.py
"""

import asyncio
import os
import wave
from typing import Any, List

from dotenv import load_dotenv

print("Starting async listen v2 force-end-turn manual test")
load_dotenv()

from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.environment import DeepgramClientEnvironment

SAMPLE_RATE = 44100
CHUNK_BYTES = SAMPLE_RATE // 10 * 2  # 100ms of 16-bit mono PCM

script_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(script_dir, "..", "..", "..", "fixtures", "audio.wav")


def _client_environment() -> DeepgramClientEnvironment:
    """TEST ONLY: target a non-prod host by exporting DEEPGRAM_BASE_URL=wss://<host>.
    Defaults to production."""
    base = os.environ.get("DEEPGRAM_BASE_URL")
    if not base:
        return DeepgramClientEnvironment.PRODUCTION
    base = base.replace("https://", "wss://").replace("http://", "ws://")
    https = base.replace("wss://", "https://").replace("ws://", "http://")
    return DeepgramClientEnvironment(base=https, production=base, agent=base, agent_rest=https)


async def main() -> None:
    if not os.environ.get("DEEPGRAM_API_KEY"):
        print("  SKIP: DEEPGRAM_API_KEY not set")
        return

    environment = _client_environment()
    print(f"  Target: {environment.production}")
    client = AsyncDeepgramClient(environment=environment)

    with wave.open(audio_path, "rb") as src:
        audio = src.readframes(int(6 * src.getframerate()))

    end_of_turns: List[Any] = []
    errors: List[str] = []
    gated = False
    started = asyncio.Event()

    def on_message(message: Any) -> None:
        nonlocal gated
        if getattr(message, "type", None) == "TurnInfo":
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

    print("\n[1/1] ForceEndTurn ends an in-progress turn with trigger='manual'")
    try:
        async with client.listen.v2.connect(
            model="flux-general-en", encoding="linear16", sample_rate=str(SAMPLE_RATE)
        ) as connection:
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.ERROR, lambda error: errors.append(f"transport: {error}"))
            listener = asyncio.create_task(connection.start_listening())

            forced = False
            for offset in range(0, len(audio), CHUNK_BYTES):
                # A gated deployment closes the socket rather than ignoring the message,
                # so later sends raise. Stop streaming so the gate can be reported.
                try:
                    await connection.send_media(audio[offset : offset + CHUNK_BYTES])
                except Exception as e:  # noqa: BLE001
                    if not gated:
                        errors.append(f"send failed: {type(e).__name__}: {e}")
                    break
                await asyncio.sleep(0.1)
                if not forced and started.is_set():
                    try:
                        await connection.send_force_end_turn()
                    except Exception as e:  # noqa: BLE001
                        errors.append(f"send_force_end_turn failed: {type(e).__name__}: {e}")
                        break
                    forced = True

            await asyncio.sleep(3)
            listener.cancel()
    except Exception as e:  # noqa: BLE001
        if not gated:
            errors.append(f"{type(e).__name__}: {e}")

    if gated:
        print("  SKIP: ForceEndTurn is not enabled on this deployment")
        print(f"        ({errors[0]})")
        print("        Set DEEPGRAM_BASE_URL to a deployment that has the feature.")
        return
    if errors:
        print(f"  FAIL: {errors[0]}")
        raise SystemExit(1)

    triggers = [getattr(t, "trigger", None) for t in end_of_turns]
    if "manual" not in triggers:
        print(f"  FAIL: expected trigger='manual', saw {triggers}")
        raise SystemExit(1)

    forced_turn = next(t for t in end_of_turns if getattr(t, "trigger", None) == "manual")
    print(f"  PASS: trigger='manual' (end_of_turn_confidence={forced_turn.end_of_turn_confidence})")
    print(f"        transcript: {forced_turn.transcript!r}")
    print("\nAsync force-end-turn manual test completed.")


if __name__ == "__main__":
    asyncio.run(main())
