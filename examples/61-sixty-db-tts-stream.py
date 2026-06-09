"""
Example: 60db Text-to-Speech (NDJSON streaming).

POSTs to https://api.60db.ai/tts-stream. The server emits one JSON object
per line. The client yields parsed SixtyDbStreamChunk objects; we
concatenate audio from "chunk" messages and stop on "complete" / "error".
"""

import base64
import os

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    sixty_db_api_key=os.getenv("SIXTY_DB_API_KEY"),
)

print("Calling 60db /tts-stream...")
audio = bytearray()
chunk_count = 0

for chunk in client.sixty_db.tts.stream(
    text="This is a longer message streamed back from 60db, chunk by chunk.",
    voice_id="fbb75ed2-975a-40c7-9e06-38e30524a9a1",
    speed=1.0,
):
    if chunk.type == "chunk" and chunk.result and chunk.result.audio_content:
        audio.extend(base64.b64decode(chunk.result.audio_content))
        chunk_count += 1
    elif chunk.type == "complete":
        print("Server reported completion.")
        break
    elif chunk.type == "error":
        raise SystemExit(f"60db stream error: {chunk.message}")

output_path = "sixty-db-stream-output.mp3"
with open(output_path, "wb") as f:
    f.write(audio)

print(f"Saved {len(audio)} bytes from {chunk_count} chunks to {output_path}")
