# Deepgram Python SDK

![Built with Fern](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)
[![PyPI version](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.python.org/pypi/deepgram-sdk)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

The official Python SDK for Deepgram's automated speech recognition, text-to-speech, and language understanding APIs. Power your applications with world-class speech and Language AI models.

## Documentation

Comprehensive API documentation and guides are available at [developers.deepgram.com](https://developers.deepgram.com).

### Migrating From Earlier Versions

- [v2 to v3+](./docs/Migrating-v2-to-v3.md)
- [v3+ to v5](./docs/Migrating-v3-to-v5.md) (current)

## Installation

Install the Deepgram Python SDK using pip:

```bash
pip install deepgram-sdk
```

## Reference

- **[API Reference](./reference.md)** - Complete reference for all SDK methods and parameters
- **[WebSocket Reference](./websockets-reference.md)** - Detailed documentation for real-time WebSocket connections

## Usage

### Quick Start

The Deepgram SDK provides both synchronous and asynchronous clients for all major use cases:

#### Real-time Speech Recognition (Listen v2)

Our newest and most advanced speech recognition model with contextual turn detection ([WebSocket Reference](./websockets-reference.md#listen-v2-connect)):

```python
from deepgram import DeepgramClient
from deepgram.core.events import EventType

client = DeepgramClient()

with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate="16000"
) as connection:
    def on_message(message):
        print(f"Received {message.type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

    # Start listening and send audio data
    connection.start_listening()
```

#### File Transcription

Transcribe pre-recorded audio files ([API Reference](./reference.md#listen-v1-media-transcribe-file)):

```python
from deepgram import DeepgramClient

client = DeepgramClient()

with open("audio.wav", "rb") as audio_file:
    response = client.listen.v1.media.transcribe_file(
        request=audio_file.read(),
        model="nova-3"
    )
    print(response.results.channels[0].alternatives[0].transcript)
```

#### Text-to-Speech

Generate natural-sounding speech from text ([API Reference](./reference.md#speak-v1-audio-generate)):

```python
from deepgram import DeepgramClient

client = DeepgramClient()

response = client.speak.v1.audio.generate(
    text="Hello, this is a sample text to speech conversion."
)

# Save the audio file
with open("output.mp3", "wb") as audio_file:
    audio_file.write(response.stream.getvalue())
```

#### Text Analysis

Analyze text for sentiment, topics, and intents ([API Reference](./reference.md#read-v1-text-analyze)):

```python
from deepgram import DeepgramClient

client = DeepgramClient()

response = client.read.v1.text.analyze(
    request={"text": "Hello, world!"},
    language="en",
    sentiment=True,
    summarize=True,
    topics=True,
    intents=True
)
```

#### Voice Agent (Conversational AI)

Build interactive voice agents ([WebSocket Reference](./websockets-reference.md#agent-v1-connect)):

```python
from deepgram import DeepgramClient
from deepgram.extensions.types.sockets import (
    AgentV1SettingsMessage, AgentV1Agent, AgentV1AudioConfig,
    AgentV1AudioInput, AgentV1Listen, AgentV1ListenProvider,
    AgentV1Think, AgentV1OpenAiThinkProvider, AgentV1SpeakProviderConfig,
    AgentV1DeepgramSpeakProvider
)

client = DeepgramClient()

with client.agent.v1.connect() as agent:
    settings = AgentV1SettingsMessage(
        audio=AgentV1AudioConfig(
            input=AgentV1AudioInput(encoding="linear16", sample_rate=44100)
        ),
        agent=AgentV1Agent(
            listen=AgentV1Listen(
                provider=AgentV1ListenProvider(type="deepgram", model="nova-3")
            ),
            think=AgentV1Think(
                provider=AgentV1OpenAiThinkProvider(
                    type="open_ai", model="gpt-4o-mini"
                )
            ),
            speak=AgentV1SpeakProviderConfig(
                provider=AgentV1DeepgramSpeakProvider(
                    type="deepgram", model="aura-2-asteria-en"
                )
            )
        )
    )

    agent.send_settings(settings)
    agent.start_listening()
```

### Complete SDK Reference

For comprehensive documentation of all available methods, parameters, and options:

- **[API Reference](./reference.md)** - Complete reference for REST API methods including:

  - Listen (Speech-to-Text): File transcription, URL transcription, and media processing
  - Speak (Text-to-Speech): Audio generation and voice synthesis
  - Read (Text Intelligence): Text analysis, sentiment, summarization, and topic detection
  - Manage: Project management, API keys, and usage analytics
  - Auth: Token generation and authentication management

- **[WebSocket Reference](./websockets-reference.md)** - Detailed documentation for real-time connections:
  - Listen v1/v2: Real-time speech recognition with different model capabilities
  - Speak v1: Real-time text-to-speech streaming
  - Agent v1: Conversational voice agents with integrated STT, LLM, and TTS

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

The SDK provides full async/await support for non-blocking operations:

```python
import asyncio
from deepgram import AsyncDeepgramClient

async def main():
    client = AsyncDeepgramClient()

    # Async file transcription
    with open("audio.wav", "rb") as audio_file:
        response = await client.listen.v1.media.transcribe_file(
            request=audio_file.read(),
            model="nova-3"
        )

    # Async WebSocket connection
    async with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate="16000"
    ) as connection:
        async def on_message(message):
            print(f"Received {message.type} event")

        connection.on(EventType.MESSAGE, on_message)
        await connection.start_listening()

asyncio.run(main())
```

## Exception Handling

The SDK provides detailed error information for debugging and error handling:

```python
from deepgram import DeepgramClient
from deepgram.core.api_error import ApiError

client = DeepgramClient()

try:
    response = client.listen.v1.media.transcribe_file(
        request=audio_data,
        model="nova-3"
    )
except ApiError as e:
    print(f"Status Code: {e.status_code}")
    print(f"Error Details: {e.body}")
    print(f"Request ID: {e.headers.get('x-dg-request-id', 'N/A')}")
except Exception as e:
    print(f"Unexpected error: {e}")
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

## Contributing

We welcome contributions to improve this SDK! However, please note that this library is primarily generated from our API specifications.

### Development Setup

1. **Install Poetry** (if not already installed):

   ```bash
   curl -sSL https://install.python-poetry.org | python - -y --version 1.5.1
   ```

2. **Install dependencies**:

   ```bash
   poetry install
   ```

3. **Install example dependencies**:

   ```bash
   poetry run pip install -r examples/requirements.txt
   ```

4. **Run tests**:

   ```bash
   poetry run pytest -rP .
   ```

5. **Run examples**:
   ```bash
   python -u examples/listen/v2/connect/main.py
   ```

### Contribution Guidelines

See our [CONTRIBUTING](./CONTRIBUTING.md) guide.

### Requirements

- Python 3.8+
- See `pyproject.toml` for full dependency list

## Community Code of Conduct

Please see our community [code of conduct](https://developers.deepgram.com/code-of-conduct) before contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
