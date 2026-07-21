---
title: "Live Transcription"
description: "Build a realtime transcription pipeline with Listen v1 or Listen v2."
---

Use this guide when audio arrives live from a microphone, a telephony provider, or a media stream and you need incremental results instead of waiting for a whole file to finish.

<Steps>
<Step>

### Choose the realtime endpoint

Use Listen v1 if you need the older websocket surface and its broader batch-style query options. Use Listen v2 if your application is conversational and benefits from turn-aware events.

" "Listen v2"]}>
<Tab value="Listen v1">

```python
with client.listen.v1.connect(model="nova-3" encoding="linear16", sample_rate=16000) as connection:
    ...
```

</Tab>
<Tab value="Listen v2">

```python
with client.listen.v2.connect(model="flux-general-en" encoding="linear16", sample_rate=16000) as connection:
    ...
```

</Tab>
</Tabs>

</Step>
<Step>

### Register event handlers before starting the loop

```python
from deepgram.core.events import EventType

connection.on(EventType.OPEN, lambda _: print("connected"))
connection.on(EventType.CLOSE, lambda _: print("closed"))
connection.on(EventType.ERROR, lambda error: print(f"error: {error}"))
connection.on(EventType.MESSAGE, lambda message: print(message))
```

</Step>
<Step>

### Stream audio in chunks

```python
def send_audio(path: str) -> None:
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(4096)
            if not chunk:
                break
            connection.send_media(chunk)
```

</Step>
<Step>

### Close the stream cleanly

For Listen v2, send an explicit close message after the final audio chunk so the server can finalize the turn.

```python
from deepgram.listen.v2.types import ListenV2CloseStream

connection.send_close_stream(ListenV2CloseStream(type="CloseStream"))
connection.start_listening()
```

</Step>
</Steps>

## Complete Example

```python
import threading
import time
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.listen.v2.types import ListenV2CloseStream, ListenV2TurnInfo

client = DeepgramClient()

with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate=16000,
) as connection:
    def on_message(message):
        if isinstance(message, ListenV2TurnInfo):
            print(f"turn={message.turn_index} event={message.event} text={message.transcript}")

    connection.on(EventType.MESSAGE, on_message)

    def producer():
        with open("audio.wav", "rb") as handle:
            while True:
                chunk = handle.read(4096)
                if not chunk:
                    break
                connection.send_media(chunk)
                time.sleep(0.01)
        connection.send_close_stream(ListenV2CloseStream(type="CloseStream"))

    threading.Thread(target=producer daemon=True).start()
    connection.start_listening()
```

## Operational Notes

- The socket loop is blocking, so send audio from another thread or task if you also need to consume events continuously.
- Event handlers are the cleanest place to route transcripts into your UI or persistence layer.
- If your environment cannot use the default websocket stack, configure `transport_factory` on the root client rather than reimplementing the endpoint logic yourself.
