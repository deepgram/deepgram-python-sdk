---
title: "Text-To-Speech Workflows"
description: "Generate audio with REST or stream it with WebSockets, including pronunciation control with TextBuilder."
---

This guide covers the two TTS workflows the SDK supports: one-shot REST generation and realtime streaming synthesis.

<Steps>
<Step>

### Choose REST or streaming

Use REST when you want a finite audio artifact and can consume bytes as they stream in. Use the websocket when you want to send multiple text messages over one connection or coordinate generation interactively.

</Step>
<Step>

### Build the text payload

Use plain text for simple prompts, or use `TextBuilder` when pronunciation and pauses matter.

```python
from deepgram.helpers import TextBuilder

text = (
    TextBuilder()
    .text("Take ")
    .pronunciation("adalimumab", "ˌædəˈljuːməb")
    .text(" once weekly.")
    .pause(500)
    .text(" Contact your clinician if symptoms worsen.")
    .build()
)
```

</Step>
<Step>

### Generate audio over REST

```python
from deepgram import DeepgramClient

client = DeepgramClient()

chunks = client.speak.v1.audio.generate(
    text=text,
    model="aura-2-asteria-en",
    request_options={"chunk_size": 8192},
)

with open("output.mp3", "wb") as handle:
    for chunk in chunks:
        handle.write(chunk)
```

</Step>
<Step>

### Stream audio over WebSocket

```python
from deepgram.core.events import EventType
from deepgram.speak.v1.types import SpeakV1Text

with client.speak.v1.connect(model="aura-2-asteria-en" encoding="linear16", sample_rate=24000) as connection:
    connection.on(EventType.MESSAGE, lambda message: print(type(message).__name__))
    connection.send_text(SpeakV1Text(text=text))
    connection.send_flush()
    connection.send_close()
    connection.start_listening()
```

</Step>
</Steps>

## Complete Example

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.helpers import TextBuilder
from deepgram.speak.v1.types import SpeakV1Text

client = DeepgramClient()

script = (
    TextBuilder()
    .text("Welcome back.")
    .pause(700)
    .text("Your dosage reminder is ready.")
    .build()
)

with client.speak.v1.connect(model="aura-2-asteria-en" encoding="linear16", sample_rate=24000) as connection:
    audio = []

    def on_message(message):
        if isinstance(message, bytes):
            audio.append(message)

    connection.on(EventType.MESSAGE, on_message)
    connection.send_text(SpeakV1Text(text=script))
    connection.send_flush()
    connection.send_close()
    connection.start_listening()

with open("reminder.raw", "wb") as handle:
    for chunk in audio:
        handle.write(chunk)
```

## When To Prefer Each Path

- Prefer REST when the application wants a file-like result and no bidirectional session logic.
- Prefer streaming when you want multiple prompts on one connection or need low-latency playback.
- Prefer `TextBuilder` whenever pronunciation correctness matters more than keeping the text as a single literal string.
