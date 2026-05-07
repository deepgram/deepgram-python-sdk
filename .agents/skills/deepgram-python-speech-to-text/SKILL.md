---
name: deepgram-python-speech-to-text
description: Use when writing or reviewing Python code in this repo that calls Deepgram Speech-to-Text v1 (`/v1/listen`) for prerecorded or live audio transcription. Covers `client.listen.v1.media.transcribe_url` / `transcribe_file` (REST) and `client.listen.v1.connect` (WebSocket). Use this skill for basic ASR; use `deepgram-python-audio-intelligence` for summarize/sentiment/topics/diarize overlays, `deepgram-python-conversational-stt` for turn-taking v2/Flux, and `deepgram-python-voice-agent` for full-duplex assistants. Triggers include "transcribe", "live transcription", "speech to text", "STT", "listen endpoint", "nova-3", "listen.v1".
---

# Using Deepgram Speech-to-Text (Python SDK)

Basic transcription (ASR) for prerecorded audio (REST) or live audio (WebSocket) via `/v1/listen`.

**Use a different skill when:**
- Summaries, sentiment, topics, intents, diarization, or redaction on audio → `deepgram-python-audio-intelligence` (same endpoint, different params).
- Turn-taking / end-of-turn events → `deepgram-python-conversational-stt` (v2 / Flux).
- Full-duplex interactive assistant (STT + LLM + TTS + function calls) → `deepgram-python-voice-agent`.

## Authentication

```python
import os
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()  # reads DEEPGRAM_API_KEY from env
# or: DeepgramClient(api_key=os.environ["DEEPGRAM_API_KEY"])
```

Header sent on every request: `Authorization: Token <api_key>` (NOT `Bearer`).

## Quick start — REST (prerecorded URL)

```python
response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    model="nova-3",
    smart_format=True,
    punctuate=True,
)
transcript = response.results.channels[0].alternatives[0].transcript
```

## Quick start — REST (prerecorded file)

```python
with open("audio.wav", "rb") as f:
    audio_bytes = f.read()

response = client.listen.v1.media.transcribe_file(
    request=audio_bytes,
    model="nova-3",
)
```

`request=` accepts raw `bytes` or an iterator of `bytes` (stream large files chunk-by-chunk). Do NOT pass a file handle.

## Quick start — WebSocket (live streaming with interim results)

```python
import threading
from deepgram.core.events import EventType
from deepgram.listen.v1.types import (
    ListenV1Results, ListenV1Metadata,
    ListenV1SpeechStarted, ListenV1UtteranceEnd,
)

with client.listen.v1.connect(
    model="nova-3",
    interim_results=True,
    utterance_end_ms=1000,
    vad_events=True,
    smart_format=True,
) as conn:
    state = {"last_interim_len": 0}

    def on_message(m):
        if isinstance(m, ListenV1Results) and m.channel and m.channel.alternatives:
            transcript = m.channel.alternatives[0].transcript
            if not transcript:
                return
            if m.is_final:
                pad = " " * max(0, state["last_interim_len"] - len(transcript))
                end = "\n" if m.speech_final else ""
                print(f"\r{transcript}{pad}", end=end, flush=True)
                state["last_interim_len"] = 0
            else:
                print(f"\r{transcript}", end="", flush=True)
                state["last_interim_len"] = len(transcript)
        elif isinstance(m, ListenV1UtteranceEnd):
            print()
        elif isinstance(m, ListenV1SpeechStarted):
            pass

    conn.on(EventType.OPEN,    lambda _: print("connected"))
    conn.on(EventType.MESSAGE, on_message)
    conn.on(EventType.CLOSE,   lambda _: print("\nclosed"))
    conn.on(EventType.ERROR,   lambda e: print(f"\nerr: {e}"))

    # Start receive loop in background so we can send concurrently
    threading.Thread(target=conn.start_listening, daemon=True).start()

    for chunk in audio_chunks:         # raw PCM bytes at declared encoding/sample_rate
        conn.send_media(chunk)

    conn.send_finalize()               # flush final partial before closing
```

### Interim vs. final flag semantics

| `is_final` | `speech_final` | Meaning |
|---|---|---|
| `False` | -- | Interim hypothesis; will be revised |
| `True` | `False` | Confirmed segment; speaker still talking |
| `True` | `True` | Confirmed segment; utterance ended (silence) |

`from_finalize=True` means the final was triggered by `send_finalize()` (vs natural endpointing). Call `send_finalize()` to flush, then `send_close_stream()` to terminate. Types: `deepgram.listen.v1.types`.

**WebSocket error recovery:** If connection fails with 401, verify auth scheme (Gotcha #1). If transcript is empty, verify `encoding`/`sample_rate` match the audio (Gotcha #2). On unexpected close, check `EventType.ERROR` payload and reconnect with exponential backoff.

## Async equivalents

```python
from deepgram import AsyncDeepgramClient
client = AsyncDeepgramClient()

response = await client.listen.v1.media.transcribe_url(url=..., model="nova-3")

async with client.listen.v1.connect(model="nova-3") as conn:
    # same .on(...) handlers, then:
    await conn.start_listening()
```

## Async / deferred result patterns

| Pattern | Returns | When to use |
|---|---|---|
| `client.listen.v1.media.transcribe_url(...)` | full transcription synchronously | files up to ~10 min |
| `await AsyncDeepgramClient().listen.v1.media.transcribe_url(...)` | full transcription, non-blocking | asyncio apps (FastAPI, aiohttp) |
| `transcribe_url(..., callback="https://...")` | `{request_id}` immediately; result POSTs to webhook | very long files; no polling endpoint exists |
| `client.listen.v1.connect(...)` (WebSocket) | streaming events as audio is sent | live audio (mic, telephony) |

For the callback pattern, pass `callback="https://your.app/webhook"` and optionally `callback_method="POST"`. The response contains only `request_id` -- the full transcription JSON is POSTed to your webhook. See `examples/12-transcription-prerecorded-callback.py`.

## Key parameters

`model`, `language`, `encoding`, `sample_rate`, `channels`, `multichannel`, `punctuate`, `smart_format`, `diarize`, `endpointing`, `interim_results`, `utterance_end_ms`, `vad_events`, `keywords`, `search`, `redact`, `numerals`, `paragraphs`, `utterances`.

## API reference (layered)

1. **In-repo Fern-generated reference**: `reference.md` — sections "Listen V1 Media" (REST) and "Listen V1 Connect" (WSS).
2. **Canonical OpenAPI (REST)**: https://developers.deepgram.com/openapi.yaml
3. **Canonical AsyncAPI (WSS)**: https://developers.deepgram.com/asyncapi.yaml
4. **Context7** — natural-language queries over the full Deepgram docs corpus. Library ID: `/llmstxt/developers_deepgram_llms_txt`.
5. **Product docs**:
   - https://developers.deepgram.com/reference/speech-to-text/listen-pre-recorded
   - https://developers.deepgram.com/reference/speech-to-text/listen-streaming

## Gotchas

1. **Use the right auth scheme for the credential type.** API keys use `Authorization: Token <api_key>`. Temporary / access tokens (from `client.auth.v1.tokens.grant()` or an equivalent server) use `Authorization: Bearer <access_token>` — the custom `DeepgramClient` installs a Bearer override when you pass `access_token=...` (see `src/deepgram/client.py`). Sending `Bearer <api_key>` with a long-lived API key is what fails.
2. **Encoding must match the audio.** Declaring `encoding="linear16"` but sending Opus → garbage output or 400.
3. **Close streams cleanly.** Call `send_finalize()` before exiting the WSS context — otherwise the last partial is dropped.
4. **Keepalive on long WSS sessions.** If idle > ~10s, the server closes. Send `KeepAlive` messages or audio chunks.
5. **Intelligence features are REST-only.** `summarize`, `topics`, `intents`, `sentiment`, `detect_language` do NOT work over WSS — see `deepgram-python-audio-intelligence`.
6. **`transcribe_file(request=...)` takes bytes or an iterator**, not a file handle.
7. **`nova-3` is the current flagship STT model.** Check `client.manage.v1.models.list()` for the live set.
8. **Sync `connection.start_listening()` blocks.** Run it in a thread (sync) or as a task (async) so you can send audio concurrently.

## Example files in this repo

- `examples/10-transcription-prerecorded-url.py`
- `examples/11-transcription-prerecorded-file.py`
- `examples/12-transcription-prerecorded-callback.py`
- `examples/13-transcription-live-websocket.py`
- `tests/wire/test_listen_v1_media.py` — wire-level fixtures
- `tests/manual/listen/v1/connect/main.py` — live WSS connection test

For cross-language Deepgram product knowledge, install the central skills: `npx skills add deepgram/skills`.
