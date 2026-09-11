"""
Example: Taking manual control of turn endings (Listen V2 / Flux)

By default Flux decides when a turn is over. Two connection options plus one control
message let the application decide instead:

    eot_threshold=1.0     suppresses Flux's confidence-based end-of-turn detection
    eot_timeout_ms=60000  pushes out the separate inactivity timeout, which would
                          otherwise still end the turn after a pause
    send_force_end_turn() ends the current turn immediately, whatever the confidence

Both options are needed for full manual control. Setting eot_threshold=1.0 alone still
leaves eot_timeout_ms (default 5000) able to close a turn — a distinction visible only
through TurnInfo.trigger, which reports what actually ended the turn:

    model    Flux's own end-of-turn detection
    manual   a ForceEndTurn message
    timeout  eot_timeout_ms elapsed

This is useful when something outside the audio tells you the speaker is done, such as a
push-to-talk button being released. The connection stays open after a forced end: the
turn index advances and transcription continues.

Note: ForceEndTurn requires server-side enablement and is not available on every
deployment. Where it is not enabled the server replies UNPARSABLE_CLIENT_MESSAGE and
closes the connection; this example reports that and exits.
"""

import os
import threading
import time
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.environment import DeepgramClientEnvironment
from deepgram.listen.v2.types import (
    ListenV2CloseStream,
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)

ListenV2SocketClientResponse = Union[ListenV2Connected, ListenV2TurnInfo, ListenV2FatalError]


def _client_environment() -> DeepgramClientEnvironment:
    """Because ForceEndTurn is gated, this example accepts DEEPGRAM_BASE_URL=wss://<host>
    so it can be pointed at a deployment that has the feature. Defaults to production."""
    base = os.environ.get("DEEPGRAM_BASE_URL")
    if not base:
        return DeepgramClientEnvironment.PRODUCTION
    base = base.replace("https://", "wss://").replace("http://", "ws://")
    https = base.replace("wss://", "https://").replace("ws://", "http://")
    return DeepgramClientEnvironment(base=https, production=base, agent=base, agent_rest=https)


client = DeepgramClient(
    api_key=os.environ.get("DEEPGRAM_API_KEY"), environment=_client_environment()
)

audio_path = Path(__file__).parent / "fixtures" / "audio.wav"

turn_started = threading.Event()
feature_disabled = threading.Event()

try:
    with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="44100",
        # Never end a turn on Flux's own judgement...
        eot_threshold="1.0",
        # ...and do not let the inactivity timeout end it either.
        eot_timeout_ms="60000",
    ) as connection:

        def on_message(message: ListenV2SocketClientResponse) -> None:
            msg_type = getattr(message, "type", None)
            if msg_type == "TurnInfo":
                event = getattr(message, "event", None)
                if event == "StartOfTurn":
                    turn_started.set()
                    print(f"[StartOfTurn] turn={message.turn_index}")
                elif event == "EndOfTurn":
                    trigger = getattr(message, "trigger", None) or "<not sent by this deployment>"
                    print(
                        f"[EndOfTurn]   turn={message.turn_index} trigger={trigger} "
                        f"end_of_turn_confidence={message.end_of_turn_confidence}"
                    )
                    print(f"              transcript: {message.transcript!r}")
            elif getattr(message, "code", None):
                code = message.code
                if code == "UNPARSABLE_CLIENT_MESSAGE":
                    feature_disabled.set()
                print(f"Server error: {code} - {getattr(message, 'description', '')}")

        connection.on(EventType.OPEN, lambda _: print("Connection opened"))
        connection.on(EventType.MESSAGE, on_message)
        connection.on(EventType.ERROR, lambda error: print(f"Connection error: {error}"))

        def send_audio() -> None:
            with open(audio_path, "rb") as f:
                f.read(44)  # skip the WAV header; we declared linear16 above
                audio = f.read(44100 * 2 * 6)  # 6 seconds of 16-bit mono PCM

            chunk_size = 44100 // 10 * 2  # 100ms
            forced = False
            print("Streaming audio...")
            for i in range(0, len(audio), chunk_size):
                try:
                    connection.send_media(audio[i : i + chunk_size])
                except Exception:
                    # A gated deployment closes the socket rather than ignoring the
                    # message, so later sends fail. Stop streaming.
                    break
                time.sleep(0.1)

                # Wait for a turn to actually be open before ending it.
                if not forced and turn_started.is_set():
                    print("Sending ForceEndTurn mid-sentence...")
                    try:
                        connection.send_force_end_turn()
                    except Exception:
                        break
                    forced = True

            time.sleep(2)
            try:
                connection.send_close_stream(ListenV2CloseStream(type="CloseStream"))
            except Exception:
                # Already closed by the server — nothing to signal.
                pass

        sender = threading.Thread(target=send_audio, daemon=True)
        sender.start()

        # This blocks until the connection closes
        connection.start_listening()

    # Reported here rather than in the sender thread: on a gated deployment the server
    # closes the connection, start_listening() returns, and the daemon thread is killed
    # before it could print anything.
    if feature_disabled.is_set():
        print("\nForceEndTurn is not enabled on this deployment.")
        print("Set DEEPGRAM_BASE_URL to a deployment that has the feature.")

except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
