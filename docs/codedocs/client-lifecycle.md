---
title: "Client Lifecycle"
description: "Learn how DeepgramClient and AsyncDeepgramClient handle auth, configuration, sessions, and per-request overrides."
---

The core abstraction in this SDK is the root client. Everything else hangs off `DeepgramClient` or `AsyncDeepgramClient`, so understanding client construction explains most of the SDK's behavior.

## What It Is

`deepgram.DeepgramClient` and `deepgram.AsyncDeepgramClient` are hand-written subclasses in `src/deepgram/client.py` that extend the generated `BaseClient` classes from `src/deepgram/base_client.py`. They solve three practical problems that the generated code alone does not solve well:

- choosing between API-key auth and bearer-token auth,
- attaching a stable session identifier to every request and websocket,
- swapping out the default WebSocket transport when you need a proxy, test double, or alternative runtime.

These root clients relate directly to `DeepgramClientEnvironment`, `RequestOptions`, and the domain clients under `listen`, `speak`, `read`, `manage`, `auth`, `agent`, `voice_agent`, and `self_hosted`.

## How It Works Internally

When you instantiate a client, `src/deepgram/client.py` pulls `access_token`, `session_id`, and `transport_factory` out of `**kwargs` before delegating to the generated base client. It then:

- creates or reuses an `x-deepgram-session-id` header,
- inserts a placeholder `api_key="token"` if you only passed an access token,
- overrides `client_wrapper.get_headers()` so REST and WebSocket calls both send `Authorization: bearer <token>`,
- optionally patches generated websocket modules via `install_transport(...)`.

The generated base classes in `src/deepgram/base_client.py` then create a shared `SyncClientWrapper` or `AsyncClientWrapper`. That wrapper stores the environment, base headers, timeout, and logging config, then exposes lazy properties for each domain client.

## Basic Usage

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
    timeout=30,
    headers={"X-App-Name": "support-bot"},
)

response = client.read.v1.text.analyze(
    request={"text": "The shipment arrived late, but support fixed it quickly."},
    language="en",
    sentiment=True,
    summarize=True,
)

print(response.results.summary.text)
```

## Advanced Usage

```python
from deepgram import AsyncDeepgramClient
from deepgram.core.request_options import RequestOptions

client = AsyncDeepgramClient(
    access_token="TEMPORARY_ACCESS_TOKEN",
    session_id="call-42",
)

request_options: RequestOptions = {
    "timeout_in_seconds": 10,
    "additional_headers": {"X-Trace-Id": "trace-42"},
    "additional_query_parameters": {"detect_language": ["en", "es"]},
}

# Any domain method can receive request_options without mutating client-wide config.
```

<Callout type="warn">If you pass both `api_key` and `access_token`, the SDK will still force bearer-token authorization. That behavior comes from `_apply_bearer_authorization_override(...)` in `src/deepgram/client.py`, so debugging auth issues should start there rather than in the generated REST clients.</Callout>

## Constructor Options

| Option | Type | Default | What it does |
|--------|------|---------|--------------|
| `environment` | `DeepgramClientEnvironment` | `DeepgramClientEnvironment.PRODUCTION` | Chooses the base HTTPS and WebSocket endpoints. |
| `api_key` | `str \| None` | `DEEPGRAM_API_KEY` | Server-side auth credential used by generated clients. |
| `access_token` | `str \| None` | `None` | Hand-written override that sends bearer auth instead of token auth. |
| `session_id` | `str \| None` | auto-generated UUID | Added as `x-deepgram-session-id` on every request and websocket. |
| `headers` | `dict[str, str] \| None` | `None` | Extra headers merged into the base wrapper headers. |
| `timeout` | `float \| None` | `60` unless a custom client is passed | Request timeout in seconds. |
| `follow_redirects` | `bool \| None` | `True` | Controls redirect behavior for the default `httpx` client. |
| `httpx_client` | `httpx.Client` or `httpx.AsyncClient` | generated default | Lets you bring your own transport, pools, proxies, or TLS settings. |
| `logging` | `LogConfig \| Logger \| None` | `None` | Enables SDK logging in the shared wrapper. |
| `transport_factory` | callable \| `None` | `None` | Globally replaces generated websocket connector calls. |

## Trade-Offs

<Accordions>
<Accordion title="Sync vs async clients">
The sync and async clients expose the same domain hierarchy, but their resource behavior is different. `DeepgramClient` is simpler for scripts, cron jobs, and request-at-a-time server handlers because it uses blocking `httpx.Client` and blocking websocket loops. `AsyncDeepgramClient` is a better fit when you already run an event loop and want to overlap many REST calls or streaming sessions without threads. The trade-off is operational: async gives you more concurrency, but you have to manage application shutdown carefully so pending streams and the async HTTP client do not outlive the loop.
</Accordion>
<Accordion title="API key auth vs access token auth">
API keys are the natural server-side default because the generated base clients already expect them and because they work across the full SDK surface, including manage APIs. Access tokens are better when you need temporary credentials or want tighter scoping, but they are injected through a hand-written override layer rather than the generated model. That makes them convenient, but also means debugging should focus on `src/deepgram/client.py` and the wrapper headers, not just your endpoint code. A practical rule is simple: use API keys for backend services, and mint access tokens with `client.auth.v1.tokens.grant()` when a short-lived credential is the safer boundary.
</Accordion>
<Accordion title="Global client config vs RequestOptions">
Client constructor options are the right place for values that should apply everywhere, such as environment, shared headers, or a standard timeout policy. `RequestOptions` is better for one-off exceptions like a larger `chunk_size`, extra query parameters, or a custom timeout for a single transcription. The advantage is isolation: you can make one noisy or slow request more permissive without weakening the rest of the application. The downside is that per-request overrides are easier to hide inside call sites, so teams should standardize which options belong at client construction and which belong at the edge of an individual request.
</Accordion>
</Accordions>
