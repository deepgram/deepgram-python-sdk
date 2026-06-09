"""
Example: 60db Text-to-Speech (one-shot REST).

POSTs to https://api.60db.ai/tts-synthesize and writes the returned
base64 audio to disk. Set DEEPGRAM_API_KEY (required by the parent SDK
constructor) and SIXTY_DB_API_KEY for 60db itself.
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

print("Calling 60db /tts-synthesize...")
resp = client.sixty_db.tts.synthesize(
    text="Hello from the 60db Python integration in the Deepgram SDK.",
    voice_id="fbb75ed2-975a-40c7-9e06-38e30524a9a1",  # default voice from docs
    speed=1.0,
    stability=50,
    similarity=75,
    output_format="mp3",
)

if not resp.audio_base64:
    raise SystemExit(f"60db returned no audio: success={resp.success} message={resp.message}")

audio_bytes = base64.b64decode(resp.audio_base64)
output_path = f"sixty-db-output.{resp.output_format or 'mp3'}"
with open(output_path, "wb") as f:
    f.write(audio_bytes)

print(f"Saved {len(audio_bytes)} bytes to {output_path}")
print(f"  duration={resp.duration_seconds}s sample_rate={resp.sample_rate} encoding={resp.encoding}")
