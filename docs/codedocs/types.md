---
title: "Types"
description: "Important exported Python types, enums, and protocols used across the Deepgram Python SDK."
---

This project does not export TypeScript interfaces because it is a Python SDK, but it does export a number of Python model types, enums, and protocols that matter when you build typed application code.

## Root Configuration Types

### `DeepgramClientEnvironment`

Source: `src/deepgram/environment.py`

```python
class DeepgramClientEnvironment:
    PRODUCTION: DeepgramClientEnvironment
    AGENT: DeepgramClientEnvironment

    def __init__(self, *, base: str, agent: str, production: str)
```

Use this when you need to point the SDK at a different Deepgram environment.

### `RequestOptions`

Source: `src/deepgram/core/request_options.py`

```python
class RequestOptions(TypedDict total=False):
    timeout_in_seconds: int
    max_retries: int
    additional_headers: dict[str, Any]
    additional_query_parameters: dict[str, Any]
    additional_body_parameters: dict[str, Any]
    chunk_size: int
```

Use this as the final keyword argument on service methods when one call needs different headers, timeout, retries, or response chunk sizing.

## Event Types

### `EventType`

Source: `src/deepgram/core/events.py`

```python
class EventType(str, Enum):
    OPEN = "open"
    MESSAGE = "message"
    ERROR = "error"
    CLOSE = "close"
```

This enum is shared by Listen, Speak, and Agent socket clients. The emitted order comes from the socket clients' `start_listening()` implementations.

## Transport Protocols

### `SyncTransport` and `AsyncTransport`

Source: `src/deepgram/transport_interface.py`

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

These are the contracts your custom transport must satisfy if you pass `transport_factory` to the root client.

## High-Value Exported Models

The root package dynamically exports a very large generated model surface through `src/deepgram/__init__.py`. The most important ones for application code are usually the request and settings models rather than every response schema.

### Agent settings models

```python
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V1,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
)
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
```

Use these when building realtime voice-agent settings payloads.

### Realtime message models

```python
from deepgram.listen.v2.types import ListenV2CloseStream, ListenV2Connected, ListenV2TurnInfo
from deepgram.speak.v1.types import SpeakV1Text, SpeakV1Flush, SpeakV1Close
```

Use these for websocket send and receive flows.

### Text-analysis and transcription request models

```python
from deepgram.requests.read_v1request import ReadV1RequestParams
from deepgram.listen.v1.media.types.media_transcribe_response import MediaTranscribeResponse
```

Use these when you want clearer local typing around request and response payloads.

## Practical Guidance

- Reach for the root client classes and `RequestOptions` first; they are the types that shape every call site.
- Use agent and websocket models when the method signature expects a model instance, not a plain dictionary.
- Treat the many generated response models as discoverable types that refine downstream code once you know which endpoint your application truly depends on.
