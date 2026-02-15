# v5 to v6 Migration Guide

This guide helps you migrate from Deepgram Python SDK v5 (versions 5.0.0 to 5.3.2) to v6.0.0. The v6 release replaces the hand-written `deepgram.extensions.types.sockets` module with Fern-generated types, simplifies WebSocket method names, and introduces dedicated control message methods.

## Table of Contents

- [Installation](#installation)
- [Configuration Changes](#configuration-changes)
- [Authentication Changes](#authentication-changes)
- [API Method Changes](#api-method-changes)
  - [Listen V1 (REST)](#listen-v1-rest)
  - [Listen V1 (WebSocket)](#listen-v1-websocket)
  - [Listen V2 (WebSocket)](#listen-v2-websocket)
  - [Speak V1 (REST)](#speak-v1-rest)
  - [Speak V1 (WebSocket)](#speak-v1-websocket)
  - [Agent V1 (WebSocket)](#agent-v1-websocket)
  - [Read V1](#read-v1)
  - [Manage V1](#manage-v1)
  - [Self-Hosted V1](#self-hosted-v1)
- [Type Changes](#type-changes)
  - [Import Path Changes](#import-path-changes)
  - [Agent Configuration Types](#agent-configuration-types)
  - [WebSocket Event Types](#websocket-event-types)
- [Breaking Changes Summary](#breaking-changes-summary)

## Installation

To upgrade from v5 to v6.0.0:

```bash
pip install --upgrade deepgram-sdk
```

## Configuration Changes

Client initialization is unchanged between v5 and v6.

```python
from deepgram import DeepgramClient

# All of these work the same in both versions
client = DeepgramClient()                                # from environment
client = DeepgramClient(api_key="YOUR_API_KEY")          # explicit API key
client = DeepgramClient(access_token="YOUR_TOKEN")       # access token
```

## Authentication Changes

No changes. Authentication works the same as v5:

1. Explicit `access_token` parameter (highest priority)
2. Explicit `api_key` parameter
3. `DEEPGRAM_TOKEN` environment variable
4. `DEEPGRAM_API_KEY` environment variable (lowest priority)

## API Method Changes

### Listen V1 (REST)

No changes. REST transcription methods work the same as v5.

```python
# Unchanged in v6
response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    model="nova-3",
)

with open("audio.wav", "rb") as audio_file:
    response = client.listen.v1.media.transcribe_file(
        request=audio_file.read(),
        model="nova-3",
    )
```

### Listen V1 (WebSocket)

The context manager pattern and event system are unchanged. The changes are in how you send media and control messages.

**v5**

```python
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import (
    ListenV1SocketClientResponse,
    ListenV1MediaMessage,
    ListenV1ControlMessage,
)

with client.listen.v1.connect(model="nova-3") as connection:
    def on_message(message: ListenV1SocketClientResponse) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

    connection.start_listening()

    # Sending media
    connection.send_media(ListenV1MediaMessage(audio_bytes))

    # Sending control messages
    connection.send_control(ListenV1ControlMessage(type="Finalize"))
    connection.send_control(ListenV1ControlMessage(type="CloseStream"))
    connection.send_control(ListenV1ControlMessage(type="KeepAlive"))
```

**v6**

```python
from deepgram.core.events import EventType
from deepgram.listen.v1.types import ListenV1Results, ListenV1Metadata

with client.listen.v1.connect(model="nova-3") as connection:
    def on_message(message) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

    connection.start_listening()

    # Sending media — accepts bytes directly
    connection.send_media(audio_bytes)

    # Sending control messages — dedicated methods, no arguments needed
    connection.send_finalize()
    connection.send_close_stream()
    connection.send_keep_alive()
```

### Listen V2 (WebSocket)

**v5**

```python
from deepgram.extensions.types.sockets import (
    ListenV2SocketClientResponse,
    ListenV2MediaMessage,
    ListenV2ControlMessage,
)

with client.listen.v2.connect(
    model="flux-general-en", encoding="linear16", sample_rate="16000"
) as connection:
    def on_message(message: ListenV2SocketClientResponse) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.MESSAGE, on_message)
    connection.start_listening()

    connection.send_media(ListenV2MediaMessage(audio_bytes))
    connection.send_control(ListenV2ControlMessage(type="CloseStream"))
```

**v6**

```python
from deepgram.listen.v2.types import ListenV2Connected, ListenV2TurnInfo

with client.listen.v2.connect(
    model="flux-general-en", encoding="linear16", sample_rate=16000
) as connection:
    def on_message(message) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.MESSAGE, on_message)
    connection.start_listening()

    connection.send_media(audio_bytes)      # bytes directly
    connection.send_close_stream()          # no argument needed
```

### Speak V1 (REST)

No changes. REST text-to-speech methods work the same as v5.

```python
# Unchanged in v6
response = client.speak.v1.audio.generate(
    text="Hello, world!",
    model="aura-2-asteria-en",
)
```

### Speak V1 (WebSocket)

**v5**

```python
from deepgram.extensions.types.sockets import (
    SpeakV1SocketClientResponse,
    SpeakV1TextMessage,
    SpeakV1ControlMessage,
)

with client.speak.v1.connect(
    model="aura-2-asteria-en", encoding="linear16", sample_rate=24000
) as connection:
    def on_message(message: SpeakV1SocketClientResponse) -> None:
        if isinstance(message, bytes):
            print("Received audio data")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    connection.on(EventType.MESSAGE, on_message)
    connection.start_listening()

    connection.send_text(SpeakV1TextMessage(text="Hello, world!"))
    connection.send_control(SpeakV1ControlMessage(type="Flush"))
    connection.send_control(SpeakV1ControlMessage(type="Clear"))
    connection.send_control(SpeakV1ControlMessage(type="Close"))
```

**v6**

```python
from deepgram.speak.v1.types import SpeakV1Text

with client.speak.v1.connect(
    model="aura-2-asteria-en", encoding="linear16", sample_rate=24000
) as connection:
    def on_message(message) -> None:
        if isinstance(message, bytes):
            print("Received audio data")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    connection.on(EventType.MESSAGE, on_message)
    connection.start_listening()

    connection.send_text(SpeakV1Text(text="Hello, world!"))
    connection.send_flush()     # no argument needed
    connection.send_clear()     # no argument needed
    connection.send_close()     # no argument needed
```

### Agent V1 (WebSocket)

The agent WebSocket has the most changes — both in configuration types and method names.

**v5**

```python
from deepgram.extensions.types.sockets import (
    AgentV1SettingsMessage,
    AgentV1Agent,
    AgentV1AudioConfig,
    AgentV1AudioInput,
    AgentV1Listen,
    AgentV1ListenProvider,
    AgentV1Think,
    AgentV1OpenAiThinkProvider,
    AgentV1SpeakProviderConfig,
    AgentV1DeepgramSpeakProvider,
    AgentV1SocketClientResponse,
    AgentV1ControlMessage,
)

with client.agent.v1.connect() as agent:
    settings = AgentV1SettingsMessage(
        audio=AgentV1AudioConfig(
            input=AgentV1AudioInput(encoding="linear16", sample_rate=44100)
        ),
        agent=AgentV1Agent(
            listen=AgentV1Listen(
                provider=AgentV1ListenProvider(
                    type="deepgram", model="nova-3"
                )
            ),
            think=AgentV1Think(
                provider=AgentV1OpenAiThinkProvider(
                    type="open_ai", model="gpt-4o-mini", temperature=0.7
                ),
                prompt="You are a helpful AI assistant.",
            ),
            speak=AgentV1SpeakProviderConfig(
                provider=AgentV1DeepgramSpeakProvider(
                    type="deepgram", model="aura-2-asteria-en"
                )
            ),
        ),
    )

    agent.send_settings(settings)
    agent.send_media(AgentV1MediaMessage(audio_bytes))
    agent.send_control(AgentV1ControlMessage(type="KeepAlive"))
    agent.start_listening()
```

**v6**

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

with client.agent.v1.connect() as agent:
    settings = AgentV1Settings(
        audio=AgentV1SettingsAudio(
            input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)
        ),
        agent=AgentV1SettingsAgent(
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider_V1(
                    type="deepgram", model="nova-3"
                )
            ),
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_OpenAi(
                    type="open_ai", model="gpt-4o-mini", temperature=0.7
                ),
                prompt="You are a helpful AI assistant.",
            ),
            speak=SpeakSettingsV1(
                provider=SpeakSettingsV1Provider_Deepgram(
                    type="deepgram", model="aura-2-asteria-en"
                )
            ),
        ),
    )

    agent.send_settings(settings)
    agent.send_media(audio_bytes)       # bytes directly
    agent.send_keep_alive()             # no argument needed
    agent.start_listening()
```

### Read V1

No changes. Text analysis methods work the same as v5.

```python
# Unchanged in v6
response = client.read.v1.text.analyze(
    request={"text": "Hello, world!"},
    language="en",
    sentiment=True,
    summarize=True,
    topics=True,
    intents=True,
)
```

### Manage V1

No changes. All management API methods work the same as v5.

```python
# Unchanged in v6
projects = client.manage.v1.projects.list()
keys = client.manage.v1.projects.keys.list(project_id="...")
usage = client.manage.v1.projects.usage.get(project_id="...")
models = client.manage.v1.models.list()
```

### Self-Hosted V1

No changes. Self-hosted API methods work the same as v5.

```python
# Unchanged in v6
credentials = client.self_hosted.v1.distribution_credentials.list(project_id="...")
```

## Type Changes

### Import Path Changes

The `deepgram.extensions.types.sockets` module has been removed. All types are now imported from their Fern-generated locations.

| v5 import path | v6 import path |
|---|---|
| `deepgram.extensions.types.sockets` | `deepgram.agent.v1.types` |
| `deepgram.extensions.types.sockets` | `deepgram.listen.v1.types` |
| `deepgram.extensions.types.sockets` | `deepgram.listen.v2.types` |
| `deepgram.extensions.types.sockets` | `deepgram.speak.v1.types` |
| `deepgram.extensions.types.sockets` | `deepgram.types.think_settings_v1` |
| `deepgram.extensions.types.sockets` | `deepgram.types.think_settings_v1provider` |
| `deepgram.extensions.types.sockets` | `deepgram.types.speak_settings_v1` |
| `deepgram.extensions.types.sockets` | `deepgram.types.speak_settings_v1provider` |

### Agent Configuration Types

Agent configuration types have been renamed. Think and speak provider types moved from agent-specific types to shared top-level types.

| v5 | v6 | Import from |
|----|----|----|
| `AgentV1SettingsMessage` | `AgentV1Settings` | `deepgram.agent.v1.types` |
| `AgentV1Agent` | `AgentV1SettingsAgent` | `deepgram.agent.v1.types` |
| `AgentV1AudioConfig` | `AgentV1SettingsAudio` | `deepgram.agent.v1.types` |
| `AgentV1AudioInput` | `AgentV1SettingsAudioInput` | `deepgram.agent.v1.types` |
| `AgentV1Listen` | `AgentV1SettingsAgentListen` | `deepgram.agent.v1.types` |
| `AgentV1ListenProvider` | `AgentV1SettingsAgentListenProvider_V1` | `deepgram.agent.v1.types` |
| `AgentV1Think` | `ThinkSettingsV1` | `deepgram.types.think_settings_v1` |
| `AgentV1OpenAiThinkProvider` | `ThinkSettingsV1Provider_OpenAi` | `deepgram.types.think_settings_v1provider` |
| `AgentV1AnthropicThinkProvider` | `ThinkSettingsV1Provider_Anthropic` | `deepgram.types.think_settings_v1provider` |
| `AgentV1AwsBedrockThinkProvider` | `ThinkSettingsV1Provider_AwsBedrock` | `deepgram.types.think_settings_v1provider` |
| `AgentV1GoogleThinkProvider` | `ThinkSettingsV1Provider_Google` | `deepgram.types.think_settings_v1provider` |
| `AgentV1GroqThinkProvider` | `ThinkSettingsV1Provider_Groq` | `deepgram.types.think_settings_v1provider` |
| `AgentV1SpeakProviderConfig` | `SpeakSettingsV1` | `deepgram.types.speak_settings_v1` |
| `AgentV1DeepgramSpeakProvider` | `SpeakSettingsV1Provider_Deepgram` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1ElevenLabsSpeakProvider` | `SpeakSettingsV1Provider_ElevenLabs` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1CartesiaSpeakProvider` | `SpeakSettingsV1Provider_Cartesia` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1OpenAiSpeakProvider` | `SpeakSettingsV1Provider_OpenAi` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1AwsPollySpeakProvider` | `SpeakSettingsV1Provider_AwsPolly` | `deepgram.types.speak_settings_v1provider` |

### WebSocket Event Types

Received event types have been renamed. The `Event`/`Message` suffix is dropped, and types are imported from their service-specific `types` module instead of `deepgram.extensions.types.sockets`.

#### Agent events

| v5 | v6 |
|---|---|
| `AgentV1WelcomeMessage` | `AgentV1Welcome` |
| `AgentV1SettingsAppliedEvent` | `AgentV1SettingsApplied` |
| `AgentV1ConversationTextEvent` | `AgentV1ConversationText` |
| `AgentV1UserStartedSpeakingEvent` | `AgentV1UserStartedSpeaking` |
| `AgentV1AgentThinkingEvent` | `AgentV1AgentThinking` |
| `AgentV1FunctionCallRequestEvent` | `AgentV1FunctionCallRequest` |
| `AgentV1AgentStartedSpeakingEvent` | `AgentV1AgentStartedSpeaking` |
| `AgentV1AgentAudioDoneEvent` | `AgentV1AgentAudioDone` |
| `AgentV1PromptUpdatedEvent` | `AgentV1PromptUpdated` |
| `AgentV1SpeakUpdatedEvent` | `AgentV1SpeakUpdated` |
| `AgentV1InjectionRefusedEvent` | `AgentV1InjectionRefused` |
| `AgentV1ErrorEvent` | `AgentV1Error` |
| `AgentV1WarningEvent` | `AgentV1Warning` |

#### Listen V1 events

| v5 | v6 |
|---|---|
| `ListenV1ResultsEvent` | `ListenV1Results` |
| `ListenV1MetadataEvent` | `ListenV1Metadata` |
| `ListenV1UtteranceEndEvent` | `ListenV1UtteranceEnd` |
| `ListenV1SpeechStartedEvent` | `ListenV1SpeechStarted` |

#### Listen V2 events

| v5 | v6 |
|---|---|
| `ListenV2ConnectedEvent` | `ListenV2Connected` |
| `ListenV2TurnInfoEvent` | `ListenV2TurnInfo` |
| `ListenV2FatalErrorEvent` | `ListenV2FatalError` |

#### Speak events

| v5 | v6 |
|---|---|
| `SpeakV1MetadataEvent` | `SpeakV1Metadata` |
| `SpeakV1WarningEvent` | `SpeakV1Warning` |
| `SpeakV1ControlEvent` | `SpeakV1Flushed` / `SpeakV1Cleared` (split into separate types) |
| `SpeakV1AudioChunkEvent` | Removed (use `bytes` directly) |

### WebSocket Method Changes

The generic `send_control()` method has been removed from all WebSocket clients. Each control action now has a dedicated method that requires no arguments.

| Client | v5 | v6 |
|--------|----|----|
| Listen V1 | `send_media(ListenV1MediaMessage(...))` | `send_media(bytes)` |
| Listen V1 | `send_control(ListenV1ControlMessage(type="Finalize"))` | `send_finalize()` |
| Listen V1 | `send_control(ListenV1ControlMessage(type="CloseStream"))` | `send_close_stream()` |
| Listen V1 | `send_control(ListenV1ControlMessage(type="KeepAlive"))` | `send_keep_alive()` |
| Listen V2 | `send_media(ListenV2MediaMessage(...))` | `send_media(bytes)` |
| Listen V2 | `send_control(ListenV2ControlMessage(type="CloseStream"))` | `send_close_stream()` |
| Speak V1 | `send_text(SpeakV1TextMessage(text=...))` | `send_text(SpeakV1Text(text=...))` |
| Speak V1 | `send_control(SpeakV1ControlMessage(type="Flush"))` | `send_flush()` |
| Speak V1 | `send_control(SpeakV1ControlMessage(type="Clear"))` | `send_clear()` |
| Speak V1 | `send_control(SpeakV1ControlMessage(type="Close"))` | `send_close()` |
| Agent V1 | `send_media(AgentV1MediaMessage(...))` | `send_media(bytes)` |
| Agent V1 | `send_control(AgentV1ControlMessage(type="KeepAlive"))` | `send_keep_alive()` |

## Breaking Changes Summary

### Major Changes

1. **WebSocket types**: The `deepgram.extensions.types.sockets` module has been removed. All types are now Fern-generated and imported from service-specific `types` modules.
2. **Agent configuration**: Agent settings types have been renamed and reorganized. Think and speak provider types are now shared top-level types.
3. **WebSocket control methods**: The generic `send_control()` method has been replaced with dedicated methods (`send_flush()`, `send_close()`, `send_keep_alive()`, etc.).
4. **WebSocket media methods**: `send_media()` now accepts raw `bytes` instead of wrapper types.
5. **Event type naming**: The `Event` and `Message` suffixes have been dropped from all WebSocket event type names.

### Removed Features

- `deepgram.extensions.types.sockets` module (all types moved to Fern-generated locations)
- `send_control()` method on all WebSocket clients (replaced with dedicated methods)
- Wrapper types for media messages (`ListenV1MediaMessage`, `AgentV1MediaMessage`, etc.)
- `SpeakV1ControlEvent` (split into `SpeakV1Flushed` and `SpeakV1Cleared`)
- `SpeakV1AudioChunkEvent` (use `bytes` directly)
- Backward compatibility aliases (`SpeakSocketClientResponse`, `ListenSocketClientResponse`, `AgentSocketClientResponse`)

### New Features in v6

- **Dedicated control methods**: Type-safe methods like `send_flush()`, `send_close()`, `send_keep_alive()` with no arguments needed
- **Simplified media sending**: Pass raw `bytes` directly to `send_media()`
- **Listen V2 provider support**: Agent settings now support `AgentV1SettingsAgentListenProvider_V2` for Listen V2-based agents
- **Additional think providers**: New `ThinkSettingsV1Provider_Groq` and other provider variants

### Migration Checklist

- [ ] Upgrade to latest version: `pip install --upgrade deepgram-sdk`
- [ ] Replace all imports from `deepgram.extensions.types.sockets` with new paths
- [ ] Rename agent configuration types (`AgentV1Agent` -> `AgentV1SettingsAgent`, etc.)
- [ ] Update think/speak provider imports to `deepgram.types.*`
- [ ] Replace `send_control()` calls with dedicated methods (`send_flush()`, `send_close()`, etc.)
- [ ] Remove wrapper types from `send_media()` calls — pass `bytes` directly
- [ ] Update `SpeakV1TextMessage` to `SpeakV1Text`
- [ ] Remove `Event`/`Message` suffixes from event type names used in `isinstance()` checks
- [ ] Remove unused imports (`SpeakV1ControlMessage`, `ListenV1MediaMessage`, etc.)
- [ ] Test all functionality with new API structure
