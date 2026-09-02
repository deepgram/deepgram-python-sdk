"""Live microphone transcription with Listen V1.

Install the optional capture dependency first:

    pip install sounddevice

On Linux, the system PortAudio library may also be required. List available
input devices before recording with:

    python examples/18-transcription-live-microphone.py --list-devices

Then set DEEPGRAM_API_KEY and run:

    python examples/18-transcription-live-microphone.py

This example sends 16-bit PCM (linear16) to Deepgram. The sample rate and
channel count in the WebSocket connection always match the microphone stream.
"""

import argparse
import os
import queue
import sys
import threading
from typing import Any, Optional

from dotenv import load_dotenv

from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v1.types import ListenV1Results

load_dotenv()

MAX_QUEUED_CHUNKS = 20


def load_sounddevice() -> Any:
    try:
        import sounddevice  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "Microphone capture requires sounddevice. Install it with: pip install sounddevice"
        ) from exc
    return sounddevice


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe microphone audio with Deepgram Listen V1")
    parser.add_argument("--list-devices", action="store_true", help="list microphone devices and exit")
    parser.add_argument("--device", help="input device name or numeric ID from --list-devices")
    parser.add_argument("--sample-rate", type=int, default=16000, help="input sample rate in Hz (default: 16000)")
    parser.add_argument("--channels", type=int, default=1, help="input channel count (default: 1)")
    parser.add_argument(
        "--block-duration",
        type=float,
        default=0.1,
        help="audio callback block duration in seconds (default: 0.1)",
    )
    parser.add_argument("--language", default="en", help="recognition language (default: en)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        sounddevice = load_sounddevice()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.list_devices:
        print(sounddevice.query_devices())
        return 0

    if not os.getenv("DEEPGRAM_API_KEY"):
        print("Set DEEPGRAM_API_KEY before recording.", file=sys.stderr)
        return 2
    if args.sample_rate <= 0 or args.channels <= 0 or args.block_duration <= 0:
        print("sample-rate, channels, and block-duration must be positive.", file=sys.stderr)
        return 2

    blocksize = int(args.sample_rate * args.block_duration)
    if blocksize == 0:
        print("block-duration is too small for the selected sample rate.", file=sys.stderr)
        return 2

    device: Optional[object] = int(args.device) if args.device and args.device.isdigit() else args.device
    audio_queue: queue.Queue[bytes] = queue.Queue(maxsize=MAX_QUEUED_CHUNKS)
    stop = threading.Event()
    closed = threading.Event()
    sender_errors: list[Exception] = []
    dropped_chunks = 0
    input_status: Optional[str] = None

    def on_message(message: object) -> None:
        if not isinstance(message, ListenV1Results) or not message.is_final:
            return
        if message.channel is None or not message.channel.alternatives:
            return
        transcript = message.channel.alternatives[0].transcript
        if transcript:
            print(f"Transcript: {transcript}")

    def on_error(error: Exception) -> None:
        sender_errors.append(error)
        stop.set()

    def on_close(_: object) -> None:
        closed.set()
        stop.set()

    def on_audio(indata: Any, _frames: int, _time: Any, status: Any) -> None:
        nonlocal dropped_chunks, input_status
        if status:
            input_status = str(status)
        try:
            audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            dropped_chunks += 1

    client = DeepgramClient()
    try:
        with client.listen.v1.connect(
            model="nova-3",
            language=args.language,
            encoding="linear16",
            sample_rate=args.sample_rate,
            channels=args.channels,
            interim_results=True,
            smart_format=True,
        ) as connection:
            connection.on(EventType.OPEN, lambda _: print("Connection opened"))
            connection.on(EventType.MESSAGE, on_message)
            connection.on(EventType.ERROR, on_error)
            connection.on(EventType.CLOSE, on_close)

            listener = threading.Thread(target=connection.start_listening, daemon=True)
            listener.start()

            def send_audio() -> None:
                while not stop.is_set():
                    try:
                        chunk = audio_queue.get(timeout=0.1)
                    except queue.Empty:
                        continue
                    try:
                        connection.send_media(chunk)
                    except Exception as exc:
                        sender_errors.append(exc)
                        stop.set()
                    finally:
                        audio_queue.task_done()

            sender = threading.Thread(target=send_audio, daemon=True)
            sender.start()

            print("Recording... press Ctrl-C to stop.")
            try:
                with sounddevice.RawInputStream(
                    samplerate=args.sample_rate,
                    blocksize=blocksize,
                    device=device,
                    channels=args.channels,
                    dtype="int16",
                    callback=on_audio,
                ):
                    while not stop.wait(0.1):
                        if sender_errors:
                            raise sender_errors[0]
            except KeyboardInterrupt:
                print("\nStopping recording...")
            finally:
                stop.set()
                sender.join(timeout=2)
                if not closed.is_set():
                    try:
                        connection.send_finalize()
                        connection.send_close_stream()
                    except Exception:
                        pass
                listener.join(timeout=5)
            if sender_errors:
                raise sender_errors[0]
    except Exception as exc:
        print(f"Microphone transcription failed: {type(exc).__name__}", file=sys.stderr)
        return 1

    if input_status:
        print(f"Microphone status: {input_status}", file=sys.stderr)
    if dropped_chunks:
        print(f"Warning: dropped {dropped_chunks} microphone chunk(s) because the sender could not keep up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
