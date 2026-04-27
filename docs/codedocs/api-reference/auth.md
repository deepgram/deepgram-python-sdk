---
title: "Auth"
description: "Reference for token generation in the Deepgram Python SDK."
---

The Auth domain is intentionally small. Its main job is to mint temporary access tokens from an API key.

## Imports

```python
from deepgram import DeepgramClient
```

Source files:

- `src/deepgram/auth/client.py`
- `src/deepgram/auth/v1/client.py`
- `src/deepgram/auth/v1/tokens/client.py`

## `TokensClient.grant`

Import path: `client.auth.v1.tokens`

```python
grant(
    *,
    ttl_seconds: float | None = OMIT,
    request_options: RequestOptions | None = None,
) -> GrantV1Response
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ttl_seconds` | `float \| None` | API default, documented as 30 seconds | Lifetime for the generated JWT. |
| `request_options` | `RequestOptions \| None` | `None` | Per-request headers, retries, and timeout. |

## Example

```python
issuer = DeepgramClient(api_key="dg_server_key")
token = issuer.auth.v1.tokens.grant(ttl_seconds=60)

client = DeepgramClient(access_token=token.access_token)
```

## Notes

- The generated docstring in `src/deepgram/auth/v1/tokens/client.py` states that the token carries `usage::write` permission for core voice APIs.
- Tokens created here do not replace the Manage APIs for project administration.
