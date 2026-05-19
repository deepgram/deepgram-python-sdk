---
title: "Deepgram Client"
description: "Reference for the root sync and async clients, shared configuration, and request options."
---

The root client layer lives in `src/deepgram/client.py` and `src/deepgram/base_client.py`. Import these classes from `deepgram`.

## Imports

```python
from deepgram import DeepgramClient, AsyncDeepgramClient, DeepgramClientEnvironment
from deepgram.core.request_options import RequestOptions
```

## Classes

### `DeepgramClient`

Source: `src/deepgram/client.py`

```python
DeepgramClient(
    *,
    environment: DeepgramClientEnvironment = DeepgramClientEnvironment.PRODUCTION,
    api_key: str | None = os.getenv("DEEPGRAM_API_KEY"),
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
    follow_redirects: bool | None = True,
    httpx_client: httpx.Client | None = None,
    logging: LogConfig | Logger | None = None,
    access_token: str | None = None,
    session_id: str | None = None,
    transport_factory: callable | None = None,
)
```

### `AsyncDeepgramClient`

Source: `src/deepgram/client.py`

```python
AsyncDeepgramClient(
    *,
    environment: DeepgramClientEnvironment = DeepgramClientEnvironment.PRODUCTION,
    api_key: str | None = os.getenv("DEEPGRAM_API_KEY"),
    headers: dict[str, str] | None = None,
    timeout: float | None = None,
    follow_redirects: bool | None = True,
    httpx_client: httpx.AsyncClient | None = None,
    logging: LogConfig | Logger | None = None,
    access_token: str | None = None,
    session_id: str | None = None,
    transport_factory: callable | None = None,
)
```

## Constructor Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `environment` | `DeepgramClientEnvironment` | `DeepgramClientEnvironment.PRODUCTION` | Chooses HTTPS and WebSocket base URLs. |
| `api_key` | `str \| None` | `DEEPGRAM_API_KEY` | Standard token-style credential for generated clients. |
| `access_token` | `str \| None` | `None` | Forces bearer auth through the hand-written override layer. |
| `session_id` | `str \| None` | auto-generated UUID | Sent as `x-deepgram-session-id` on REST and WebSocket calls. |
| `headers` | `dict[str, str] \| None` | `None` | Extra shared headers. |
| `timeout` | `float \| None` | `60` when using default clients | Base timeout in seconds. |
| `follow_redirects` | `bool \| None` | `True` | Redirect handling for default `httpx` clients. |
| `httpx_client` | `httpx.Client \| httpx.AsyncClient \| None` | generated default | Bring-your-own HTTP transport, pools, or proxies. |
| `logging` | `LogConfig \| Logger \| None` | `None` | Shared SDK logging config. |
| `transport_factory` | callable \| `None` | `None` | Global override for generated websocket transport calls. |

## Domain Properties

These properties are created lazily in `src/deepgram/base_client.py`.

| Property | Return type | Import path |
|----------|-------------|-------------|
| `agent` | `AgentClient` / `AsyncAgentClient` | `deepgram.agent` |
| `auth` | `AuthClient` / `AsyncAuthClient` | `deepgram.auth` |
| `listen` | `ListenClient` / `AsyncListenClient` | `deepgram.listen` |
| `manage` | `ManageClient` / `AsyncManageClient` | `deepgram.manage` |
| `read` | `ReadClient` / `AsyncReadClient` | `deepgram.read` |
| `self_hosted` | `SelfHostedClient` / `AsyncSelfHostedClient` | `deepgram.self_hosted` |
| `speak` | `SpeakClient` / `AsyncSpeakClient` | `deepgram.speak` |
| `voice_agent` | `VoiceAgentClient` / `AsyncVoiceAgentClient` | `deepgram.voice_agent` |

## Supporting Types

### `DeepgramClientEnvironment`

Source: `src/deepgram/environment.py`

```python
class DeepgramClientEnvironment:
    PRODUCTION: DeepgramClientEnvironment
    AGENT: DeepgramClientEnvironment

    def __init__(self, *, base: str, agent: str, production: str)
```

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

## Example

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    access_token="TEMP_TOKEN",
    session_id="call-17",
    headers={"X-App-Name": "triage-worker"},
)

response = client.read.v1.text.analyze(
    request={"text": "Customer wants to upgrade the subscription."},
    intents=True,
    request_options={"timeout_in_seconds": 15},
)
```

## Related Pages

- `/docs/api-reference/listen`
- `/docs/api-reference/speak`
- `/docs/client-lifecycle`
