# Deepgram API Python Library

![](https://developers.deepgram.com)

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fdeepgram%2Fdeepgram-python-sdk)
[![pypi](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.python.org/pypi/deepgram-sdk)

Power your apps with world-class speech and Language AI models

## Table of Contents

- [Documentation](#documentation)
- [Installation](#installation)
- [Reference](#reference)
- [Usage](#usage)
- [Authentication](#authentication)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Advanced Features](#advanced-features)
- [Websockets](#websockets)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Contributing](#contributing)
- [Community Code of Conduct](#community-code-of-conduct)
- [License](#license)

## Documentation

API reference documentation is available [here](https://developers.deepgram.com/reference/deepgram-api-overview).

## Installation

```sh
pip install deepgram-sdk
```

## Reference

A full reference for this library is available [here](https://github.com/deepgram/deepgram-python-sdk/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.listen.v1.media.transcribe_file()
```

## Authentication

The Deepgram SDK supports two authentication methods:

### Access Token Authentication

Use access tokens for temporary or scoped access (recommended for client-side applications):

```python
from deepgram import DeepgramClient

# Explicit access token
client = DeepgramClient(access_token="YOUR_ACCESS_TOKEN")

# Or via environment variable DEEPGRAM_TOKEN
client = DeepgramClient()

# Generate access tokens using your API key
auth_client = DeepgramClient(api_key="YOUR_API_KEY")
token_response = auth_client.auth.v1.tokens.grant()
token_client = DeepgramClient(access_token=token_response.access_token)
```

### API Key Authentication

Use your Deepgram API key for server-side applications:

```python
from deepgram import DeepgramClient

# Explicit API key
client = DeepgramClient(api_key="YOUR_API_KEY")

# Or via environment variable DEEPGRAM_API_KEY
client = DeepgramClient()
```

### Environment Variables

The SDK automatically discovers credentials from these environment variables:

- `DEEPGRAM_TOKEN` - Your access token (takes precedence)
- `DEEPGRAM_API_KEY` - Your Deepgram API key

**Precedence:** Explicit parameters > Environment variables

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient(
    api_key="YOUR_API_KEY",
)


async def main() -> None:
    await client.listen.v1.media.transcribe_file()


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from deepgram.core.api_error import ApiError

try:
    client.listen.v1.media.transcribe_file(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Advanced Features

### Raw Response Access

Access raw HTTP response data including headers:

```python
from deepgram import DeepgramClient

client = DeepgramClient()

response = client.listen.v1.media.with_raw_response.transcribe_file(
    request=audio_data,
    model="nova-3"
)

print(response.headers)  # Access response headers
print(response.data)     # Access the response object
```

### Request Configuration

Configure timeouts, retries, and other request options:

```python
from deepgram import DeepgramClient

# Global client configuration
client = DeepgramClient(timeout=30.0)

# Per-request configuration
response = client.listen.v1.media.transcribe_file(
    request=audio_data,
    model="nova-3",
    request_options={
        "timeout_in_seconds": 60,
        "max_retries": 3
    }
)
```

### Custom HTTP Client

Use a custom httpx client for advanced networking features:

```python
import httpx
from deepgram import DeepgramClient

client = DeepgramClient(
    httpx_client=httpx.Client(
        proxies="http://proxy.example.com",
        timeout=httpx.Timeout(30.0)
    )
)
```

### Retry Configuration

The SDK automatically retries failed requests with exponential backoff:

```python
# Automatic retries for 408, 429, and 5xx status codes
response = client.listen.v1.media.transcribe_file(
    request=audio_data,
    model="nova-3",
    request_options={"max_retries": 3}
)
```

## Websockets

The SDK supports both sync and async websocket connections for real-time, low-latency communication. Sockets can be created using the `connect` method, which returns a context manager. 
You can either iterate through the returned `SocketClient` to process messages as they arrive, or attach handlers to respond to specific events.

```python

# Connect to the websocket (Sync)
import threading

from deepgram import DeepgramClient

client = DeepgramClient(...)

with client.v1.connect() as socket:
    # Iterate over the messages as they arrive
    for message in socket
        print(message)

    # Or, attach handlers to specific events
    socket.on(EventType.OPEN, lambda _: print("open"))
    socket.on(EventType.MESSAGE, lambda message: print("received message", message))
    socket.on(EventType.CLOSE, lambda _: print("close"))
    socket.on(EventType.ERROR, lambda error: print("error", error))


    # Start the listening loop in a background thread
    listener_thread = threading.Thread(target=socket.start_listening, daemon=True)
    listener_thread.start()
```

```python

# Connect to the websocket (Async)
import asyncio

from deepgram import AsyncDeepgramClient

client = AsyncDeepgramClient(...)

async with client.v1.connect() as socket:
    # Iterate over the messages as they arrive
    async for message in socket
        print(message)

    # Or, attach handlers to specific events
    socket.on(EventType.OPEN, lambda _: print("open"))
    socket.on(EventType.MESSAGE, lambda message: print("received message", message))
    socket.on(EventType.CLOSE, lambda _: print("close"))
    socket.on(EventType.ERROR, lambda error: print("error", error))


    # Start listening for events in an asyncio task
    listen_task = asyncio.create_task(socket.start_listening())
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    ...,
)
response = client.listen.v1.media.with_raw_response.transcribe_file(...)
print(response.headers)  # access the response headers
print(response.status_code)  # access the response status code
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.listen.v1.media.transcribe_file(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from deepgram import DeepgramClient

client = DeepgramClient(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.listen.v1.media.transcribe_file(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from deepgram import DeepgramClient

client = DeepgramClient(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
## Community Code of Conduct

Please see our community [code of conduct](https://developers.deepgram.com/code-of-conduct) before contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

