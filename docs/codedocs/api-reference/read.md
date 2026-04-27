---
title: "Read"
description: "Reference for text analysis methods in the Deepgram Python SDK."
---

The Read domain is the text intelligence surface. It is smaller than Listen or Speak, but it is the main place to request summaries, topics, intents, and sentiment over plain text.

## Imports

```python
from deepgram import DeepgramClient
```

Source files:

- `src/deepgram/read/client.py`
- `src/deepgram/read/v1/client.py`
- `src/deepgram/read/v1/text/client.py`

## `TextClient.analyze`

Import path: `client.read.v1.text`

```python
analyze(
    *,
    request: ReadV1RequestParams,
    callback: str | None = None,
    callback_method: TextAnalyzeRequestCallbackMethod | None = None,
    sentiment: bool | None = None,
    summarize: TextAnalyzeRequestSummarize | None = None,
    tag: str | Sequence[str] | None = None,
    topics: bool | None = None,
    custom_topic: str | Sequence[str] | None = None,
    custom_topic_mode: TextAnalyzeRequestCustomTopicMode | None = None,
    intents: bool | None = None,
    custom_intent: str | Sequence[str] | None = None,
    custom_intent_mode: TextAnalyzeRequestCustomIntentMode | None = None,
    language: str | None = None,
    request_options: RequestOptions | None = None,
) -> ReadV1Response
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | `ReadV1RequestParams` | — | Text payload, commonly `{"text": "..."}` or a URL-backed request. |
| `callback` | `str \| None` | `None` | Optional callback URL. |
| `callback_method` | enum \| `None` | `None` | HTTP method for the callback. |
| `sentiment` | `bool \| None` | `None` | Return sentiment analysis. |
| `summarize` | enum \| `None` | `None` | Return summary output. |
| `topics` | `bool \| None` | `None` | Return topic detection. |
| `custom_topic`, `custom_topic_mode` | string or sequence + enum | `None` | Constrain or extend topic matching. |
| `intents` | `bool \| None` | `None` | Return detected intents. |
| `custom_intent`, `custom_intent_mode` | string or sequence + enum | `None` | Constrain or extend intent matching. |
| `language` | `str \| None` | `None` | Primary language hint. |
| `tag` | `str \| Sequence[str] \| None` | `None` | Usage tag metadata. |
| `request_options` | `RequestOptions \| None` | `None` | Per-request headers, timeout, and retry settings. |

## Example

```python
response = client.read.v1.text.analyze(
    request={"text": "The customer wants a refund and sounds frustrated."},
    language="en",
    sentiment=True,
    intents=True,
    summarize=True,
)

print(response.results.summary.text)
```

## Return Type

`ReadV1Response` contains a `results` object with optional sentiment, summary, topic, and intent sections. The shape is model-based rather than plain dictionaries, so you access fields via attributes such as `response.results.summary.text`.
