# Deepgram API Python Library

![](https://developers.deepgram.com)

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fdeepgram%2Fdeepgram-python-sdk)
[![pypi](https://img.shields.io/pypi/v/deepgram)](https://pypi.python.org/pypi/deepgram)

Power your apps with world-class speech and Language AI models

## Documentation

API reference documentation is available [here](https://developers.deepgram.com/reference/deepgram-api-overview).

## Migrating from earlier versions

### V2 to V3

We have published [a migration guide on our docs](https://developers.deepgram.com/sdks/python-sdk/v2-to-v3-migration), showing how to move from v2 to v3.

### V3.\* to V4

The Voice Agent interfaces have been updated to use the new Voice Agent V1 API. Please refer to our [Documentation](https://developers.deepgram.com/docs/voice-agent-v1-migration) on Migration to new V1 Agent API.

## Requirements

[Python](https://www.python.org/downloads/) (version ^3.10)

## Installation

```sh
pip install deepgram
```

## Initialization

All of the examples below will require `DeepgramClient`.

```python
from deepgram import DeepgramClient

# Initialize the client
deepgram = DeepgramClient("YOUR_API_KEY")  # Replace with your API key
```

### Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

## Pre-Recorded (Synchronous)

### Remote Files (Synchronous)

Transcribe audio from a URL.

```python
from deepgram import PrerecordedOptions, UrlSource

payload: UrlSource = {
    "url": "https://dpgr.am/spacewalk.wav"
}

options = PrerecordedOptions(model="nova-3") # Apply other options

response = deepgram.listen.rest.v("1").transcribe_url(
    payload,
    options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

### Local Files (Synchronous)

Transcribe audio from a file.

```python
from deepgram import PrerecordedOptions, FileSource

with open("path/to/your/audio.wav", "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(model="nova-3") # Apply other options

response = deepgram.listen.rest.v("1").transcribe_file(
    payload,
    options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

## Pre-Recorded (Asynchronous / Callbacks)

### Remote Files (Asynchronous)

Transcribe audio from a URL.

```python
from deepgram import PrerecordedOptions, UrlSource

payload: UrlSource = {
    "url": "https://dpgr.am/spacewalk.wav"
}

options = PrerecordedOptions(model="nova-3") # Apply other options

response = deepgram.listen.rest.v("1").transcribe_url_callback(
    payload,
    "https://your-callback-url.com/webhook",
    options=options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

### Local Files (Asynchronous)

Transcribe audio from a file.

```python
from deepgram import PrerecordedOptions, FileSource

with open("path/to/your/audio.wav", "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(model="nova-3") # Apply other options

response = deepgram.listen.rest.v("1").transcribe_file_callback(
    payload,
    "https://your-callback-url.com/webhook",
    options=options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

## Streaming Audio

Transcribe streaming audio.

```python
from deepgram import LiveOptions, LiveTranscriptionEvents

# Create a websocket connection
connection = deepgram.listen.websocket.v("1")

# Handle transcription events
@connection.on(LiveTranscriptionEvents.Transcript)
def handle_transcript(result):
    print(result.channel.alternatives[0].transcript)

# Start connection with streaming options
connection.start(LiveOptions(model="nova-3", language="en-US"))

# Send audio data
connection.send(open("path/to/your/audio.wav", "rb").read())

# Close when done
connection.finish()
```

[See our API reference for more info](https://developers.deepgram.com/reference/streaming-api).

## Transcribing to Captions

Transcribe audio to captions.

### WebVTT

```python
from deepgram_captions import DeepgramConverter, webvtt

transcription = DeepgramConverter(dg_response)
captions = webvtt(transcription)
```

### SRT

```python
from deepgram_captions import DeepgramConverter, srt

transcription = DeepgramConverter(dg_response)
captions = srt(transcription)
```

[See our stand alone captions library for more information.](https://github.com/deepgram/deepgram-python-captions).

## Voice Agent

Configure a Voice Agent.

```python
from deepgram import (
    SettingsOptions,
    Speak
)

# Create websocket connection
connection = deepgram.agent.websocket.v("1")

# Configure agent settings
options = SettingsOptions()
options.language = "en"
options.agent.think.provider.type = "open_ai"
options.agent.think.provider.model = "gpt-4o-mini"
options.agent.think.prompt = "You are a helpful AI assistant."
options.agent.listen.provider.type = "deepgram"
options.agent.listen.provider.model = "nova-3"

# Configure multiple TTS providers for automatic fallback.
primary = Speak()
primary.provider.type = "deepgram"
primary.provider.model = "aura-2-zeus-en"

fallback = Speak()
fallback.provider.type = "cartesia"
fallback.provider.model = "sonic-english"

options.agent.speak = [primary, fallback]
# Set Agent greeting
options.greeting = "Hello, I'm your AI assistant."

# Start the connection
connection.start(options)

# Close the connection
connection.finish()
```

This example demonstrates:

- Setting up a WebSocket connection
- Configuring the agent with speech, language, and audio settings
- Handling various agent events (speech, transcripts, audio)
- Sending audio data and keeping the connection alive

For a complete implementation, you would need to:

1. Add your audio input source (e.g., microphone)
2. Implement audio playback for the agent's responses
3. Handle any function calls if your agent uses them
4. Add proper error handling and connection management

[See our API reference for more info](https://developers.deepgram.com/reference/voice-agent-api/agent).

## Text to Speech REST

Convert text into speech using the REST API.

```python
from deepgram import SpeakOptions

# Configure speech options
options = SpeakOptions(model="aura-2-thalia-en")

# Convert text to speech and save to file
response = deepgram.speak.rest.v("1").save(
    "output.mp3",
    {"text": "Hello world!"},
    options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/text-to-speech-api/speak).

## Text to Speech Streaming

Convert streaming text into speech using a Websocket.

```python
from deepgram import (
    SpeakWSOptions,
    SpeakWebSocketEvents
)

# Create websocket connection
connection = deepgram.speak.websocket.v("1")

# Handle audio data
@connection.on(SpeakWebSocketEvents.AudioData)

# Configure streaming options
options = SpeakWSOptions(
    model="aura-2-thalia-en",
    encoding="linear16",
    sample_rate=16000
)

# Start connection and send text
connection.start(options)
connection.send_text("Hello, this is a text to speech example.")
connection.flush()
connection.wait_for_complete()

# Close when done
connection.finish()
```

[See our API reference for more info](https://developers.deepgram.com/reference/text-to-speech-api/speak).

## Text Intelligence

Analyze text.

```python
from deepgram import AnalyzeOptions, TextSource

# Configure analyze options
options = AnalyzeOptions(
    sentiment=True,
    intents=True,
    topics=True,
    summarize=True
)

# Create text source
payload: TextSource = {
    "buffer": "The quick brown fox jumps over the lazy dog."
}

# Process text for intelligence
response = deepgram.read.analyze.v("1").analyze_text(
    payload,
    options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/text-intelligence-api/text-read).

## Authentication

The Deepgram Python SDK supports multiple authentication methods to provide flexibility and enhanced security for your applications.

### Authentication Methods

#### API Key Authentication (Traditional)

The traditional method using your Deepgram API key:

```python
from deepgram import DeepgramClient

# Direct API key
client = DeepgramClient(api_key="YOUR_API_KEY")

# Or using environment variable DEEPGRAM_API_KEY
client = DeepgramClient()  # Auto-detects from environment
```

#### Bearer Token Authentication (OAuth 2.0)

Use short-lived access tokens for enhanced security:

```python
from deepgram import DeepgramClient

# Direct access token
client = DeepgramClient(access_token="YOUR_ACCESS_TOKEN")

# Or using environment variable DEEPGRAM_ACCESS_TOKEN
client = DeepgramClient()  # Auto-detects from environment
```

### Authentication Priority

When multiple credentials are provided, the SDK follows this priority order:

1. **Explicit `access_token` parameter** (highest priority)
2. **Explicit `api_key` parameter**
3. **`DEEPGRAM_ACCESS_TOKEN` environment variable**
4. **`DEEPGRAM_API_KEY` environment variable** (lowest priority)

### Environment Variables

Set your credentials using environment variables:

```bash
# For API key authentication
export DEEPGRAM_API_KEY="your-deepgram-api-key"

# For bearer token authentication
export DEEPGRAM_ACCESS_TOKEN="your-access-token"
```

### Dynamic Authentication Switching

Switch between authentication methods at runtime:

```python
from deepgram import DeepgramClient, DeepgramClientOptions

# Start with API key
config = DeepgramClientOptions(api_key="your-api-key")
client = DeepgramClient(config=config)

# Switch to access token
client._config.set_access_token("your-access-token")

# Switch back to API key
client._config.set_apikey("your-api-key")
```

### Complete Bearer Token Workflow

Here's a practical example of using API keys to obtain access tokens:

```python
from deepgram import DeepgramClient

# Step 1: Create client with API key
api_client = DeepgramClient(api_key="your-api-key")

# Step 2: Get a short-lived access token (30-second TTL)
response = api_client.auth.v("1").grant_token()
access_token = response.access_token

# Step 3: Create new client with Bearer token
bearer_client = DeepgramClient(access_token=access_token)

# Step 4: Use the Bearer client for API calls
transcription = bearer_client.listen.rest.v("1").transcribe_url(
    {"url": "https://dpgr.am/spacewalk.wav"}
)
```

### Benefits of Bearer Token Authentication

- **Enhanced Security**: Short-lived tokens (30-second expiration) minimize risk
- **OAuth 2.0 Compliance**: Standard bearer token format
- **Scope Limitation**: Tokens can be scoped to specific permissions
- **Audit Trail**: Better tracking of token usage vs API keys

### Authentication Management

#### Get Token Details

Retrieves the details of the current authentication token:

```python
response = deepgram.manage.rest.v("1").get_token_details()
```

#### Grant Token

Creates a temporary token with a 30-second TTL:

```python
response = deepgram.auth.v("1").grant_token()
```

[See our API reference for more info](https://developers.deepgram.com/reference/token-based-auth-api/grant-token).

## Projects

### Get Projects

Returns all projects accessible by the API key.

```python
response = deepgram.manage.v("1").get_projects()
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/list).

### Get Project

Retrieves a specific project based on the provided project_id.

```python
response = deepgram.manage.v("1").get_project(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/get).

### Update Project

Update a project.

```python
response = deepgram.manage.v("1").update_project(myProjectId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/update).

### Delete Project

Delete a project.

```python
response = deepgram.manage.v("1").delete_project(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/delete).

## Keys

### List Keys

Retrieves all keys associated with the provided project_id.

```python
response = deepgram.manage.v("1").get_keys(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/list)

### Get Key

Retrieves a specific key associated with the provided project_id.

```python
response = deepgram.manage.v("1").get_key(myProjectId, myKeyId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/get)

### Create Key

Creates an API key with the provided scopes.

```python
 response = deepgram.manage.v("1").create_key(myProjectId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/create)

### Delete Key

Deletes a specific key associated with the provided project_id.

```python
response = deepgram.manage.v("1").delete_key(myProjectId, myKeyId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/delete)

## Members

### Get Members

Retrieves account objects for all of the accounts in the specified project_id.

```python
response = deepgram.manage.v("1").get_members(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/members/list).

### Remove Member

Removes member account for specified member_id.

```python
response = deepgram.manage.v("1").remove_member(myProjectId, MemberId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/members/delete).

## Scopes

### Get Member Scopes

Retrieves scopes of the specified member in the specified project.

```python
response = deepgram.manage.v("1").get_member_scopes(myProjectId, memberId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/scopes/list).

### Update Scope

Updates the scope for the specified member in the specified project.

```python
response = deepgram.manage.v("1").update_member_scope(myProjectId, memberId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/scopes/update).

## Invitations

### List Invites

Retrieves all invitations associated with the provided project_id.

```python
response = deepgram.manage.v("1").get_invites(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/invitations/list).

### Send Invite

Sends an invitation to the provided email address.

```python
response = deepgram.manage.v("1").send_invite(myProjectId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/invitations/create).

### Delete Invite

Removes the specified invitation from the project.

```python
response = deepgram.manage.v("1").delete_invite(myProjectId, email)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/invitations/delete).

### Leave Project

```python
response = deepgram.manage.v("1").leave_project(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/invitations/leave).

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

## Billing

### Get All Balances

Retrieves the list of balance info for the specified project.

```python
response = deepgram.manage.v("1").get_balances(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/balances/list).

### Get Balance

Retrieves the balance info for the specified project and balance_id.

```python
response = deepgram.manage.v("1").get_balance(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/balances/get).

## Models

### Get All Project Models

Retrieves all models available for a given project.

```python
response = deepgram.manage.v("1").get_project_models(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/list-models).

### Get Model

Retrieves details of a specific model.

```python
response = deepgram.manage.v("1").get_project_model(myProjectId, ModelId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/get-model).

## On-Prem APIs

### List On-Prem credentials

Lists sets of distribution credentials for the specified project.

```python
response = deepgram.selfhosted.v("1").list_selfhosted_credentials(projectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/list-credentials).

### Get On-Prem credentials

Returns a set of distribution credentials for the specified project.

```python
response = deepgram.selfhosted.v("1").get_selfhosted_credentials(projectId, distributionCredentialsId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/get-credentials).

### Create On-Prem credentials

Creates a set of distribution credentials for the specified project.

```python
response = deepgram.selfhosted.v("1").create_selfhosted_credentials(project_id, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/create-credentials).

### Delete On-Prem credentials

Deletes a set of distribution credentials for the specified project.

```python
response = deepgram.selfhosted.v("1").delete_selfhosted_credentials(projectId, distributionCredentialId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/delete-credentials).

## Pinning Versions

To ensure your application remains stable and reliable, we recommend using version pinning in your project. This is a best practice in Python development that helps prevent unexpected changes. You can pin to a major version (like `==4.*`) for a good balance of stability and updates, or to a specific version (like `==4.1.0`) for maximum stability. We've included some helpful resources about [version pinning](https://discuss.python.org/t/how-to-pin-a-package-to-a-specific-major-version-or-lower/17077) and [dependency management](https://www.easypost.com/dependency-pinning-guide) if you'd like to learn more. For a deeper understanding of how version numbers work, check out[semantic versioning](https://semver.org/).

In a `requirements.txt` file, you can pin to a specific version like this:

```sh
deepgram-sdk==4.1.0
```

Or using pip:

```sh
pip install deepgram-sdk==4.1.0
```

## Logging

This SDK provides logging as a means to troubleshoot and debug issues encountered. By default, this SDK will enable `Information` level messages and higher (ie `Warning`, `Error`, etc) when you initialize the library as follows:

```python
deepgram: DeepgramClient = DeepgramClient()
```

To increase the logging output/verbosity for debug or troubleshooting purposes, you can set the `DEBUG` level but using this code:

```python
config: DeepgramClientOptions = DeepgramClientOptions(
    verbose=logging.DEBUG,
)
deepgram: DeepgramClient = DeepgramClient("", config)
```

## Testing

### Daily and Unit Tests

If you are looking to use, run, contribute or modify to the daily/unit tests, then you need to install the following dependencies:

```bash
pip install -r requirements-dev.txt
```

### Daily Tests

The daily tests invoke a series of checks against the actual/real API endpoint and save the results in the `tests/response_data` folder. This response data is updated nightly to reflect the latest response from the server. Running the daily tests does require a `DEEPGRAM_API_KEY` set in your environment variables.

To run the Daily Tests:

```bash
make daily-test
```

#### Unit Tests

The unit tests invoke a series of checks against mock endpoints using the responses saved in `tests/response_data` from the daily tests. These tests are meant to simulate running against the endpoint without actually reaching out to the endpoint; running the unit tests does require a `DEEPGRAM_API_KEY` set in your environment variables, but you will not actually reach out to the server.

```bash
make unit-test
```

## Backwards Compatibility

We follow semantic versioning (semver) to ensure a smooth upgrade experience. Within a major version (like `4.*`), we will maintain backward compatibility so your code will continue to work without breaking changes. When we release a new major version (like moving from `3.*` to `4.*`), we may introduce breaking changes to improve the SDK. We'll always document these changes clearly in our release notes to help you upgrade smoothly.

Older SDK versions will receive Priority 1 (P1) bug support only. Security issues, both in our code and dependencies, are promptly addressed. Significant bugs without clear workarounds are also given priority attention.

## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](CODE_OF_CONDUCT.md). Then see the
[Contribution](CONTRIBUTING.md) guidelines for more information.

In order to develop new features for the SDK itself, you first need to uninstall any previous installation of the `deepgram-sdk` and then install/pip the dependencies contained in the `requirements.txt` then instruct python (via pip) to use the SDK by installing it locally.

From the root of the repo, that would entail:

```bash
pip uninstall deepgram-sdk
pip install -r requirements.txt
pip install -e .
```

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue in this repository](https://github.com/deepgram/deepgram-python-sdk/issues/new)
- [Join the Deepgram Github Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

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
        proxies="http://my.test.proxy.example.com",
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
