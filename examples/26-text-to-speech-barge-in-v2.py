"""
Example: Barge-in and mid-stream reconfiguration on the Speak V2 (Flux) WebSocket

Two capabilities that need bidirectional timing, so this example is async --
`start_listening()` blocks in sync mode, which leaves no way to send a message
while audio is still streaming back.

1. Barge-in (`send_interrupt`). Stops the current turn. Pass a `playback_offset`
   with how much audio the user has actually *heard* and the server replies with
   a `SpeechInterrupted` telling you which words were spoken and which were not
   -- exactly what you need to keep a conversation transcript honest. Two rules
   worth knowing: the offset is cumulative from the start of the session (not the
   start of the turn), and each `Interrupt` must advance past the previous one.
   Omit the offset and you still stop the turn, but `text_spoken` /
   `text_remaining` come back empty because the server cannot know where you were.

2. Mid-stream reconfiguration (`send_configure`). Changes the speech rate without
   reconnecting. The server acknowledges with `ConfigureSuccess` (echoing what it
   applied) or a typed `ConfigureFailure` -- the SDK does not range-check `speed`,
   so an out-of-range value comes back as `SPEED_OUT_OF_RANGE` rather than raising
   locally.
"""

import asyncio

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient
from deepgram.speak.v2.types import (
    SpeakV2Configure,
    SpeakV2Interrupt,
    SpeakV2InterruptPlaybackOffset,
    SpeakV2Speak,
)

# 24 kHz linear16 mono: 2 bytes per sample, so 48 bytes per millisecond.
BYTES_PER_MS = 24000 * 2 // 1000

TEXT = (
    "This sentence is deliberately long so that audio is still streaming when the "
    "interrupt is sent, which is what makes the barge-in observable."
)


async def main() -> None:
    client = AsyncDeepgramClient()

    async with client.speak.v2.connect(
        model="flux-alexis-en",
        encoding="linear16",
        sample_rate="24000",
        speed=1.0,
    ) as connection:
        audio_bytes = 0
        interrupted = asyncio.Event()

        async def consume() -> None:
            nonlocal audio_bytes
            async for message in connection:
                if isinstance(message, bytes):
                    audio_bytes += len(message)
                    continue

                msg_type = getattr(message, "type", None)

                if msg_type == "ConfigureSuccess":
                    print(f"Configure applied: speed={getattr(message.applied, 'speed', None)}")
                elif msg_type == "ConfigureFailure":
                    # e.g. SPEED_OUT_OF_RANGE / SPEED_INCREMENT_INVALID
                    print(f"Configure rejected [{message.code}]: {message.description}")
                elif msg_type == "SpeechInterrupted":
                    print(f"Interrupted after {message.audio_played_ms} ms of audio")
                    print(f"  spoken   : {message.text_spoken!r}")
                    print(f"  remaining: {message.text_remaining!r}")
                    interrupted.set()
                else:
                    print(f"Received {msg_type} event")

        consumer = asyncio.create_task(consume())

        # Mid-stream speed change, acknowledged by the server.
        await connection.send_configure(SpeakV2Configure(speed=1.05))

        await connection.send_speak(SpeakV2Speak(text=TEXT))

        # Let some audio actually stream back, then barge in at the point the
        # listener had reached. Offset is cumulative from session start.
        await asyncio.sleep(2)
        played_ms = audio_bytes // BYTES_PER_MS
        print(f"Barging in at {played_ms} ms ({audio_bytes} bytes received)")
        await connection.send_interrupt(
            SpeakV2Interrupt(
                playback_offset=SpeakV2InterruptPlaybackOffset(type="time_ms", value=played_ms)
            )
        )

        try:
            await asyncio.wait_for(interrupted.wait(), timeout=10)
        except asyncio.TimeoutError:
            print("No SpeechInterrupted received before the timeout")

        await connection.send_close()
        consumer.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
