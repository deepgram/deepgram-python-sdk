---
title: "Listen"
description: "Reference for batch and realtime speech-to-text clients in the Deepgram Python SDK."
---

The Listen domain combines REST transcription and realtime speech recognition. Root import path: `client.listen`.

## Imports

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import ListenV2CloseStream
```

## Module Hierarchy

```python
client.listen.v1.media
client.listen.v1.connect(...)
client.listen.v2.connect(...)
```

Source files:

- `src/deepgram/listen/client.py`
- `src/deepgram/listen/v1/client.py`
- `src/deepgram/listen/v1/media/client.py`
- `src/deepgram/listen/v1/socket_client.py`
- `src/deepgram/listen/v2/client.py`
- `src/deepgram/listen/v2/socket_client.py`

## `MediaClient`

Import path: `client.listen.v1.media`

### Signatures

```python
transcribe_url(
    *,
    url: str,
    callback: str | None = None,
    callback_method: MediaTranscribeRequestCallbackMethod | None = None,
    extra: str | Sequence[str] | None = None,
    sentiment: bool | None = None,
    summarize: MediaTranscribeRequestSummarize | None = None,
    tag: str | Sequence[str] | None = None,
    topics: bool | None = None,
    custom_topic: str | Sequence[str] | None = None,
    custom_topic_mode: MediaTranscribeRequestCustomTopicMode | None = None,
    intents: bool | None = None,
    custom_intent: str | Sequence[str] | None = None,
    custom_intent_mode: MediaTranscribeRequestCustomIntentMode | None = None,
    detect_entities: bool | None = None,
    detect_language: bool | None = None,
    diarize: bool | None = None,
    dictation: bool | None = None,
    encoding: MediaTranscribeRequestEncoding | None = None,
    filler_words: bool | None = None,
    keyterm: str | Sequence[str] | None = None,
    keywords: str | Sequence[str] | None = None,
    language: str | None = None,
    measurements: bool | None = None,
    model: MediaTranscribeRequestModel | None = None,
    multichannel: bool | None = None,
    numerals: bool | None = None,
    paragraphs: bool | None = None,
    profanity_filter: bool | None = None,
    punctuate: bool | None = None,
    redact: str | None = None,
    replace: str | Sequence[str] | None = None,
    search: str | Sequence[str] | None = None,
    smart_format: bool | None = None,
    utterances: bool | None = None,
    utt_split: float | None = None,
    version: MediaTranscribeRequestVersion | None = None,
    mip_opt_out: bool | None = None,
    request_options: RequestOptions | None = None,
) -> MediaTranscribeResponse

transcribe_file(
    *,
    request: bytes | Iterator[bytes] | AsyncIterator[bytes],
    callback: str | None = None,
    callback_method: MediaTranscribeRequestCallbackMethod | None = None,
    extra: str | Sequence[str] | None = None,
    sentiment: bool | None = None,
    summarize: MediaTranscribeRequestSummarize | None = None,
    tag: str | Sequence[str] | None = None,
    topics: bool | None = None,
    custom_topic: str | Sequence[str] | None = None,
    custom_topic_mode: MediaTranscribeRequestCustomTopicMode | None = None,
    intents: bool | None = None,
    custom_intent: str | Sequence[str] | None = None,
    custom_intent_mode: MediaTranscribeRequestCustomIntentMode | None = None,
    detect_entities: bool | None = None,
    detect_language: bool | None = None,
    diarize: bool | None = None,
    dictation: bool | None = None,
    encoding: MediaTranscribeRequestEncoding | None = None,
    filler_words: bool | None = None,
    keyterm: str | Sequence[str] | None = None,
    keywords: str | Sequence[str] | None = None,
    language: str | None = None,
    measurements: bool | None = None,
    model: MediaTranscribeRequestModel | None = None,
    multichannel: bool | None = None,
    numerals: bool | None = None,
    paragraphs: bool | None = None,
    profanity_filter: bool | None = None,
    punctuate: bool | None = None,
    redact: str | None = None,
    replace: str | Sequence[str] | None = None,
    search: str | Sequence[str] | None = None,
    smart_format: bool | None = None,
    utterances: bool | None = None,
    utt_split: float | None = None,
    version: MediaTranscribeRequestVersion | None = None,
    mip_opt_out: bool | None = None,
    request_options: RequestOptions | None = None,
) -> MediaTranscribeResponse
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | — | Hosted media URL for `transcribe_url(...)`. |
| `request` | `bytes \| Iterator[bytes] \| AsyncIterator[bytes]` | — | Raw file content or chunk iterator for `transcribe_file(...)`. |
| `model` | `MediaTranscribeRequestModel \| None` | `None` | Speech model such as `nova-3`. |
| `callback` | `str \| None` | `None` | Callback URL for asynchronous completion. |
| `callback_method` | enum \| `None` | `None` | HTTP method for the callback. |
| `language` | `str \| None` | `None` | BCP-47 language hint. |
| `encoding` | enum \| `None` | `None` | Audio encoding when Deepgram cannot infer it. |
| `detect_entities` | `bool \| None` | `None` | Entity extraction. |
| `detect_language` | `bool \| None` | `None` | Dominant-language detection. |
| `diarize` | `bool \| None` | `None` | Speaker diarization. |
| `dictation` | `bool \| None` | `None` | Dictation-specific formatting. |
| `keyterm`, `keywords`, `search`, `replace` | string or sequence | `None` | Prompting, search, and replacement controls. |
| `topics`, `intents`, `sentiment`, `summarize` | feature flags | `None` | Additional language-intelligence outputs. |
| `paragraphs`, `utterances`, `utt_split` | layout options | `None` | Segmentation controls for readability and utterance boundaries. |
| `smart_format`, `punctuate`, `numerals`, `measurements`, `profanity_filter`, `redact` | formatting controls | `None` | Output cleanup and normalization features. |
| `request_options` | `RequestOptions \| None` | `None` | Per-request headers, query params, retries, and timeout overrides. |

### Example

```python
response = client.listen.v1.media.transcribe_file(
    request=open("audio.wav", "rb").read(),
    model="nova-3",
    smart_format=True,
    diarize=True,
)
```

## `V1Client.connect`

Import path: `client.listen.v1`

```python
connect(
    *,
    model: ListenV1Model,
    callback: ListenV1Callback | None = None,
    callback_method: ListenV1CallbackMethod | None = None,
    channels: ListenV1Channels | None = None,
    detect_entities: ListenV1DetectEntities | None = None,
    diarize: ListenV1Diarize | None = None,
    dictation: ListenV1Dictation | None = None,
    encoding: ListenV1Encoding | None = None,
    endpointing: ListenV1Endpointing | None = None,
    extra: ListenV1Extra | None = None,
    interim_results: ListenV1InterimResults | None = None,
    keyterm: ListenV1Keyterm | None = None,
    keywords: ListenV1Keywords | None = None,
    language: ListenV1Language | None = None,
    mip_opt_out: ListenV1MipOptOut | None = None,
    multichannel: ListenV1Multichannel | None = None,
    numerals: ListenV1Numerals | None = None,
    profanity_filter: ListenV1ProfanityFilter | None = None,
    punctuate: ListenV1Punctuate | None = None,
    redact: ListenV1Redact | None = None,
    replace: ListenV1Replace | None = None,
    sample_rate: ListenV1SampleRate | None = None,
    search: ListenV1Search | None = None,
    smart_format: ListenV1SmartFormat | None = None,
    tag: ListenV1Tag | None = None,
    utterance_end_ms: ListenV1UtteranceEndMs | None = None,
    vad_events: ListenV1VadEvents | None = None,
    version: ListenV1Version | None = None,
    authorization: str | None = None,
    request_options: RequestOptions | None = None,
) -> Iterator[V1SocketClient]
```

## `V2Client.connect`

Import path: `client.listen.v2`

```python
connect(
    *,
    model: ListenV2Model,
    encoding: ListenV2Encoding | None = None,
    sample_rate: ListenV2SampleRate | None = None,
    eager_eot_threshold: ListenV2EagerEotThreshold | None = None,
    eot_threshold: ListenV2EotThreshold | None = None,
    eot_timeout_ms: ListenV2EotTimeoutMs | None = None,
    keyterm: ListenV2KeytermParams | None = None,
    mip_opt_out: ListenV2MipOptOut | None = None,
    tag: ListenV2Tag | None = None,
    authorization: str | None = None,
    request_options: RequestOptions | None = None,
) -> Iterator[V2SocketClient]
```

## Socket Client Methods

### `V1SocketClient`

- `start_listening()`
- `send_media(message: bytes) -> None`
- `send_finalize(message: ListenV1Finalize | None = None) -> None`
- `send_close_stream(message: ListenV1CloseStream | None = None) -> None`
- `send_keep_alive(message: ListenV1KeepAlive | None = None) -> None`
- `recv() -> V1SocketClientResponse`

### `V2SocketClient`

- `start_listening()`
- `send_media(message: bytes) -> None`
- `send_close_stream(message: ListenV2CloseStream | None = None) -> None`
- `send_configure(message: Any) -> None`
- `recv() -> V2SocketClientResponse`

### Streaming Example

```python
with client.listen.v2.connect(model="flux-general-en" encoding="linear16", sample_rate=16000) as connection:
    connection.on(EventType.MESSAGE, lambda message: print(message))
    connection.send_media(b"...pcm bytes...")
    connection.send_close_stream(ListenV2CloseStream(type="CloseStream"))
    connection.start_listening()
```
