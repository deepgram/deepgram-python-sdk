---
name: using-text-intelligence
description: Use when writing or reviewing Python code in this repo that calls Deepgram Text Intelligence / Read (`/v1/read`) for sentiment, summarization, topic detection, and intent recognition on text input. Covers `client.read.v1.text.analyze(...)` with body `text` or `url`. Use `using-audio-intelligence` when the source is audio instead of text. Triggers include "read API", "text intelligence", "analyze text", "sentiment", "summarize text", "topics", "intents", "read.v1".
---

# Using Deepgram Text Intelligence (Python SDK)

Analyze plain text (or a hosted text URL) for sentiment, summarization, topics, and intents via `/v1/read`.

## When to use this product

- You have **text already** (a transcript, document, chat log, email) and want analytics.
- You want a quick one-shot analysis — REST only, no streaming.

**Use a different skill when:**
- The source is audio and you want analytics overlays → `using-audio-intelligence` (same analytics, applied at transcription time).

## Authentication

```python
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient()
```

Header: `Authorization: Token <api_key>`.

## Quick start

```python
response = client.read.v1.text.analyze(
    request={"text": "Hello, world! This is a sample text for analysis."},
    language="en",
    sentiment=True,
    summarize=True,   # boolean per docstring; "v2" also works (see gotchas)
    topics=True,
    intents=True,
)

if response.results.sentiments:
    print("sentiment avg:", response.results.sentiments.average)
if response.results.summary:
    print("summary:", response.results.summary.text)
if response.results.topics:
    print("topics:", response.results.topics.segments)
if response.results.intents:
    print("intents:", response.results.intents.segments)
```

Pass `request={"text": "..."}` for raw text OR `request={"url": "https://..."}` for a hosted plain-text document.

## Async equivalent

```python
from deepgram import AsyncDeepgramClient
client = AsyncDeepgramClient()
response = await client.read.v1.text.analyze(request={"text": "..."}, language="en", sentiment=True)
```

## Key parameters

| Param | Type | Notes |
|---|---|---|
| `request` | `{"text": str}` or `{"url": str}` | One of these is required |
| `language` | `str` | Required for most analytics. English only today. |
| `sentiment` | `bool` | Per-segment + average sentiment |
| `summarize` | `bool` or `"v2"` | Type alias `TextAnalyzeRequestSummarize = typing.Union[typing.Literal["v2"], typing.Any]` accepts either. The `analyze` docstring says "For Read API, accepts boolean only" — but the wire test uses `summarize="v2"` on `/read` and the server accepts it. Both work; `bool` matches the documented Read shape. |
| `topics` | `bool` | Topic detection per segment |
| `intents` | `bool` | Intent recognition per segment |
| `custom_topic` / `custom_topic_mode` | `list[str]` / `str` | User-defined topics |
| `custom_intent` / `custom_intent_mode` | `list[str]` / `str` | User-defined intents |
| `callback`, `callback_method`, `tag` | | Async callback + metadata |

## Response shape (abridged)

```
response.results.summary.text
response.results.sentiments.segments[]
response.results.sentiments.average
response.results.topics.segments[]
response.results.intents.segments[]
response.metadata
```

See `reference.md` → "Read V1 Text" for full shape. Request body model: `ReadV1RequestParams`.

## API reference (layered)

1. **In-repo reference**: `reference.md` — "Read V1 Text".
2. **OpenAPI (REST)**: https://developers.deepgram.com/openapi.yaml
3. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
4. **Product docs**:
   - https://developers.deepgram.com/reference/text-intelligence/analyze-text
   - https://developers.deepgram.com/docs/text-intelligence
   - https://developers.deepgram.com/docs/text-sentiment-analysis

## Gotchas

1. **`Token` auth, not `Bearer`.**
2. **English-only** for sentiment / summarize / topics / intents today.
3. **`summarize` accepts either a boolean or the string `"v2"`** — both work on `/v1/read`. The SDK type `Union[Literal["v2"], Any]` permits either. The `analyze` method docstring says "For Read API, accepts boolean only" (distinguishing it from Listen's versioned string), but the generated wire test uses `summarize="v2"` and the server accepts it. Use `True`/`False` to match the documented Read shape, or `"v2"` to align with Listen — don't assume one form is the "only" one.
4. **`language` is required** for the gated analytics features above.
5. **Body is JSON `request=`**, not query parameters. Don't confuse with `/v1/listen` which takes audio as the body.
6. **Custom topics/intents need a mode** (`custom_topic_mode="extended"`, `"strict"`) or they are ignored.

## Example files in this repo

- `examples/40-text-intelligence.py`
- `tests/wire/test_read_v1_text.py`

## Central product skills

For cross-language Deepgram product knowledge — the consolidated API reference, documentation finder, focused runnable recipes, third-party integration examples, and MCP setup — install the central skills:

```bash
npx skills add deepgram/skills
```

This SDK ships language-idiomatic code skills; `deepgram/skills` ships cross-language product knowledge (see `api`, `docs`, `recipes`, `examples`, `starters`, `setup-mcp`).
