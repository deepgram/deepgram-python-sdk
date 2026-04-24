---
name: deepgram-python-audio-intelligence
description: Use when writing or reviewing Python code in this repo that calls Deepgram audio analytics overlays on `/v1/listen` - summarize, topics, intents, sentiment, diarize, redact, detect_language, entity detection. Same endpoint as plain STT but with analytics params. Covers both REST (`client.listen.v1.media.transcribe_url`/`transcribe_file`) and the WSS-supported subset (`client.listen.v1.connect`). Use `deepgram-python-speech-to-text` for plain transcription, `deepgram-python-text-intelligence` for analytics on already-transcribed text. Triggers include "diarize", "summarize audio", "sentiment from audio", "redact PII", "topic detection audio", "audio intelligence", "detect language audio".
---

# Using Deepgram Audio Intelligence (Python SDK)

Analytics overlays applied to `/v1/listen` transcription: summarize, topics, intents, sentiment, language detection, diarization, redaction, entities. Same endpoint / same client methods as STT — enable features via params.

## When to use this product

- You have **audio** (file, URL, or live stream) and want analytics alongside the transcript.
- REST is the primary path — most analytics are REST-only.

**Use a different skill when:**
- You want a pure transcript with no analytics → `deepgram-python-speech-to-text`.
- Your input is already transcribed text → `deepgram-python-text-intelligence` (`/v1/read`).
- You need conversational turn-taking → `deepgram-python-conversational-stt`.
- You need a full interactive agent → `deepgram-python-voice-agent`.

## Feature availability: REST vs WSS

| Feature | REST | WSS |
|---|---|---|
| `diarize` | yes | yes |
| `redact` | yes | yes |
| `punctuate`, `smart_format` | yes | yes |
| Entity detection | yes | yes |
| `summarize` | yes | **no** |
| `topics` | yes | **no** |
| `intents` | yes | **no** |
| `sentiment` | yes | **no** |
| `detect_language` | yes | **no** |
| `custom_topic` / `custom_intent` | yes | **no** |

For the WSS-only subset, same code path as `deepgram-python-speech-to-text`.

## Authentication

```python
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient()
```

Header: `Authorization: Token <api_key>`.

## Quick start — REST with full analytics

```python
response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    model="nova-3",
    smart_format=True,
    punctuate=True,
    diarize=True,              # speaker separation
    summarize="v2",            # "v2" for the current model; True also accepted on /v1/listen
    topics=True,
    intents=True,
    sentiment=True,
    detect_language=True,
    redact=["pci", "pii"],     # or Sequence[str]
    language="en-US",
)

r = response.results
print("transcript:", r.channels[0].alternatives[0].transcript)
print("summary:",    r.summary)
print("topics:",     r.topics)
print("intents:",    r.intents)
print("sentiments:", r.sentiments)
print("detected_language:", r.channels[0].detected_language)

# Speaker diarization
for word in r.channels[0].alternatives[0].words or []:
    speaker = getattr(word, "speaker", None)
    if speaker is not None:
        print(f"Speaker {speaker}: {word.word}")
```

## Quick start — REST file

```python
with open("call.wav", "rb") as f:
    audio = f.read()

response = client.listen.v1.media.transcribe_file(
    request=audio,
    model="nova-3",
    diarize=True,
    redact=["pii"],
    summarize="v2",
    topics=True,
)
```

## Quick start — WSS subset (diarize / redact / entities only)

```python
import threading
from deepgram.core.events import EventType

with client.listen.v1.connect(model="nova-3", diarize=True, redact=["pii"]) as conn:
    conn.on(EventType.MESSAGE, lambda m: print(m))
    threading.Thread(target=conn.start_listening, daemon=True).start()
    for chunk in audio_chunks:
        conn.send_media(chunk)
    conn.send_finalize()
```

## Key parameters

`summarize`, `topics`, `intents`, `sentiment`, `detect_language`, `diarize`, `redact`, `custom_topic`, `custom_topic_mode`, `custom_intent`, `custom_intent_mode`, `detect_entities`, plus all the standard STT params (`model`, `language`, `encoding`, `sample_rate`, ...).

`redact` accepts a string OR sequence (e.g. `"pci"` or `["pci", "pii", "numbers", "phi"]`). The SDK supports both via `Union[str, Sequence[str]]` — see the permanent patches in `.fernignore` for `listen_v1redact.py`.

## API reference (layered)

1. **In-repo reference**: `reference.md` — "Listen V1 Media" (REST params include all analytics flags), "Listen V1 Connect" (WSS-supported subset).
2. **OpenAPI (REST)**: https://developers.deepgram.com/openapi.yaml
3. **AsyncAPI (WSS)**: https://developers.deepgram.com/asyncapi.yaml
4. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
5. **Product docs**:
   - https://developers.deepgram.com/docs/stt-intelligence-feature-overview
   - https://developers.deepgram.com/docs/summarization
   - https://developers.deepgram.com/docs/topic-detection
   - https://developers.deepgram.com/docs/intent-recognition
   - https://developers.deepgram.com/docs/sentiment-analysis
   - https://developers.deepgram.com/docs/language-detection
   - https://developers.deepgram.com/docs/redaction
   - https://developers.deepgram.com/docs/diarization

## Gotchas

1. **`summarize` on `/v1/listen` accepts a boolean OR the string `"v2"`.** Use `"v2"` to pin the current summarization model; `True` also works (maps to the default model). `/v1/read` is the reverse — it accepts boolean only. If you need summarization on already-transcribed text, see `deepgram-python-text-intelligence`.
2. **Sentiment / topics / intents / summarize / detect_language are REST-only.** Don't pass them on WSS — they'll be ignored or rejected.
3. **English-only** for sentiment / topics / intents / summarize.
4. **Not all models support all overlays.** Flux / Base models have restrictions. Stick to `nova-3` unless you have a reason.
5. **Redaction values** are `pci`, `pii`, `phi`, `numbers`, etc. — not arbitrary strings.
6. **`custom_topic` / `custom_intent` need a mode** (`"extended"` or `"strict"`).
7. **Diarization is noisy on short / low-quality audio.** Expect speaker churn on <30s clips.

## Example files in this repo

- `examples/15-transcription-advanced-options.py` — smart_format, punctuate, diarize
- `tests/wire/test_listen_v1_media.py` — wire test covering intelligence params

## Related skills

- `deepgram-python-speech-to-text` — same endpoint, plain transcription
- `deepgram-python-text-intelligence` — same analytics, text input
- `deepgram-python-conversational-stt` — Flux for turn-taking
- `deepgram-python-voice-agent` — interactive assistants

## Central product skills

For cross-language Deepgram product knowledge — the consolidated API reference, documentation finder, focused runnable recipes, third-party integration examples, and MCP setup — install the central skills:

```bash
npx skills add deepgram/skills
```

This SDK ships language-idiomatic code skills; `deepgram/skills` ships cross-language product knowledge (see `api`, `docs`, `recipes`, `examples`, `starters`, `setup-mcp`).
