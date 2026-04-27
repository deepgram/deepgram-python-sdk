---
title: "Helpers"
description: "Reference for helper utilities such as TextBuilder and custom transport protocols."
---

This SDK ships a small but important helper surface: text assembly for TTS and transport protocols for custom WebSocket integrations.

## Imports

```python
from deepgram.helpers import TextBuilder
from deepgram.transport import install_transport, restore_transport
from deepgram.transport_interface import SyncTransport, AsyncTransport
```

## `TextBuilder`

Source: `src/deepgram/helpers/text_builder.py`

```python
class TextBuilder:
    def text(self, content: str) -> TextBuilder
    def pronunciation(self, word: str, ipa: str) -> TextBuilder
    def pause(self, duration_ms: int) -> TextBuilder
    def from_ssml(self, ssml_text: str) -> TextBuilder
    def build(self) -> str
```

Related free functions:

```python
add_pronunciation(text: str, word: str, ipa: str) -> str
ssml_to_deepgram(ssml_text: str) -> str
```

### Example

```python
from deepgram.helpers import TextBuilder

text = (
    TextBuilder()
    .text("Take ")
    .pronunciation("methotrexate", "mɛθəˈtrɛkseɪt")
    .text(" weekly.")
    .build()
)
```

## Transport Utilities

Source files:

- `src/deepgram/transport.py`
- `src/deepgram/transport_interface.py`

### Signatures

```python
install_transport(*, sync_factory: callable | None = None, async_factory: callable | None = None) -> None
restore_transport() -> None
```

### Protocols

```python
class SyncTransport(Protocol):
    def send(self, data: Any) -> None
    def recv(self) -> Any
    def __iter__(self) -> Iterator
    def close(self) -> None

class AsyncTransport(Protocol):
    async def send(self, data: Any) -> None
    async def recv(self) -> Any
    def __aiter__(self) -> Any
    async def close(self) -> None
```

### Example

```python
from deepgram import DeepgramClient


class MyTransport:
    def __init__(self, url: str, headers: dict[str, str]):
        self.url = url
        self.headers = headers

    def send(self, data):
        ...

    def recv(self):
        ...

    def __iter__(self):
        yield from ()

    def close(self):
        pass


client = DeepgramClient(api_key="dg_key", transport_factory=MyTransport)
```

## When To Use These Helpers

- Use `TextBuilder` when pronunciation correctness matters.
- Use transport helpers when you need to integrate the SDK with a non-default websocket layer or a controlled test environment.
