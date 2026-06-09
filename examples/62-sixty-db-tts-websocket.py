"""
Example: 60db Text-to-Speech (WebSocket).

Opens wss://api.60db.ai/ws/tts, creates a context, sends some text,
flushes, and writes the concatenated PCM audio to disk.

LINEAR16 @ 16000 Hz is the default. PCM frames are mono 16-bit signed
little-endian and concatenate cleanly. OGG_OPUS chunks are NOT
concatenatable - each is a self-contained Ogg file.
"""

import asyncio
import base64
import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import AsyncDeepgramClient


async def main() -> None:
    client = AsyncDeepgramClient(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        sixty_db_api_key=os.getenv("SIXTY_DB_API_KEY"),
    )

    audio = bytearray()
    async with client.sixty_db.tts.websocket() as ws:
        # First server message is connection_established; create our context.
        first = await ws.recv()
        if first.connection_established:
            print(
                "Connected. credits={} workspace={}".format(
                    first.connection_established.credit_balance,
                    first.connection_established.workspace,
                )
            )

        ctx_id = await ws.create_context(
            voice_id="fbb75ed2-975a-40c7-9e06-38e30524a9a1",
            audio_encoding="LINEAR16",
            sample_rate_hertz=16000,
        )
        print(f"context_id={ctx_id}")

        await ws.send_text("Hello from the 60db WebSocket via the Deepgram SDK fork.")
        await ws.flush()

        async for event in ws:
            if event.context_created:
                continue
            if event.audio_chunk and event.audio_chunk.audio_content:
                audio.extend(base64.b64decode(event.audio_chunk.audio_content))
            elif event.flush_completed:
                print("Flush complete.")
                break
            elif event.error:
                raise SystemExit(f"60db WS error: {event.error.message}")

        await ws.close_context()

    output_path = "sixty-db-ws-output.pcm"
    with open(output_path, "wb") as f:
        f.write(audio)
    print(f"Saved {len(audio)} bytes of raw LINEAR16 PCM to {output_path}")


asyncio.run(main())
