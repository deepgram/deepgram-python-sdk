# v3+ to v5 Migration Guide

This guide helps you migrate from Deepgram Python SDK v3+ (versions 3.0.0 to 4.8.1) to v5.0.0. The v5 release introduces significant improvements including better type safety, cleaner API design, and enhanced WebSocket functionality.

## Table of Contents

- [Installation Changes](#installation-changes)
- [Configuration Changes](#configuration-changes)
- [Authentication Changes](#authentication-changes)
- [API Method Changes](#api-method-changes)
  - [Auth V1](#auth-v1)
  - [Listen V1](#listen-v1)
  - [Speak V1](#speak-v1)
  - [Agent V1](#agent-v1)
  - [Read V1](#read-v1)
  - [Models V1](#models-v1)
  - [Manage V1](#manage-v1)
  - [Self-Hosted V1](#self-hosted-v1)
- [Breaking Changes Summary](#breaking-changes-summary)

## Installation

To upgrade from v3+ to v5.0.0:

```bash
pip install --upgrade deepgram-sdk
```

## Configuration Changes

### v3+ Client Initialization

```python
from deepgram import DeepgramClient

# Basic initialization
deepgram = DeepgramClient("YOUR_API_KEY")

# With configuration
from deepgram import DeepgramClientOptions
config = DeepgramClientOptions(api_key="your-api-key")
client = DeepgramClient(config=config)
```

### v5.0.0 Client Initialization

```python
from deepgram import DeepgramClient

# API key authentication (server-side)
client = DeepgramClient(api_key="YOUR_API_KEY")

# Access token authentication (recommended for client-side)
client = DeepgramClient(access_token="YOUR_ACCESS_TOKEN")

# Environment variable authentication
# Set DEEPGRAM_API_KEY or DEEPGRAM_TOKEN
client = DeepgramClient()

# With custom HTTP client
import httpx
client = DeepgramClient(
    httpx_client=httpx.Client(
        proxies="http://proxy.example.com",
        timeout=httpx.Timeout(30.0)
    )
)
```

## Authentication Changes

### Environment Variables

- **v3+**: `DEEPGRAM_API_KEY`
- **v5.0.0**: `DEEPGRAM_TOKEN` (takes precedence) or `DEEPGRAM_API_KEY`

### Authentication Priority (v5.0.0)

1. Explicit `access_token` parameter (highest priority)
2. Explicit `api_key` parameter
3. `DEEPGRAM_TOKEN` environment variable
4. `DEEPGRAM_API_KEY` environment variable (lowest priority)

## API Method Changes

### Auth V1

#### Grant Token

**v3+ (3.0.0 - 4.8.1)**

```python
response = deepgram.auth.v("1").grant_token()
```

**v5.0.0**

```python
response = client.auth.v1.tokens.grant()

# With custom TTL
response = client.auth.v1.tokens.grant(ttl_seconds=60)
```

### Listen V1

#### Response Types

In v5.0.0, there are two types of responses for transcription requests:

1. **Synchronous Response**: When no callback is provided, returns the full transcription result immediately
2. **Asynchronous Response**: When a callback URL is provided, returns a "listen accepted" response and sends the actual transcription to the callback URL

#### Transcribe URL

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import PrerecordedOptions, UrlSource

payload: UrlSource = {
    "url": "https://dpgr.am/spacewalk.wav"
}

options = PrerecordedOptions(model="nova-3")

response = deepgram.listen.rest.v("1").transcribe_url(
    payload,
    options
)
```

**v5.0.0**

```python
# Returns the full transcription result immediately (synchronous)
response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    model="nova-3"
)
```

#### Transcribe File

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import PrerecordedOptions, FileSource

with open("path/to/your/audio.wav", "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(model="nova-3")

response = deepgram.listen.rest.v("1").transcribe_file(
    payload,
    options
)
```

**v5.0.0**

```python
# Returns the full transcription result immediately (synchronous)
with open("audio.wav", "rb") as audio_file:
    response = client.listen.v1.media.transcribe_file(
        request=audio_file.read(),
        model="nova-3"
    )
```

#### Transcribe URL with Callback (Asynchronous)

**v3+ (3.0.0 - 4.8.1)**

```python
response = deepgram.listen.rest.v("1").transcribe_url_callback(
    payload,
    "https://your-callback-url.com/webhook",
    options=options
)
```

**v5.0.0**

```python
# Returns a listen accepted response (not the full transcription)
response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    callback="https://your-callback-url.com/webhook",
    model="nova-3"
)
# The actual transcription will be sent to the callback URL
```

#### Transcribe File with Callback (Asynchronous)

**v3+ (3.0.0 - 4.8.1)**

```python
response = deepgram.listen.rest.v("1").transcribe_file_callback(
    payload,
    "https://your-callback-url.com/webhook",
    options=options
)
```

**v5.0.0**

```python
# Returns a listen accepted response (not the full transcription)
with open("audio.wav", "rb") as audio_file:
    response = client.listen.v1.media.transcribe_file(
        request=audio_file.read(),
        callback="https://your-callback-url.com/webhook",
        model="nova-3"
    )
# The actual transcription will be sent to the callback URL
```

#### WebSocket Streaming (Listen V1)

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import LiveOptions, LiveTranscriptionEvents

connection = deepgram.listen.websocket.v("1")

@connection.on(LiveTranscriptionEvents.Transcript)
def handle_transcript(result):
    print(result.channel.alternatives[0].transcript)

connection.start(LiveOptions(model="nova-3", language="en-US"))
connection.send(open("path/to/your/audio.wav", "rb").read())
connection.finish()
```

**v5.0.0**

```python
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import ListenV1SocketClientResponse

with client.listen.v1.connect(model="nova-3") as connection:
    def on_message(message: ListenV1SocketClientResponse) -> None:
        msg_type = getattr(message, "type", "Unknown")
        print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

    connection.start_listening()

    # Send audio data (as raw bytes)
    connection.send_media(audio_bytes)

```

#### WebSocket Streaming (Listen V2 - New in v5.0.0)

**v5.0.0**

```python
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

    connection.start_listening()
```

### Speak V1

#### Generate Audio (REST)

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import SpeakOptions

options = SpeakOptions(model="aura-2-thalia-en")

response = deepgram.speak.rest.v("1").save(
    "output.mp3",
    {"text": "Hello world!"},
    options
)
```

**v5.0.0**

```python
response = client.speak.v1.audio.generate(
    text="Hello, this is a sample text to speech conversion.",
    model="aura-2-asteria-en"
)

# Save the audio file
with open("output.mp3", "wb") as audio_file:
    audio_file.write(response.stream.getvalue())
```

#### WebSocket Streaming (Speak V1)

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import (
    SpeakWSOptions,
    SpeakWebSocketEvents
)

connection = deepgram.speak.websocket.v("1")

@connection.on(SpeakWebSocketEvents.AudioData)
def handle_audio_data(data):
    # Handle audio data
    pass

options = SpeakWSOptions(
    model="aura-2-thalia-en",
    encoding="linear16",
    sample_rate=16000
)

connection.start(options)
connection.send_text("Hello, this is a text to speech example.")
connection.flush()
connection.wait_for_complete()
connection.finish()
```

**v5.0.0**

```python
from deepgram.extensions.types.sockets import SpeakV1SocketClientResponse

with client.speak.v1.connect(
    model="aura-2-asteria-en",
    encoding="linear16",
    sample_rate=24000
) as connection:
    def on_message(message: SpeakV1SocketClientResponse) -> None:
        if isinstance(message, bytes):
            print("Received audio event")
        else:
            msg_type = getattr(message, "type", "Unknown")
            print(f"Received {msg_type} event")

    connection.on(EventType.OPEN, lambda _: print("Connection opened"))
    connection.on(EventType.MESSAGE, on_message)
    connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
    connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

    connection.start_listening()

    # Send text to be converted to speech
    from deepgram.extensions.types.sockets import SpeakV1TextMessage
    connection.send_text(SpeakV1TextMessage(text="Hello, world!"))

    # Send control messages
    from deepgram.extensions.types.sockets import SpeakV1ControlMessage
    connection.send_control(SpeakV1ControlMessage(type="Flush"))
    connection.send_control(SpeakV1ControlMessage(type="Close"))
```

### Agent V1

#### Voice Agent Configuration

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import (
    SettingsOptions,
    Speak
)

connection = deepgram.agent.websocket.v("1")

options = SettingsOptions()
options.language = "en"
options.agent.think.provider.type = "open_ai"
options.agent.think.provider.model = "gpt-4o-mini"
options.agent.think.prompt = "You are a helpful AI assistant."
options.agent.listen.provider.type = "deepgram"
options.agent.listen.provider.model = "nova-3"

primary = Speak()
primary.provider.type = "deepgram"
primary.provider.model = "aura-2-zeus-en"

options.agent.speak = [primary]
options.greeting = "Hello, I'm your AI assistant."

connection.start(options)
```

**v5.0.0**

```python
from deepgram.extensions.types.sockets import (
    AgentV1SettingsMessage, AgentV1Agent, AgentV1AudioConfig,
    AgentV1AudioInput, AgentV1Listen, AgentV1ListenProvider,
    AgentV1Think, AgentV1OpenAiThinkProvider, AgentV1SpeakProviderConfig,
    AgentV1DeepgramSpeakProvider
)

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

### Read V1

#### Text Analysis

**v3+ (3.0.0 - 4.8.1)**

```python
from deepgram import AnalyzeOptions, TextSource

options = AnalyzeOptions(
    sentiment=True,
    intents=True,
    topics=True,
    summarize=True
)

payload: TextSource = {
    "buffer": "The quick brown fox jumps over the lazy dog."
}

response = deepgram.read.analyze.v("1").analyze_text(
    payload,
    options
)
```

**v5.0.0**

```python
response = client.read.v1.text.analyze(
    request={"text": "Hello, world!"},
    language="en",
    sentiment=True,
    summarize=True,
    topics=True,
    intents=True
)
```

### Models V1

#### List Models

**v3+ (3.0.0 - 4.8.1)**

```python
# Not available in v3+
```

**v5.0.0**

```python
response = client.manage.v1.models.list()

# Include outdated models
response = client.manage.v1.models.list(include_outdated=True)
```

#### Get Model

**v3+ (3.0.0 - 4.8.1)**

```python
# Not available in v3+
```

**v5.0.0**

```python
response = client.manage.v1.models.get(
    model_id="6ba7b814-9dad-11d1-80b4-00c04fd430c8"
)
```

### Manage V1

#### Projects

**v3+ (3.0.0 - 4.8.1)**

```python
# Get projects
response = deepgram.manage.v("1").get_projects()

# Get project
response = deepgram.manage.v("1").get_project("550e8400-e29b-41d4-a716-446655440000")

# Update project
response = deepgram.manage.v("1").update_project("550e8400-e29b-41d4-a716-446655440000", options)

# Delete project
response = deepgram.manage.v("1").delete_project("550e8400-e29b-41d4-a716-446655440000")
```

**v5.0.0**

```python
# Get projects
response = client.manage.v1.projects.list()

# Get project
response = client.manage.v1.projects.get(project_id="550e8400-e29b-41d4-a716-446655440000")

# Update project
response = client.manage.projects.update(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    name="New Project Name"
)

# Delete project
response = client.manage.projects.delete(project_id="550e8400-e29b-41d4-a716-446655440000")
```

#### Keys

**v3+ (3.0.0 - 4.8.1)**

```python
# List keys
response = deepgram.manage.v("1").get_keys("550e8400-e29b-41d4-a716-446655440000")

# Get key
response = deepgram.manage.v("1").get_key("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")

# Create key
response = deepgram.manage.v("1").create_key("550e8400-e29b-41d4-a716-446655440000", options)

# Delete key
response = deepgram.manage.v("1").delete_key("550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8")
```

**v5.0.0**

```python
# List keys
response = client.manage.v1.projects.keys.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get key
response = client.manage.v1.projects.keys.get(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    key_id="6ba7b810-9dad-11d1-80b4-00c04fd430c8"
)

# Create key
response = client.manage.projects.keys.create(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    request={"key": "value"}
)

# Delete key
response = client.manage.projects.keys.delete(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    key_id="6ba7b810-9dad-11d1-80b4-00c04fd430c8"
)
```

#### Members

**v3+ (3.0.0 - 4.8.1)**

```python
# Get members
response = deepgram.manage.v("1").get_members("550e8400-e29b-41d4-a716-446655440000")

# Remove member
response = deepgram.manage.v("1").remove_member("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")
```

**v5.0.0**

```python
# Get members
response = client.manage.v1.projects.members.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Remove member
response = client.manage.v1.projects.members.delete(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    member_id="6ba7b811-9dad-11d1-80b4-00c04fd430c8"
)
```

#### Scopes

**v3+ (3.0.0 - 4.8.1)**

```python
# Get member scopes
response = deepgram.manage.v("1").get_member_scopes("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8")

# Update scope
response = deepgram.manage.v("1").update_member_scope("550e8400-e29b-41d4-a716-446655440000", "6ba7b811-9dad-11d1-80b4-00c04fd430c8", options)
```

**v5.0.0**

```python
# Get member scopes
response = client.manage.v1.projects.members.scopes.list(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    member_id="6ba7b811-9dad-11d1-80b4-00c04fd430c8"
)

# Update scope
response = client.manage.projects.members.scopes.update(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    member_id="6ba7b811-9dad-11d1-80b4-00c04fd430c8",
    scope="admin"
)
```

#### Invitations

**v3+ (3.0.0 - 4.8.1)**

```python
# List invites
response = deepgram.manage.v("1").get_invites("550e8400-e29b-41d4-a716-446655440000")

# Send invite
response = deepgram.manage.v("1").send_invite("550e8400-e29b-41d4-a716-446655440000", options)

# Delete invite
response = deepgram.manage.v("1").delete_invite("550e8400-e29b-41d4-a716-446655440000", "hello@deepgram.com")

# Leave project
response = deepgram.manage.v("1").leave_project("550e8400-e29b-41d4-a716-446655440000")
```

**v5.0.0**

```python
# List invites
response = client.manage.v1.projects.members.invites.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Send invite
response = client.manage.v1.projects.members.invites.create(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    email="hello@deepgram.com",
    scope="member"
)

# Delete invite
response = client.manage.v1.projects.members.invites.delete(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    email="hello@deepgram.com"
)

# Leave project
response = client.manage.v1.projects.leave(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)
```

#### Usage

**v3+ (3.0.0 - 4.8.1)**

```python
# Get all requests
response = deepgram.manage.v("1").get_usage_requests("550e8400-e29b-41d4-a716-446655440000")

# Get request
response = deepgram.manage.v("1").get_usage_request("550e8400-e29b-41d4-a716-446655440000", "6ba7b812-9dad-11d1-80b4-00c04fd430c8")

# Get fields
response = deepgram.manage.v("1").get_usage_fields("550e8400-e29b-41d4-a716-446655440000")

# Summarize usage
response = deepgram.manage.v("1").get_usage_summary("550e8400-e29b-41d4-a716-446655440000")
```

**v5.0.0**

```python
# Get all requests
response = client.manage.v1.projects.requests.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get request
response = client.manage.v1.projects.requests.get(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    request_id="6ba7b812-9dad-11d1-80b4-00c04fd430c8"
)

# Get fields
response = client.manage.v1.projects.usage.fields.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get usage summary
response = client.manage.v1.projects.usage.get(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get usage breakdown (new in v5)
response = client.manage.v1.projects.usage.breakdown.get(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)
```

#### Billing

**v3+ (3.0.0 - 4.8.1)**

```python
# Get all balances
response = deepgram.manage.v("1").get_balances("550e8400-e29b-41d4-a716-446655440000")

# Get balance
response = deepgram.manage.v("1").get_balance("550e8400-e29b-41d4-a716-446655440000", "6ba7b813-9dad-11d1-80b4-00c04fd430c8")
```

**v5.0.0**

```python
# Get all balances
response = client.manage.v1.projects.balances.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get balance
response = client.manage.v1.projects.balances.get(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    balance_id="6ba7b813-9dad-11d1-80b4-00c04fd430c8"
)
```

#### Models (Project-specific)

**v3+ (3.0.0 - 4.8.1)**

```python
# Get all project models
response = deepgram.manage.v("1").get_project_models("550e8400-e29b-41d4-a716-446655440000")

# Get model
response = deepgram.manage.v("1").get_project_model("550e8400-e29b-41d4-a716-446655440000", "6ba7b814-9dad-11d1-80b4-00c04fd430c8")
```

**v5.0.0**

```python
# Get all project models
response = client.manage.v1.projects.models.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get model
response = client.manage.v1.projects.models.get(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    model_id="6ba7b814-9dad-11d1-80b4-00c04fd430c8"
)
```

### Self-Hosted V1

#### Distribution Credentials

**v3+ (3.0.0 - 4.8.1)**

```python
# List credentials
response = deepgram.selfhosted.v("1").list_selfhosted_credentials("550e8400-e29b-41d4-a716-446655440000")

# Get credentials
response = deepgram.selfhosted.v("1").get_selfhosted_credentials("550e8400-e29b-41d4-a716-446655440000", "6ba7b815-9dad-11d1-80b4-00c04fd430c8")

# Create credentials
response = deepgram.selfhosted.v("1").create_selfhosted_credentials("550e8400-e29b-41d4-a716-446655440000", options)

# Delete credentials
response = deepgram.selfhosted.v("1").delete_selfhosted_credentials("550e8400-e29b-41d4-a716-446655440000", "6ba7b815-9dad-11d1-80b4-00c04fd430c8")
```

**v5.0.0**

```python
# List credentials
response = client.self_hosted.v1.distribution_credentials.list(
    project_id="550e8400-e29b-41d4-a716-446655440000"
)

# Get credentials
response = client.self_hosted.v1.distribution_credentials.get(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    distribution_credentials_id="6ba7b815-9dad-11d1-80b4-00c04fd430c8"
)

# Create credentials
response = client.self_hosted.v1.distribution_credentials.create(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    scopes=["read", "write"],
    provider="quay",
    comment="Development credentials"
)

# Delete credentials
response = client.self_hosted.v1.distribution_credentials.delete(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    distribution_credentials_id="6ba7b815-9dad-11d1-80b4-00c04fd430c8"
)
```

## Breaking Changes Summary

### Major Changes

1. **Authentication**: New access token support with environment variable `DEEPGRAM_TOKEN`
2. **API structure**: Flattened method names and cleaner parameter passing
3. **WebSocket API**: Complete redesign with context managers and typed message objects
4. **Type safety**: Enhanced type annotations and response objects
5. **Error handling**: Improved error types and handling

### Removed Features

- Custom configuration objects (replaced with direct parameters)
- String-based versioning (`v("1")` → `v1`)
- Separate callback methods (integrated into main methods)
- Legacy WebSocket event system

### New Features in v5.0.0

- **Listen V2**: Advanced conversational speech recognition with contextual turn detection
- **Enhanced Agent V1**: More flexible voice agent configuration
- **Raw response access**: Access to HTTP headers and raw response data
- **Custom HTTP client**: Support for custom httpx clients
- **Usage breakdown**: Detailed usage analytics
- **Better async support**: Full async/await support throughout

### Migration Checklist

- [ ] Upgrade to latest version: `pip install --upgrade deepgram-sdk`
- [ ] Update import statements if needed
- [ ] Replace API key configuration with new authentication methods
- [ ] Update all API method calls to new structure
- [ ] Migrate WebSocket connections to new context manager pattern
- [ ] Update error handling for new exception types
- [ ] Test all functionality with new API structure
