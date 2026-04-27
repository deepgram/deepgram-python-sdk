# v6 to v7 Migration Guide

This guide helps you migrate from Deepgram Python SDK v6 (versions 6.0.0 to 6.1.1) to v7.0.0. The v7 release keeps the core client APIs unchanged, but it does include two breaking changes: Python 3.8/3.9 are no longer supported, and several public generated types were renamed or removed during SDK regeneration.

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
  - [Minimum Python Version](#minimum-python-version)
  - [Agent Think and Speak Types](#agent-think-and-speak-types)
  - [WebSocket Type Aliases](#websocket-type-aliases)
  - [Other Removed Generated Types](#other-removed-generated-types)
- [Breaking Changes Summary](#breaking-changes-summary)

## Installation

To upgrade from v6 to v7.0.0:

```bash
pip install --upgrade deepgram-sdk
```

If you are still running Python 3.8 or 3.9, upgrade your runtime to Python 3.10 or newer before installing v7.

## Configuration Changes

Client initialization is unchanged between v6 and v7.

```python
from deepgram import DeepgramClient

# All of these work the same in both versions
client = DeepgramClient()                                # from environment
client = DeepgramClient(api_key="YOUR_API_KEY")          # explicit API key
client = DeepgramClient(access_token="YOUR_TOKEN")       # access token
```

## Authentication Changes

No changes. Authentication works the same as v6:

1. Explicit `access_token` parameter (highest priority)
2. Explicit `api_key` parameter
3. `DEEPGRAM_TOKEN` environment variable
4. `DEEPGRAM_API_KEY` environment variable (lowest priority)

## API Method Changes

### Listen V1 (REST)

No changes. REST transcription methods work the same as v6.

### Listen V1 (WebSocket)

No breaking changes. Existing connection setup, event handling, `send_media()`, and control methods keep working as they did in v6.

### Listen V2 (WebSocket)

No breaking changes. Existing `client.listen.v2.connect(...)`, event handling, `send_media()`, and `send_close_stream()` calls continue to work.

v7 also adds optional `send_configure()` support and generated `ListenV2Configure*` types, but you do not need to change existing v6 code to upgrade.

### Speak V1 (REST)

No changes. REST text-to-speech methods work the same as v6.

### Speak V1 (WebSocket)

No breaking changes. Existing WebSocket connection setup, event handling, `send_text()`, `send_flush()`, `send_clear()`, and `send_close()` calls continue to work.

### Agent V1 (WebSocket)

No client methods were removed, and existing runtime behavior is unchanged for common agent workflows.

The breaking changes in v7 are in the generated public types used to build agent think/speak settings and updates. If you only used `DeepgramClient` and the documented examples, your runtime code is likely already compatible. If you imported generated voice-agent types directly, see [Agent Think and Speak Types](#agent-think-and-speak-types).

v7 also adds optional `send_update_think()` support plus new generated event types such as `AgentV1ThinkUpdated` and `AgentV1History`.

### Read V1

No changes. Text analysis methods work the same as v6.

### Manage V1

No breaking changes to existing management API methods.

v7 also adds generated support for reusable voice agent configurations and variables APIs under `client.voice_agent.*`.

### Self-Hosted V1

No changes. Self-hosted API methods work the same as v6.

## Type Changes

### Minimum Python Version

Python 3.8 and 3.9 are no longer supported in v7.

| v6 | v7 |
|---|---|
| Python 3.8+ | Python 3.10+ |

If you publish a library or application that depends on `deepgram-sdk`, update your package metadata, CI matrix, and runtime images accordingly.

### Agent Think and Speak Types

The biggest source-level change in v7 is a consolidation of voice-agent think/speak schemas. Several agent-specific generated types were removed and replaced by shared top-level schemas in `deepgram.types`.

This mostly affects code that imported types from `deepgram.agent.v1.types` or `deepgram.agent.v1.requests` directly.

| v6 | v7 | Import from |
|---|---|---|
| `AgentV1SettingsAgentSpeakEndpoint` | `SpeakSettingsV1` | `deepgram.types.speak_settings_v1` |
| `AgentV1SettingsAgentSpeakOneItem` | `SpeakSettingsV1` | `deepgram.types.speak_settings_v1` |
| `AgentV1SettingsAgentSpeakEndpointProvider_*` | `SpeakSettingsV1Provider_*` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1SettingsAgentSpeakOneItemProvider_*` | `SpeakSettingsV1Provider_*` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1SettingsAgentThinkOneItem` | `ThinkSettingsV1` | `deepgram.types.think_settings_v1` |
| `AgentV1SettingsAgentThinkOneItemContextLength` | `ThinkSettingsV1ContextLength` | `deepgram.types.think_settings_v1context_length` |
| `AgentV1SettingsAgentThinkOneItemEndpoint` | `ThinkSettingsV1Endpoint` | `deepgram.types.think_settings_v1endpoint` |
| `AgentV1SettingsAgentThinkOneItemFunctionsItem` | `ThinkSettingsV1FunctionsItem` | `deepgram.types.think_settings_v1functions_item` |
| `AgentV1SettingsAgentThinkOneItemFunctionsItemEndpoint` | `ThinkSettingsV1FunctionsItemEndpoint` | `deepgram.types.think_settings_v1functions_item_endpoint` |
| `AgentV1SettingsAgentThinkOneItemProvider` | `ThinkSettingsV1Provider` | `deepgram.types.think_settings_v1provider` |
| `AgentV1UpdateSpeakSpeakEndpoint` | `SpeakSettingsV1` | `deepgram.types.speak_settings_v1` |
| `AgentV1UpdateSpeakSpeakOneItem` | `SpeakSettingsV1` | `deepgram.types.speak_settings_v1` |
| `AgentV1UpdateSpeakSpeakEndpointProvider_*` | `SpeakSettingsV1Provider_*` | `deepgram.types.speak_settings_v1provider` |
| `AgentV1UpdateSpeakSpeakOneItemProvider_*` | `SpeakSettingsV1Provider_*` | `deepgram.types.speak_settings_v1provider` |

If you used generated request `*Params` typed dicts instead of model classes, the same consolidation applies in `deepgram.requests`.

**v6**

```python
from deepgram.agent.v1.types import (
    AgentV1SettingsAgentSpeakOneItem,
    AgentV1SettingsAgentSpeakOneItemProvider_Deepgram,
    AgentV1SettingsAgentThinkOneItem,
)
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

speak = [
    AgentV1SettingsAgentSpeakOneItem(
        provider=AgentV1SettingsAgentSpeakOneItemProvider_Deepgram(
            type="deepgram",
            model="aura-2-asteria-en",
        )
    )
]

think = [
    AgentV1SettingsAgentThinkOneItem(
        provider=ThinkSettingsV1Provider_OpenAi(
            type="open_ai",
            model="gpt-4o-mini",
        )
    )
]
```

**v7**

```python
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

speak = [
    SpeakSettingsV1(
        provider=SpeakSettingsV1Provider_Deepgram(
            type="deepgram",
            model="aura-2-asteria-en",
        )
    )
]

think = [
    ThinkSettingsV1(
        provider=ThinkSettingsV1Provider_OpenAi(
            type="open_ai",
            model="gpt-4o-mini",
        )
    )
]
```

### WebSocket Type Aliases

Several exported `*Type` aliases were removed. The underlying event objects still have a `.type` field, but the separate generated alias exports are gone.

Common examples:

| v6 | v7 |
|---|---|
| `ListenV1MetadataType` | Removed; use `typing.Literal["Metadata"]` or `str` |
| `ListenV1ResultsType` | Removed; use `typing.Literal["Results"]` or `str` |
| `ListenV1SpeechStartedType` | Removed; use `typing.Literal["SpeechStarted"]` or `str` |
| `ListenV1UtteranceEndType` | Removed; use `typing.Literal["UtteranceEnd"]` or `str` |
| `ListenV2ConnectedType` | Removed; use `typing.Literal["Connected"]` or `str` |
| `ListenV2FatalErrorType` | Removed; use `typing.Literal["FatalError"]` or `str` |
| `ListenV2TurnInfoType` | Removed; use `typing.Literal["TurnInfo"]` or `str` |
| `SpeakV1MetadataType` | Removed; use `typing.Literal["Metadata"]` or `str` |
| `SpeakV1TextType` | Removed; use `typing.Literal["Speak"]` or `str` |
| `SpeakV1WarningType` | Removed; use `typing.Literal["Warning"]` or `str` |
| `AgentV1WelcomeType` and other `AgentV1*Type` aliases | Removed; use `typing.Literal[...]` or `str` |

**v6**

```python
from deepgram.listen.v1.types import ListenV1MetadataType

event_type: ListenV1MetadataType = "Metadata"
```

**v7**

```python
from typing import Literal

event_type: Literal["Metadata"] = "Metadata"
```

In most application code, comparing `message.type` to a string continues to work unchanged.

### Other Removed Generated Types

Two smaller groups of generated helper types were also removed:

- `AgentThinkModelsV1ResponseModelsItem*Provider` helper exports
- `MediaTranscribeRequest*Zero` helper exports

If you were importing these low-level generated helpers directly, switch to the parent response/request types or the new shared provider types described above.

## Breaking Changes Summary

### Major Changes

1. **Python runtime support**: v7 requires Python 3.10 or newer.
2. **Voice agent generated types**: Agent think/speak settings and update types were consolidated into shared `SpeakSettingsV1*` and `ThinkSettingsV1*` schemas.
3. **WebSocket alias exports**: Separate generated `*Type` aliases were removed and inlined to `Literal[...]` values.

### Removed Features

- Python 3.8 support
- Python 3.9 support
- Agent-specific generated speak provider type families such as `AgentV1SettingsAgentSpeakOneItemProvider_*`
- Agent-specific generated think helper types such as `AgentV1SettingsAgentThinkOneItem`, `AgentV1SettingsAgentThinkOneItemProvider`, and related nested types
- Exported WebSocket `*Type` aliases such as `ListenV1MetadataType`, `SpeakV1TextType`, and `AgentV1WelcomeType`
- Low-level generated helper exports such as `MediaTranscribeRequest*Zero`

### New Features in v7

- **Listen V2 configure support**: `send_configure()` and generated `ListenV2Configure*` types
- **Agent think updates**: `send_update_think()` and generated `AgentV1ThinkUpdated` support
- **Agent history events**: generated `AgentV1History` types
- **Voice agent management APIs**: `client.voice_agent.configurations` and `client.voice_agent.variables`

### Migration Checklist

- [ ] Upgrade to Python 3.10+ if you are still on Python 3.8 or 3.9
- [ ] Upgrade to the latest SDK version: `pip install --upgrade deepgram-sdk`
- [ ] Replace any removed agent-specific think/speak imports with shared `SpeakSettingsV1*` and `ThinkSettingsV1*` types from `deepgram.types`
- [ ] Remove imports of exported WebSocket `*Type` aliases and use `typing.Literal[...]` or `str` instead
- [ ] Update any direct imports of low-level generated helper types such as `MediaTranscribeRequest*Zero`
- [ ] Re-run type checking and tests after updating imports
