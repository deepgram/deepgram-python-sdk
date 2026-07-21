---
title: "Speak"
description: "Reference for text-to-speech REST and WebSocket clients."
---

The Speak domain exposes both a REST API that yields audio bytes and a WebSocket API for interactive streaming TTS.

## Imports

```python
from deepgram import DeepgramClient
from deepgram.speak.v1.types import SpeakV1Text
```

Source files:

- `src/deepgram/speak/client.py`
- `src/deepgram/speak/v1/client.py`
- `src/deepgram/speak/v1/audio/client.py`
- `src/deepgram/speak/v1/socket_client.py`

## `AudioClient.generate`

Import path: `client.speak.v1.audio`

```python
generate(
    *,
    text: str,
    callback: str | None = None,
    callback_method: AudioGenerateRequestCallbackMethod | None = None,
    mip_opt_out: bool | None = None,
    tag: str | Sequence[str] | None = None,
    bit_rate: float | None = None,
    container: AudioGenerateRequestContainer | None = None,
    encoding: AudioGenerateRequestEncoding | None = None,
    model: AudioGenerateRequestModel | None = None,
    sample_rate: float | None = None,
    speed: float | None = None,
    request_options: RequestOptions | None = None,
) -> Iterator[bytes]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | — | Text to synthesize. |
| `callback` | `str \| None` | `None` | Optional callback URL. |
| `callback_method` | enum \| `None` | `None` | HTTP method for the callback. |
| `model` | enum \| `None` | `None` | Voice model, commonly an Aura model. |
| `encoding` | enum \| `None` | `None` | Output audio encoding. |
| `container` | enum \| `None` | `None` | Output file wrapper. |
| `sample_rate` | `float \| None` | `None` | Output sample rate. |
| `bit_rate` | `float \| None` | `None` | Output bitrate. |
| `speed` | `float \| None` | `None` | Speaking rate multiplier. |
| `tag` | `str \| Sequence[str] \| None` | `None` | Usage tag metadata. |
| `request_options` | `RequestOptions \| None` | `None` | Request timeout and `chunk_size` overrides. |

### Example

```python
audio_chunks = client.speak.v1.audio.generate(
    text="Hello from Deepgram.",
    model="aura-2-asteria-en",
)
```

## `V1Client.connect`

Import path: `client.speak.v1`

```python
connect(
    *,
    encoding: SpeakV1Encoding | None = None,
    mip_opt_out: SpeakV1MipOptOut | None = None,
    model: SpeakV1Model | None = None,
    sample_rate: SpeakV1SampleRate | None = None,
    speed: SpeakV1Speed | None = None,
    authorization: str | None = None,
    request_options: RequestOptions | None = None,
) -> Iterator[V1SocketClient]
```

## `V1SocketClient` Methods

Source: `src/deepgram/speak/v1/socket_client.py`

- `start_listening()`
- `send_text(message: SpeakV1Text) -> None`
- `send_flush(message: SpeakV1Flush | None = None) -> None`
- `send_clear(message: SpeakV1Clear | None = None) -> None`
- `send_close(message: SpeakV1Close | None = None) -> None`
- `recv() -> V1SocketClientResponse`

The response union includes binary audio plus metadata types such as `SpeakV1Metadata`, `SpeakV1Flushed`, `SpeakV1Cleared`, and `SpeakV1Warning`.

### Example

```python
with client.speak.v1.connect(model="aura-2-asteria-en" encoding="linear16", sample_rate=24000) as connection:
    connection.send_text(SpeakV1Text(text="Hello from the websocket API."))
    connection.send_flush()
    connection.send_close()
    connection.start_listening()
```

## Related Helper

If you need pronunciation and pause control, build the `text` value with `deepgram.helpers.TextBuilder`. See `/docs/api-reference/helpers` and `/docs/text-builder`.
