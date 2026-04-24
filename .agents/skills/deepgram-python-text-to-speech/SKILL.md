---
name: deepgram-python-text-to-speech
description: Use when writing or reviewing Python code in this repo that calls Deepgram Text-to-Speech v1 (`/v1/speak`) for audio synthesis. Covers one-shot REST (`client.speak.v1.audio.generate`) and streaming WebSocket (`client.speak.v1.connect`). Also covers the in-repo `deepgram.helpers.TextBuilder` for incremental text assembly before synthesis. Use `deepgram-python-voice-agent` when you need full-duplex STT + LLM + TTS with barge-in. Triggers include "TTS", "speak", "synthesize voice", "aura", "text to speech", "speak.v1", "TextBuilder".
---

# Using Deepgram Text-to-Speech (Python SDK)

Convert text to audio: one-shot REST download or low-latency streaming synthesis via `/v1/speak`.

## When to use this product

- **REST (`speak.v1.audio.generate`)** — one-shot synthesis, returns audio bytes. Use for rendered files, pre-generated prompts, anything where you have the full text upfront.
- **WebSocket (`speak.v1.connect`)** — incremental text input, streaming audio output. Use for low-latency playback while an LLM is still producing tokens.

**Use a different skill when:**
- You need the agent to also listen and converse (full-duplex) → `deepgram-python-voice-agent`.

## Authentication

```python
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient()  # reads DEEPGRAM_API_KEY
```

Header: `Authorization: Token <api_key>` (NOT `Bearer`).

## Quick start — REST (one-shot)

```python
audio_iter = client.speak.v1.audio.generate(
    text="Hello, this is a text to speech example.",
    model="aura-2-asteria-en",
    encoding="linear16",
    sample_rate=24000,
)

with open("output.raw", "wb") as f:
    for chunk in audio_iter:
        f.write(chunk)
```

Returns an iterator of `bytes` (streaming audio response). The response body is `audio/*`, NOT JSON. Useful response headers: `dg-model-name`, `dg-char-count`, `dg-request-id`.

## Quick start — WebSocket (streaming)

```python
from deepgram.core.events import EventType
from deepgram.speak.v1.types import SpeakV1Text

with client.speak.v1.connect(
    model="aura-2-asteria-en",
    encoding="linear16",
    sample_rate=24000,
) as conn:
    def on_message(m):
        if isinstance(m, bytes):
            # audio chunk — write to file or audio output
            ...
        else:
            print(f"event: {getattr(m, 'type', 'Unknown')}")

    conn.on(EventType.OPEN,    lambda _: print("open"))
    conn.on(EventType.MESSAGE, on_message)
    conn.on(EventType.CLOSE,   lambda _: print("close"))
    conn.on(EventType.ERROR,   lambda e: print(f"err: {e}"))

    conn.send_text(SpeakV1Text(text="Hello, this is streaming TTS."))
    conn.send_flush()
    conn.send_close()
    conn.start_listening()   # blocks until server closes
```

In **sync** mode, `start_listening()` blocks — send all text + flush + close BEFORE calling it, OR run it in a thread. In **async** mode, run `start_listening()` as a task and send concurrently.

## TextBuilder helper (incremental text assembly)

`deepgram.helpers.TextBuilder` is a hand-maintained helper (NOT Fern-generated) that assembles text incrementally — useful when streaming LLM tokens into TTS.

```python
from deepgram.helpers import TextBuilder

final_text = (
    TextBuilder()
    .text("Hello,")
    .text(" this is built incrementally.")
    .pronunciation("Deepgram", "ˈdiːpɡɹæm")
    .pause(200)
    .build()
)
```

The fluent API is `.text(...)` (append raw text), `.pronunciation(word, ipa)` (pin pronunciation), `.pause(duration_ms)` (insert a pause), and `.build()` (return the final SSML-ish string). There is no `.add(...)` method.

See `examples/22-text-builder-demo.py`, `examples/23-text-builder-helper.py`, `examples/24-text-builder-streaming.py`.

## Async equivalents

```python
from deepgram import AsyncDeepgramClient
client = AsyncDeepgramClient()

# REST
audio_iter = await client.speak.v1.audio.generate(text=..., model="aura-2-asteria-en")
async for chunk in audio_iter:
    ...

# WSS
async with client.speak.v1.connect(model="aura-2-asteria-en", ...) as conn:
    listen_task = asyncio.create_task(conn.start_listening())
    await conn.send_text(SpeakV1Text(text="..."))
    await conn.send_flush()
    await conn.send_close()
    await listen_task
```

## Key parameters

REST & WSS: `model` (e.g. `aura-2-asteria-en`), `encoding` (`linear16`, `mulaw`, `alaw`, `opus`, `flac`, `mp3`, `aac`), `sample_rate`, `bit_rate`, `container`, `callback` (REST async), `tag`, `mip_opt_out`.

WSS client messages: `SpeakV1Text`, `Flush`, `Clear`, `Close`.

## API reference (layered)

1. **In-repo reference**: `reference.md` — sections "Speak V1 Audio" (REST) and "Speak V1 Connect" (WSS).
2. **OpenAPI (REST)**: https://developers.deepgram.com/openapi.yaml
3. **AsyncAPI (WSS)**: https://developers.deepgram.com/asyncapi.yaml
4. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
5. **Product docs**:
   - https://developers.deepgram.com/reference/text-to-speech/speak-request
   - https://developers.deepgram.com/reference/text-to-speech/speak-streaming
   - https://developers.deepgram.com/docs/tts-models

## Gotchas

1. **`Token` auth, not `Bearer`.**
2. **REST response is audio bytes, not JSON.** Iterate the response; don't `.json()` it.
3. **Flush before close (WSS).** `send_close()` without `send_flush()` may drop trailing audio.
4. **Sync `start_listening()` blocks.** Queue all messages first, or use async.
5. **`SpeakV1Text` is required** for WSS text input — don't send raw strings.
6. **`encoding`/`sample_rate`/`container` must match your playback path.** Mismatches cause silent failure or distortion.
7. **`TextBuilder` helpers are hand-maintained** (listed in `.fernignore` as permanently frozen). Don't move them under `src/deepgram/` auto-generated paths.

## Example files in this repo

- `examples/20-text-to-speech-single.py` — REST one-shot
- `examples/21-text-to-speech-streaming.py` — WSS streaming
- `examples/22-text-builder-demo.py` — TextBuilder (no API key)
- `examples/23-text-builder-helper.py` — TextBuilder + REST
- `examples/24-text-builder-streaming.py` — TextBuilder + WSS
- `tests/wire/test_speak_v1_audio.py` — REST wire test
- `tests/manual/speak/v1/connect/main.py` — live WSS test

## Central product skills

For cross-language Deepgram product knowledge — the consolidated API reference, documentation finder, focused runnable recipes, third-party integration examples, and MCP setup — install the central skills:

```bash
npx skills add deepgram/skills
```

This SDK ships language-idiomatic code skills; `deepgram/skills` ships cross-language product knowledge (see `api`, `docs`, `recipes`, `examples`, `starters`, `setup-mcp`).
