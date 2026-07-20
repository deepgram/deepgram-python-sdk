---
name: deepgram-python-voice-agent
description: Use when writing or reviewing Python code in this repo that builds an interactive voice agent via `agent.deepgram.com/v1/agent/converse`. Covers `client.agent.v1.connect()`, `AgentV1Settings`, `send_settings`, `send_media`, event handling, and function/tool calling. Full-duplex STT + LLM + TTS with barge-in. Use `deepgram-python-text-to-speech` for one-way synthesis, `deepgram-python-speech-to-text` / `deepgram-python-conversational-stt` for transcription only. Triggers include "voice agent", "agent converse", "full duplex", "interactive assistant", "barge-in", "agent.v1", "function calling", "AgentV1Settings".
---

# Using Deepgram Voice Agent (Python SDK)

Full-duplex voice agent runtime: STT + LLM (think) + TTS + function calling over a single WebSocket at `agent.deepgram.com/v1/agent/converse`.

**Use a different skill when:**
- One-way transcription → `deepgram-python-speech-to-text` or `deepgram-python-conversational-stt`.
- One-way synthesis → `deepgram-python-text-to-speech`.
- Analytics on finished audio → `deepgram-python-audio-intelligence`.
- Managing reusable agent configs → `deepgram-python-management-api`.

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

`Welcome`, `SettingsApplied`, `ConversationText` (with `role`), `UserStartedSpeaking`, `AgentThinking`, `FunctionCallRequest`, `AgentStartedSpeaking`, binary audio frames, `AgentAudioDone`, `Warning`, `Error`.

## Reusable agent configurations

Persist the `agent` block server-side via `client.voice_agent.configurations.*` and reference by `agent_id` in future Settings messages. See `deepgram-python-management-api` for CRUD operations.

## Dynamic mid-session adjustment

Change agent behavior without disconnecting via control messages. Key methods on the agent connection object:

| Method | Type | Server reply | Notes |
|---|---|---|---|
| `send_update_prompt(AgentV1UpdatePrompt(prompt="..."))` | `AgentV1UpdatePrompt` | `PromptUpdated` | Swap system prompt |
| `send_update_speak(AgentV1UpdateSpeak(speak=SpeakSettingsV1(...)))` | `AgentV1UpdateSpeak` | `SpeakUpdated` | Swap TTS voice/model |
| `send_update_think(AgentV1UpdateThink(think=ThinkSettingsV1(...)))` | `AgentV1UpdateThink` | `ThinkUpdated` | Swap LLM provider/model |
| `send_inject_agent_message(AgentV1InjectAgentMessage(message="..."))` | `AgentV1InjectAgentMessage` | — | Force agent to speak |
| `send_inject_user_message(AgentV1InjectUserMessage(content="..."))` | `AgentV1InjectUserMessage` | may `InjectionRefused` | Inject text as user; retry after `AgentAudioDone` if refused |
| `send_keep_alive()` | `AgentV1KeepAlive` | — | Idle keep-alive (every ~5s) |

Import types from `deepgram.agent.v1.types` and provider types from `deepgram.types.*`. Async equivalents are `await`-prefixed.

## Stream lifecycle & recovery

- **Pause / idle:** Stop sending audio but emit `send_keep_alive()` every ~5s. Server closes at ~10s idle without keepalive.
- **Resume:** Just call `send_media` again -- no control message needed.
- **Reconnect (preserve context):** Open a new connection, resend `Settings` with prior turns in `Settings.agent.context.messages` (types: `AgentV1SettingsAgentContext`, `AgentV1SettingsAgentContextMessagesItem`, `AgentV1SettingsAgentContextMessagesItemContent`, `AgentV1SettingsAgentContextMessagesItemContentRole`). Use `settings.model_copy(update={"agent": settings.agent.model_copy(update={"context": context})})`.
- **Detect disconnects:** `EventType.CLOSE` fires before the `with` block exits. Check `EventType.ERROR` payloads for cause. The server emits an `AgentV1History` object (`"History"` wire type) on connect -- persist these turns for reconnect context.

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

1. **Auth:** API keys use `Token <api_key>`. Access tokens (from `client.auth.v1.tokens.grant()`) use `Bearer`. The SDK's `access_token=` param installs the override -- see `src/deepgram/client.py`.
2. **Base URL is `agent.deepgram.com`**, not `api.deepgram.com`.
3. **Send `Settings` IMMEDIATELY after connect** -- no audio before settings are applied.
4. **Function call responses are synchronous to the turn** -- reply promptly or the agent stalls.
5. **Provider types are tagged unions** (`ThinkSettingsV1Provider_OpenAi`, `SpeakSettingsV1Provider_Deepgram`, ...). Pick the right variant; don't pass raw dicts.
6. **`socket_client.py` is temporarily frozen** (`.fernignore` → `src/deepgram/agent/v1/socket_client.py`) with `_sanitize_numeric_types` + `construct_type` fixes for unknown WS message shapes.

## Example files in this repo

- `examples/30-voice-agent.py`
- `tests/manual/agent/v1/connect/main.py` — live connection test

For cross-language Deepgram product knowledge, install the central skills: `npx skills add deepgram/skills`.
