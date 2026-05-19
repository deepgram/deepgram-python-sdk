---
title: "Authentication And Clients"
description: "Set up the Deepgram Python SDK with API keys, temporary tokens, and sync or async clients."
---

This guide shows the recommended way to bootstrap the SDK, choose the right client class, and switch from long-lived API keys to temporary access tokens when needed.

<Steps>
<Step>

### Configure the environment

For server-side applications, set `DEEPGRAM_API_KEY` and let the SDK discover it automatically. This works because `BaseClient` in `src/deepgram/base_client.py` defaults `api_key` from the environment.

```bash
export DEEPGRAM_API_KEY="dg_your_api_key"
```

</Step>
<Step>

### Create the root client

Use the sync client for scripts or one-request-at-a-time applications.

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    timeout=30,
    headers={"X-App-Name": "docs-example"},
)
```

If your app already runs on `asyncio`, use the async client instead.

```python
from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient(timeout=30)
```

</Step>
<Step>

### Mint a temporary token when you need one

Tokens come from `client.auth.v1.tokens.grant()` in `src/deepgram/auth/v1/tokens/client.py`. Use this when you want a short-lived credential for a downstream client.

```python
from deepgram import DeepgramClient

issuer = DeepgramClient(api_key="dg_server_key")
token = issuer.auth.v1.tokens.grant(ttl_seconds=60)

browser_or_edge_client = DeepgramClient(
    access_token=token.access_token,
    session_id="session-123",
)
```

</Step>
<Step>

### Make a quick verification call

```python
response = client.read.v1.text.analyze(
    request={"text": "The package arrived on time and the customer is happy."},
    language="en",
    sentiment=True,
)

print(response.results.sentiments.average)
```

</Step>
</Steps>

## Full Example

```python
import asyncio
from deepgram import AsyncDeepgramClient


async def main() -> None:
    client = AsyncDeepgramClient(
        access_token="TEMPORARY_TOKEN",
        session_id="support-call-9001",
    )

    response = await client.read.v1.text.analyze(
        request={"text": "Please refund the extra shipping charge."},
        language="en",
        intents=True,
        sentiment=True,
        request_options={
            "additional_headers": {"X-Trace-Id": "trace-9001"},
            "timeout_in_seconds": 10,
        },
    )

    print(response.results.sentiments.average)


asyncio.run(main())
```

## Why This Pattern Works

- Auth stays at the root client, so domain modules inherit the same headers and session ID.
- Temporary tokens do not require you to rework the rest of the API surface.
- `RequestOptions` lets you tune one call without mutating the shared client object.
