"""
Example: Production-Grade Live Transcription with Automatic Reconnection

Long-running streaming transcription has to survive the network: sockets drop,
servers restart, and load balancers time idle connections out. This example
shows the production patterns Deepgram recommends for resilient streaming:

- Exponential backoff with full jitter and a retry cap
- Distinguishing reconnect-worthy close codes from normal or fatal closure
- Buffering audio while disconnected and resuming after reconnect
- Re-applying the original connection options on every reconnect
- Offsetting timestamps so downstream consumers see one continuous stream
- Clean shutdown via CloseStream

It streams a pre-recorded audio file in real-time chunks to simulate a live
microphone feed, and deliberately severs the TCP connection mid-stream to
demonstrate recovery. Run it with DEEPGRAM_API_KEY set:

    python examples/17-transcription-live-reconnect.py

See also: https://developers.deepgram.com/docs/recovering-from-connection-errors-and-timeouts-when-live-streaming-audio
"""

import collections
import os
import random
import socket
import sys
import threading
import time
import wave
from typing import Deque, List, Optional, Tuple, Union

from dotenv import load_dotenv

load_dotenv()

from websockets.exceptions import ConnectionClosed, InvalidStatus

from deepgram import DeepgramClient
from deepgram.core.api_error import ApiError
from deepgram.core.events import EventType
from deepgram.listen.v1.socket_client import V1SocketClient
from deepgram.listen.v1.types import (
    ListenV1Metadata,
    ListenV1Results,
    ListenV1SpeechStarted,
    ListenV1UtteranceEnd,
)

ListenV1SocketClientResponse = Union[ListenV1Results, ListenV1Metadata, ListenV1UtteranceEnd, ListenV1SpeechStarted]

# --- Reconnection policy -----------------------------------------------------

# Exponential backoff with full jitter: sleep a random amount between 0 and
# min(MAX_DELAY, BASE_DELAY * 2^attempt). Jitter prevents a fleet of clients
# from reconnecting in lockstep after a shared outage (a "thundering herd").
BASE_DELAY_SECONDS = 1.0
MAX_DELAY_SECONDS = 10.0
MAX_RETRIES = 5

# Close codes worth reconnecting for: the failure is transient, so the same
# request is likely to succeed on a fresh connection.
#   1006 - abnormal closure (network dropped, no close frame received)
#   1011 - server error, including Deepgram's NET-0000/NET-0001 data timeouts
#   1012 - service restart
#   1013 - try again later (server overloaded)
RETRYABLE_CLOSE_CODES = {1006, 1011, 1012, 1013}

# Normal closure codes: expected when either side shuts down on purpose.
NORMAL_CLOSE_CODES = {1000, 1001}

# Anything else (1002/1003/1007/1008, 4xxx policy codes) means the request
# itself was rejected — bad audio, bad parameters, or a policy violation.
# Retrying the identical request would just fail the same way.

# --- Audio buffering policy --------------------------------------------------

CHUNK_SECONDS = 0.25  # size of each audio chunk sent to Deepgram
MAX_BUFFER_SECONDS = 60.0  # cap on audio held while disconnected

# Deepgram accepts audio at up to 1.25x real-time, so a large backlog drains
# slowly. Capping the buffer bounds memory and catch-up delay; when the cap is
# hit we drop the oldest audio and accept a gap in the transcript.


class ResilientTranscriber:
    """Streams audio to Deepgram Listen V1, reconnecting through failures.

    A producer thread paces audio chunks into a buffer in real time,
    disconnected or not. The main thread runs one websocket session at a
    time: it drains the buffer into the socket, and when a session dies it
    classifies the failure, backs off, and reconnects with the original
    connection options. Audio that arrived during the gap is still in the
    buffer, so transcription resumes where it left off.
    """

    def __init__(self, client: DeepgramClient, audio_path: str):
        self._client = client
        self._audio_path = audio_path

        with wave.open(audio_path, "rb") as wav:
            if wav.getsampwidth() != 2:
                raise ValueError("This example expects 16-bit PCM audio (linear16)")
            self._sample_rate = wav.getframerate()
            self._channels = wav.getnchannels()

        # The original connection options, stored once and re-applied verbatim
        # on every reconnect so a recovered session behaves like the first.
        self._connect_options = {
            "model": "nova-3",
            "encoding": "linear16",
            "sample_rate": self._sample_rate,
            "channels": self._channels,
            "smart_format": True,
        }

        self._buffer: Deque[bytes] = collections.deque()
        self._producer_done = threading.Event()
        self._stop = threading.Event()

        # Each new connection restarts Deepgram's timestamps at zero. We track
        # where the previous session ended and offset every result by it, so
        # timestamps stay continuous across reconnects.
        self._time_offset = 0.0
        self._last_end = 0.0

        self.active_socket: Optional[V1SocketClient] = None
        self.transcripts: List[str] = []
        self.reconnects = 0

    # --- audio producer -------------------------------------------------

    def _produce_audio(self) -> None:
        """Pace the audio file into the buffer at real-time speed.

        This stands in for a live audio source (microphone, telephony leg,
        browser stream). It never touches the network: whether the websocket
        is up or down, audio lands in the buffer, which is what preserves it
        across a reconnect gap.
        """
        chunk_frames = int(self._sample_rate * CHUNK_SECONDS)
        with wave.open(self._audio_path, "rb") as wav:
            while not self._stop.is_set():
                frames = wav.readframes(chunk_frames)
                if not frames:
                    break
                if self._buffered_seconds() >= MAX_BUFFER_SECONDS:
                    try:
                        self._buffer.popleft()
                        print("Buffer full: dropped oldest chunk (transcript will gap)")
                    except IndexError:
                        pass  # the sender drained the buffer in the meantime
                self._buffer.append(frames)
                time.sleep(CHUNK_SECONDS)
        self._producer_done.set()

    def _buffered_seconds(self) -> float:
        # len() of a deque is atomic, so this is safe to call from any thread
        # while others append or pop. Chunks are fixed-size, so the count is
        # an accurate proxy for duration.
        return len(self._buffer) * CHUNK_SECONDS

    # --- event handlers ---------------------------------------------------

    def _on_message(self, message: ListenV1SocketClientResponse) -> None:
        if isinstance(message, ListenV1Results):
            # Offset this session's timestamps by where the last session ended.
            start = self._time_offset + message.start
            self._last_end = start + message.duration
            if message.channel.alternatives:
                transcript = message.channel.alternatives[0].transcript
                if transcript:
                    self.transcripts.append(transcript)
                    print(f"[{start:6.2f}s] {transcript}")
        elif isinstance(message, ListenV1Metadata):
            print(f"Session summary received (request_id: {message.request_id})")

    # --- one websocket session -------------------------------------------

    def _run_session(self) -> Tuple[str, str]:
        """Run a single connection until it finishes or fails.

        Returns ("finished", detail) when the stream completed and was closed
        cleanly, ("retry", detail) when the connection was lost and is worth
        re-establishing, or ("fatal", detail) when retrying would be futile.
        """
        errors: List[Exception] = []
        closed = threading.Event()

        self._time_offset = self._last_end

        with self._client.listen.v1.connect(**self._connect_options) as connection:
            self.active_socket = connection
            connection.on(EventType.OPEN, lambda _: print("Connection open"))
            connection.on(EventType.MESSAGE, self._on_message)
            connection.on(EventType.ERROR, errors.append)
            connection.on(EventType.CLOSE, lambda _: closed.set())

            # start_listening() blocks while it dispatches incoming messages,
            # so it runs in a thread while this thread sends audio.
            listener = threading.Thread(target=connection.start_listening, daemon=True)
            listener.start()

            try:
                while not self._stop.is_set():
                    if closed.is_set():
                        # The socket died while we were between sends.
                        break
                    if not self._buffer:
                        if self._producer_done.is_set():
                            break  # all audio sent
                        time.sleep(0.05)
                        continue
                    chunk = self._buffer.popleft()
                    try:
                        connection.send_media(chunk)
                    except Exception:
                        # The send failed, so this chunk never made it out.
                        # Put it back so the next session resends it. (Audio
                        # already handed to a dying socket may still be lost;
                        # exactly-once delivery needs server-side dedupe.)
                        self._buffer.appendleft(chunk)
                        raise
            except KeyboardInterrupt:
                print("\nInterrupted: closing stream cleanly...")
                self._stop.set()

            if not closed.is_set() and not errors:
                # Clean shutdown: CloseStream tells Deepgram to flush any
                # remaining transcription and close the connection with a
                # normal close code. Waiting for CLOSE collects those final
                # results instead of discarding them.
                connection.send_close_stream()
                closed.wait(timeout=10)

        self.active_socket = None
        listener.join(timeout=5)

        if self._stop.is_set() or (not errors and self._producer_done.is_set() and not self._buffer):
            return ("finished", "stream complete")
        return self._classify_disconnect(errors)

    def _classify_disconnect(self, errors: List[Exception]) -> Tuple[str, str]:
        """Decide whether a lost connection is worth retrying."""
        if not errors:
            return ("retry", "server closed the connection mid-stream")
        exc = errors[0]
        if isinstance(exc, ConnectionClosed):
            code = exc.rcvd.code if exc.rcvd is not None else 1006
            if code in RETRYABLE_CLOSE_CODES:
                return ("retry", f"close code {code} (transient failure)")
            if code in NORMAL_CLOSE_CODES:
                return ("retry", f"close code {code} (normal closure, but audio remains)")
            # Non-retryable: the request itself was rejected, so an identical
            # retry would fail the same way.
            reason = exc.rcvd.reason if exc.rcvd is not None else ""
            return ("fatal", f"close code {code}: {reason or 'request rejected'}")
        # Network-level errors (OSError, timeouts) are transient by nature.
        return ("retry", f"{type(exc).__name__}: {exc}")

    # --- reconnection loop -----------------------------------------------

    def run(self) -> None:
        producer = threading.Thread(target=self._produce_audio, daemon=True)
        producer.start()

        attempt = 0
        while True:
            had_results = len(self.transcripts)
            try:
                outcome, detail = self._run_session()
            except (ApiError, InvalidStatus) as err:
                # A rejected handshake surfaces as ApiError, or as the
                # websockets library's InvalidStatus depending on the
                # installed websockets version.
                status = err.status_code if isinstance(err, ApiError) else err.response.status_code
                if status in (401, 403):
                    # Bad credentials never fix themselves — do not retry.
                    raise RuntimeError(f"Handshake rejected with HTTP {status}: check DEEPGRAM_API_KEY") from err
                outcome, detail = "retry", f"handshake failed (status {status})"
            except OSError as err:
                outcome, detail = "retry", f"network error: {err}"

            if outcome == "finished":
                print(f"Done: {detail}")
                return
            if outcome == "fatal":
                raise RuntimeError(f"Connection closed with a non-retryable error: {detail}")

            # A session that produced results was healthy, so its failure is
            # a fresh incident: reset the backoff schedule.
            if len(self.transcripts) > had_results:
                attempt = 0
            attempt += 1
            if attempt > MAX_RETRIES:
                raise RuntimeError(f"Giving up after {MAX_RETRIES} reconnect attempts")

            delay = random.uniform(0.0, min(MAX_DELAY_SECONDS, BASE_DELAY_SECONDS * 2 ** (attempt - 1)))
            print(f"Connection lost: {detail}")
            print(f"Backing off {delay:.1f}s before reconnect attempt {attempt}/{MAX_RETRIES}...")
            time.sleep(delay)
            self.reconnects += 1
            print(f"Reconnecting with {self._buffered_seconds():.1f}s of audio buffered during the gap")
            # Deepgram closes new connections that stay silent for ~10s, so
            # the buffered audio must start flowing promptly — which the
            # session loop does as soon as the socket opens.


def force_network_drop(transcriber: ResilientTranscriber, after_seconds: float) -> None:
    """DEMO ONLY: sever the TCP socket to simulate a mid-stream network failure.

    This reaches into SDK internals to yank the connection out from under the
    client, the same way a dropped network would. Never do this in production
    code — it exists so this example can demonstrate recovery on demand.
    """
    time.sleep(after_seconds)
    connection = transcriber.active_socket
    if connection is None:
        return
    print("\n--- DEMO: severing the TCP connection to simulate a network failure ---\n")
    try:
        connection._websocket.socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass  # already closed


def main() -> int:
    audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "audio.wav")
    client = DeepgramClient()  # reads DEEPGRAM_API_KEY from the environment
    transcriber = ResilientTranscriber(client, audio_path)

    # Simulate one network failure 8 seconds in. Set SIMULATE_DROP=0 to
    # stream without it.
    if os.getenv("SIMULATE_DROP", "1") != "0":
        threading.Thread(target=force_network_drop, args=(transcriber, 8.0), daemon=True).start()

    try:
        transcriber.run()
    except (RuntimeError, ApiError) as err:
        # Permanent failures (bad credentials, non-retryable close codes,
        # retries exhausted) end with a message and a non-zero exit so
        # supervisors and scripts can tell success from failure.
        print(f"\nStream failed permanently: {err}")
        return 1

    print(f"\nTranscribed {len(transcriber.transcripts)} segments across {transcriber.reconnects + 1} connection(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

    # For async applications, the same patterns apply with AsyncDeepgramClient:
    #     async with client.listen.v1.connect(model="nova-3", ...) as connection:
    #         await connection.send_media(chunk)
    # using an asyncio.Queue as the buffer and asyncio.sleep for backoff.
