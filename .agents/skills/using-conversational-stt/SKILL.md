---
name: using-conversational-stt
description: Use when writing or reviewing Python code in this repo that calls Deepgram Conversational STT v2 / Flux (`/v2/listen`) for turn-aware streaming transcription. Covers `client.listen.v2.connect(...)`, Flux models, end-of-turn detection. Use `using-speech-to-text` for standard v1 ASR, `using-voice-agent` for full-duplex interactive assistants. Triggers include "flux", "v2 listen", "conversational STT", "turn detection", "end of turn", "EOT", "listen.v2", "flux-general-en", "flux-general-multi".
---

# Using Deepgram Conversational STT / Flux (Python SDK)

Turn-aware streaming STT at `/v2/listen` — optimized for conversational audio (end-of-turn detection, eager EOT, barge-in scenarios).

## When to use this product

- You're building a **conversational UI** and need explicit turn boundaries.
- You want **Flux models** (optimized for human-to-human or human-to-agent conversation).
- You want lower latency turn signals than v1 utterance_end.

**Use a different skill when:**
- You want general-purpose transcription (captions, batch, non-conversational) → `using-speech-to-text`.
- You want a full interactive agent (STT + LLM + TTS) → `using-voice-agent`.
- You want analytics (summarize/sentiment) → `using-audio-intelligence`.

## Authentication

```python
import os
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient(api_key=os.environ["DEEPGRAM_API_KEY"])
```

Header: `Authorization: Token <api_key>`. WSS only — no REST path on v2.

## Quick start

```python
import threading, time
from pathlib import Path
from deepgram.core.events import EventType
from deepgram.listen.v2.types import (
    ListenV2CloseStream,
    ListenV2Connected,
    ListenV2FatalError,
    ListenV2TurnInfo,
)

with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate="16000",
) as conn:

    def on_message(m):
        if isinstance(m, ListenV2TurnInfo):
            print(f"turn {m.turn_index} [{m.event}] {m.transcript}")
        elif isinstance(m, dict):                     # untyped fallback
            if m.get("type") == "TurnInfo":
                print(f"turn {m.get('turn_index')} [{m.get('event')}] {m.get('transcript')}")
        else:
            print(f"event: {getattr(m, 'type', type(m).__name__)}")

    conn.on(EventType.OPEN,    lambda _: print("open"))
    conn.on(EventType.MESSAGE, on_message)
    conn.on(EventType.CLOSE,   lambda _: print("close"))
    conn.on(EventType.ERROR,   lambda e: print(f"err: {type(e).__name__}: {e}"))

    def send_audio():
        for chunk in mic_chunks():                     # 80ms recommended
            conn.send_media(chunk)
            time.sleep(0.01)
        conn.send_close_stream(ListenV2CloseStream(type="CloseStream"))

    threading.Thread(target=send_audio, daemon=True).start()
    conn.start_listening()
```

## Key parameters

| Param | Notes |
|---|---|
| `model` | `flux-general-en` (English) or `flux-general-multi` (multilingual) — REQUIRED, must be a Flux model |
| `encoding` | `linear16`, `mulaw`, etc. Omit for containerized audio |
| `sample_rate` | String in the SDK signature, e.g. `"16000"` |
| `eager_eot_threshold` | Fire end-of-turn early at this confidence |
| `eot_threshold` | Primary end-of-turn confidence |
| `eot_timeout_ms` | Time-based fallback turn end |
| `keyterm` | Bias for domain keywords |
| `mip_opt_out`, `tag` | Metadata / privacy flags |
| `language_hint` | **ONLY for `flux-general-multi`** |
| `authorization`, `request_options` | Override auth or request options |

**No `language` parameter** on v2 — language is implied by model (`flux-general-en`) or hinted via `language_hint` on multi.

## Events (server → client)

- `ListenV2Connected` — connection established
- `ListenV2ConfigureSuccess` / `ListenV2ConfigureFailure` — mid-session config changes
- `ListenV2TurnInfo` — per-turn transcript + event (`Update`, `EndOfTurn`, `EagerEndOfTurn`, ...) + `turn_index`
- `ListenV2FatalError` — terminal error

Client messages: `ListenV2Media`, `ListenV2Configure`, `ListenV2CloseStream`.

## Async equivalent

```python
from deepgram import AsyncDeepgramClient
client = AsyncDeepgramClient()

async with client.listen.v2.connect(model="flux-general-en", ...) as conn:
    # same .on(...) handlers, then:
    await conn.start_listening()
```

## API reference (layered)

1. **In-repo reference**: `reference.md` — "Listen V2 Connect".
2. **AsyncAPI (WSS)**: https://developers.deepgram.com/asyncapi.yaml
3. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
4. **Product docs**:
   - https://developers.deepgram.com/reference/speech-to-text/listen-flux
   - https://developers.deepgram.com/docs/flux/quickstart
   - https://developers.deepgram.com/docs/flux/language-prompting

## Gotchas

1. **`/v2/listen`, not `/v1/listen`.** Different route, different client path (`listen.v2` vs `listen.v1`).
2. **Flux models only.** `nova-3`, `base`, etc. will be rejected. Use `flux-general-en` or `flux-general-multi`.
3. **No `language` parameter.** Language is set by model choice. Use `language_hint` on `flux-general-multi`.
4. **`sample_rate` is a STRING** in the SDK (e.g. `"16000"`).
5. **Send ~80ms audio chunks** for best turn-detection latency.
6. **Close with `send_close_stream(ListenV2CloseStream(type="CloseStream"))`** — not `send_finalize` (that's v1).
7. **Messages may arrive as typed objects OR raw dicts** — the SDK uses a tagged union with `construct_type` for unknowns. Handle both branches (see `socket_client.py` patch in `.fernignore`).
8. **`client.py` and `socket_client.py` are patched** (see `.fernignore` → `listen/v2/`). Don't edit auto-generated versions directly.
9. **Omit `encoding`/`sample_rate` for containerized audio** (WAV, OGG, etc.) — the server detects them from the container.

## Example files in this repo

- `examples/14-transcription-live-websocket-v2.py`
- `tests/manual/listen/v2/connect/main.py`

## Related skills

- `using-speech-to-text` — v1 general-purpose STT (REST + WSS)
- `using-voice-agent` — full interactive assistant
