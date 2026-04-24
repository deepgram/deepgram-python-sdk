---
name: deepgram-python-voice-agent
description: Use when writing or reviewing Python code in this repo that builds an interactive voice agent via `agent.deepgram.com/v1/agent/converse`. Covers `client.agent.v1.connect()`, `AgentV1Settings`, `send_settings`, `send_media`, event handling, and function/tool calling. Full-duplex STT + LLM + TTS with barge-in. Use `deepgram-python-text-to-speech` for one-way synthesis, `deepgram-python-speech-to-text` / `deepgram-python-conversational-stt` for transcription only. Triggers include "voice agent", "agent converse", "full duplex", "interactive assistant", "barge-in", "agent.v1", "function calling", "AgentV1Settings".
---

# Using Deepgram Voice Agent (Python SDK)

Full-duplex voice agent runtime: STT + LLM (think) + TTS + function calling over a single WebSocket at `agent.deepgram.com/v1/agent/converse`.

## When to use this product

- You want an **interactive voice assistant**: user speaks, agent thinks, agent speaks, interruptions allowed.
- You want **function / tool calling** triggered by the conversation.
- You want Deepgram to host the orchestration (vs wiring STT + LLM + TTS yourself).

**Use a different skill when:**
- One-way transcription → `deepgram-python-speech-to-text` or `deepgram-python-conversational-stt`.
- One-way synthesis → `deepgram-python-text-to-speech`.
- Analytics on finished audio → `deepgram-python-audio-intelligence`.
- Managing reusable agent configs (persisted on the server) → `deepgram-python-management-api`.

## Authentication

```python
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient()
```

Header: `Authorization: Token <api_key>`. Base URL: `wss://agent.deepgram.com/v1/agent/converse`.

## Quick start

```python
import threading, time
from deepgram.core.events import EventType
from deepgram.agent.v1.types import (
    AgentV1Settings,
    AgentV1SettingsAgent,
    AgentV1SettingsAgentListen,
    AgentV1SettingsAgentListenProvider_V1,
    AgentV1SettingsAudio,
    AgentV1SettingsAudioInput,
)
from deepgram.types.speak_settings_v1 import SpeakSettingsV1
from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
from deepgram.types.think_settings_v1 import ThinkSettingsV1
from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

with client.agent.v1.connect() as agent:
    settings = AgentV1Settings(
        audio=AgentV1SettingsAudio(
            input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000),
        ),
        agent=AgentV1SettingsAgent(
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3"),
            ),
            think=ThinkSettingsV1(
                provider=ThinkSettingsV1Provider_OpenAi(
                    type="open_ai", model="gpt-4o-mini", temperature=0.7,
                ),
                prompt="You are a helpful assistant. Keep replies brief.",
            ),
            speak=SpeakSettingsV1(
                provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en"),
            ),
        ),
    )

    agent.send_settings(settings)   # MUST be first message after connect

    def on_message(m):
        if isinstance(m, bytes):
            # agent speech audio — play or append to output buffer
            return
        t = getattr(m, "type", "Unknown")
        if t == "ConversationText":
            print(f"[{getattr(m, 'role', '?')}] {getattr(m, 'content', '')}")
        elif t == "UserStartedSpeaking":  print(">> user speaking")
        elif t == "AgentThinking":        print(">> agent thinking")
        elif t == "AgentStartedSpeaking": print(">> agent speaking")
        elif t == "AgentAudioDone":       print(">> agent done")
        elif t == "FunctionCallRequest":  handle_tool_call(m)

    agent.on(EventType.OPEN,    lambda _: print("open"))
    agent.on(EventType.MESSAGE, on_message)
    agent.on(EventType.CLOSE,   lambda _: print("close"))
    agent.on(EventType.ERROR,   lambda e: print(f"err: {e}"))

    def send_audio():
        for chunk in mic_chunks():
            agent.send_media(chunk)

    threading.Thread(target=send_audio, daemon=True).start()
    agent.start_listening()   # blocks
```

## Event types (server → client)

- `Welcome` — connection acknowledged
- `SettingsApplied` — your `Settings` accepted
- `ConversationText` — text of a turn (with `role`: `user` or `assistant`)
- `UserStartedSpeaking` — VAD detected user
- `AgentThinking` — LLM is working
- `FunctionCallRequest` — tool/function call initiated by the model
- `AgentStartedSpeaking` — TTS starting
- Binary frames — audio chunks
- `AgentAudioDone` — TTS finished for this turn
- `Warning`, `Error`

## Client messages

- Initial `Settings` (send first)
- `Media` (binary audio frames in declared encoding/sample_rate)
- `KeepAlive` (on long sessions)
- Prompt / think / speak update messages (change mid-session)
- User / assistant text injection
- Function call response (reply to `FunctionCallRequest`)

## Reusable agent configurations

You can persist the **`agent` block** of a Settings message server-side and reuse it by `agent_id`. `client.voice_agent.configurations.create` stores a JSON string representing the `agent` object only (listen / think / speak providers + prompt) — NOT the full `AgentV1Settings` payload. Do not send top-level Settings fields like `audio` to that API; those still go in the live Settings message at connect time. The returned `agent_id` replaces the inline `agent` object in future Settings messages. Managed via `client.voice_agent.configurations.*` — see `deepgram-python-management-api`.

## API reference (layered)

1. **In-repo reference**: `reference.md` — "Agent V1 Connect", "Voice Agent Configurations".
2. **AsyncAPI (WSS)**: https://developers.deepgram.com/asyncapi.yaml
3. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
4. **Product docs**:
   - https://developers.deepgram.com/reference/voice-agent/voice-agent
   - https://developers.deepgram.com/docs/voice-agent
   - https://developers.deepgram.com/docs/configure-voice-agent
   - https://developers.deepgram.com/docs/voice-agent-message-flow

## Gotchas

1. **Pick the right auth scheme for the credential type.** API keys use `Authorization: Token <api_key>`. Temporary / access tokens (created via `client.auth.v1.tokens.grant()` or an equivalent server) use `Authorization: Bearer <access_token>`. The custom `DeepgramClient` in this repo accepts an `access_token` parameter and installs a Bearer override for all HTTP + WebSocket calls — see `src/deepgram/client.py`.
2. **Base URL is `agent.deepgram.com`, not `api.deepgram.com`.**
3. **Send `Settings` IMMEDIATELY after connect** — no audio before settings are applied.
4. **Listen/speak encoding + sample_rate must match** both your input audio and your playback path.
5. **Keepalive on long idle sessions**, otherwise the server closes.
6. **Function call responses are synchronous to the turn** — reply promptly.
7. **Provider types are tagged unions** (`ThinkSettingsV1Provider_OpenAi`, `SpeakSettingsV1Provider_Deepgram`, ...). Pick the right union variant; don't pass raw dicts.
8. **`socket_client.py` is temporarily frozen** (see `.fernignore` → `src/deepgram/agent/v1/socket_client.py`) and currently carries `_sanitize_numeric_types` plus the `construct_type` / broad-catch fixes — needed for unknown WS message shapes. Expected to be unfrozen during a future Fern regen and re-compared.

## Example files in this repo

- `examples/30-voice-agent.py`
- `tests/manual/agent/v1/connect/main.py` — live connection test

## Central product skills

For cross-language Deepgram product knowledge — the consolidated API reference, documentation finder, focused runnable recipes, third-party integration examples, and MCP setup — install the central skills:

```bash
npx skills add deepgram/skills
```

This SDK ships language-idiomatic code skills; `deepgram/skills` ships cross-language product knowledge (see `api`, `docs`, `recipes`, `examples`, `starters`, `setup-mcp`).
