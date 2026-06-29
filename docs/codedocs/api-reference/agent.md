---
title: "Agent"
description: "Reference for the realtime agent websocket and think-model discovery APIs."
---

The Agent domain is the runtime surface for realtime conversational sessions.

## Imports

```python
from deepgram import DeepgramClient
from deepgram.agent.v1.types import AgentV1Settings
```

Source files:

- `src/deepgram/agent/v1/client.py`
- `src/deepgram/agent/v1/socket_client.py`
- `src/deepgram/agent/v1/settings/think/models/client.py`

## `V1Client.connect`

Import path: `client.agent.v1`

```python
connect(
    *,
    authorization: str | None = None,
    request_options: RequestOptions | None = None,
) -> Iterator[V1SocketClient]
```

## `V1SocketClient` Methods

Source: `src/deepgram/agent/v1/socket_client.py`

- `start_listening()`
- `send_settings(message: AgentV1Settings) -> None`
- `send_update_speak(message: AgentV1UpdateSpeak) -> None`
- `send_inject_user_message(message: AgentV1InjectUserMessage) -> None`
- `send_inject_agent_message(message: AgentV1InjectAgentMessage) -> None`
- `send_function_call_response(message: AgentV1SendFunctionCallResponse) -> None`
- `send_keep_alive(message: AgentV1KeepAlive | None = None) -> None`
- `send_update_prompt(message: AgentV1UpdatePrompt) -> None`
- `send_update_think(message: AgentV1UpdateThink) -> None`
- `send_media(message: bytes) -> None`
- `recv() -> V1SocketClientResponse`

`V1SocketClientResponse` is a union of typed agent events such as `AgentV1ConversationText`, `AgentV1AgentThinking`, `AgentV1FunctionCallRequest`, `AgentV1Warning`, `AgentV1History`, plus raw `bytes` audio.

## Think Model Discovery

Import path: `client.agent.v1.settings.think.models`

```python
list(*, request_options: RequestOptions | None = None) -> AgentThinkModelsV1Response
```

This endpoint comes from `src/deepgram/agent/v1/settings/think/models/client.py` and lets you inspect supported think providers before composing agent settings.

## Example

```python
with client.agent.v1.connect() as agent:
    agent.send_settings(settings)
    agent.send_media(b"...audio chunk...")
    agent.start_listening()
```

## Implementation Note

Before sending a Pydantic model, the socket client runs `_sanitize_numeric_types(...)`. That helper converts values such as `24000.0` into `24000` so integer-only API fields survive serialization correctly.
