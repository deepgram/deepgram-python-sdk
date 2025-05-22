# Deepgram Python SDK

[![Discord](https://dcbadge.vercel.app/api/server/xWRaCDBtW4?style=flat)](https://discord.gg/xWRaCDBtW4) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepgram/deepgram-python-sdk/CI)](https://github.com/deepgram/deepgram-python-sdk/actions/workflows/CI.yml) [![PyPI](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.org/project/deepgram-sdk/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](./.github/CODE_OF_CONDUCT.md)

Official Python SDK for [Deepgram](https://www.deepgram.com/). Power your apps with world-class speech and Language AI models.

- [Pre-Recorded (Synchronous)](#pre-recorded-synchronous)
  - [Remote Files (Synchronous)](#remote-files-synchronous)
  - [Local Files (Synchronous)](#local-files-synchronous)
- [Pre-Recorded (Asynchronous / Callbacks)](#pre-recorded-asynchronous--callbacks)
  - [Remote Files (Asynchronous)](#remote-files-asynchronous)
  - [Local Files (Asynchronous)](#local-files-asynchronous)
- [Streaming Audio](#streaming-audio)
- [Transcribing to Captions](#transcribing-to-captions)
- [Voice Agent](#voice-agent)
- [Text to Speech REST](#text-to-speech-rest)
- [Text to Speech Streaming](#text-to-speech-streaming)
- [Text Intelligence](#text-intelligence)
- [Authentication](#authentication)
  - [Get Token Details](#get-token-details)
  - [Grant Token](#grant-token)
- [Projects](#projects)
  - [Get Projects](#get-projects)
  - [Get Project](#get-project)
  - [Update Project](#update-project)
  - [Delete Project](#delete-project)
- [Keys](#keys)
  - [List Keys](#list-keys)
  - [Get Key](#get-key)
  - [Create Key](#create-key)
  - [Delete Key](#delete-key)
- [Members](#members)
  - [Get Members](#get-members)
  - [Remove Member](#remove-member)
- [Scopes](#scopes)
  - [Get Member Scopes](#get-member-scopes)
  - [Update Scope](#update-scope)
- [Invitations](#invitations)
  - [List Invites](#list-invites)
  - [Send Invite](#send-invite)
  - [Delete Invite](#delete-invite)
  - [Leave Project](#leave-project)
- [Usage](#usage)
  - [Get All Requests](#get-all-requests)
  - [Get Request](#get-request)
  - [Summarize Usage](#summarize-usage)
  - [Get Fields](#get-fields)
- [Billing](#billing)
  - [Get All Balances](#get-all-balances)
  - [Get Balance](#get-balance)
- [Models](#models)
  - [Get All Project Models](#get-all-project-models)
  - [Get Model](#get-model)
- [On-Prem APIs](#on-prem-apis)
  - [List On-Prem credentials](#list-on-prem-credentials)
  - [Get On-Prem credentials](#get-on-prem-credentials)
  - [Create On-Prem credentials](#create-on-prem-credentials)
  - [Delete On-Prem credentials](#delete-on-prem-credentials)
- [Logging](#logging)
- [Backwards Compatibility](#backwards-compatibility)
- [Development and Contributing](#development-and-contributing)
- [Getting Help](#getting-help)

## Documentation

You can learn more about the Deepgram API at [developers.deepgram.com](https://developers.deepgram.com/docs).

## Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

## Requirements

[Python](https://www.python.org/downloads/) (version ^3.10)

## Installation

To install the latest version available:

```sh
pip install deepgram-sdk
```

## Initialization

All the examples below will require `DeepgramClient`.

```python
from deepgram import DeepgramClient

# Initialize the client
deepgram = DeepgramClient("YOUR_API_KEY")  # Replace with your API key
```

## Pre-Recorded (Synchronous)

### Remote Files (Synchronous)

Transcribe audio from a URL.

```python

from deepgram import PrerecordedOptions

response = deepgram.listen.rest.v("1").transcribe_url(
    source={"url": "https://dpgr.am/spacewalk.wav"},
    options=PrerecordedOptions(model="nova-3") # Apply other options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/sync/url/main.py).

### Local Files (Synchronous)

Transcribe audio from a file.

```python
from deepgram import PrerecordedOptions

response = deepgram.listen.rest.v("1").transcribe_file(
    source=open("path/to/your/audio.wav", "rb"),
    options=PrerecordedOptions(model="nova-3") # Apply other options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/sync/file/main.py).

## Pre-Recorded (Asynchronous / Callbacks)

### Remote Files (Asynchronous)

Transcribe audio from a URL.

```python
from deepgram import PrerecordedOptions

response = deepgram.listen.rest.v("1").transcribe_url_async(
    source={"url": "https://dpgr.am/spacewalk.wav"},
    callback_url="https://your-callback-url.com/webhook",
    options=PrerecordedOptions(model="nova-3") # Apply other options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/async/url/main.py).

### Local Files (Asynchronous)

Transcribe audio from a file.

```python
from deepgram import PrerecordedOptions

response = deepgram.listen.rest.v("1").transcribe_file_async(
    source=open("path/to/your/audio.wav", "rb"),
    callback_url="https://your-callback-url.com/webhook",
    options=PrerecordedOptions(model="nova-3") # Apply other options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/async/file/main.py).

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

[See the Examples for more info](./examples/speech-to-text/websocket/).

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
    SettingsOptions
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
options.agent.speak.provider.type = "deepgram"
options.agent.speak.provider.model ="aura-2-thalia-en"

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

[See the Examples for more info](./examples/agent/).

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

[See the Example for more info](./examples/text-to-speech/rest/).

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

[See the Examples for more info](./examples/text-to-speech/websocket/).

## Text Intelligence

Analyze text.

```python
from deepgram import ReadOptions

# Configure read options
options = ReadOptions(
    model="nova-3",
    language="en"
)

# Process text for intelligence
response = deepgram.read.rest.v("1").process(
    text="The quick brown fox jumps over the lazy dog.",
    options=options
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/text-intelligence-api/text-read).

## Authentication

### Get Token Details

Retrieves the details of the current authentication token.

```python
response = deepgram.manage.rest.v("1").get_token_details()
```

[See our API reference for more info](https://developers.deepgram.com/reference/authentication).

### Grant Token

Creates a temporary token with a 30-second TTL.

```python
response = deepgram.auth.v("1").grant_token()

```

[See our API reference for more info](https://developers.deepgram.com/reference/token-based-auth-api/grant-token).

[See The Examples for more info](./examples/auth/)

## Projects

### Get Projects

Returns all projects accessible by the API key.

```python
response = deepgram.manage.v("1").get_projects()
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/list).

[See The Example for more info](./examples/manage/projects/main.py).

### Get Project

Retrieves a specific project based on the provided project_id.

```python
response = deepgram.manage.v("1").get_project(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/get).

[See The Example for more info](./examples/manage/projects/main.py).

### Update Project

Update a project.

```python
response = deepgram.manage.v("1").update_project(myProjectId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/update).

[See The Example for more info](./examples/manage/projects/main.py).

### Delete Project

Delete a project.

```python
response = deepgram.manage.v("1").delete_project(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/projects/delete).

[See The Example for more info](./examples/manage/projects/main.py).

## Keys

### List Keys

Retrieves all keys associated with the provided project_id.

```python
response = deepgram.manage.v("1").get_keys(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/list)

[See The Example for more info](./examples/manage/keys/main.py).

### Get Key

Retrieves a specific key associated with the provided project_id.

```python
response = deepgram.manage.v("1").get_key(myProjectId, myKeyId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/get)

[See The Example for more info](./examples/manage/keys/main.py).

### Create Key

Creates an API key with the provided scopes.

```python
 response = deepgram.manage.v("1").create_key(myProjectId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/create)

[See The Example for more info](./examples/manage/keys/main.py).

### Delete Key

Deletes a specific key associated with the provided project_id.

```python
response = deepgram.manage.v("1").delete_key(myProjectId, myKeyId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/keys/delete)

[See The Example for more info](./examples/manage/keys/main.py).

## Members

### Get Members

Retrieves account objects for all of the accounts in the specified project_id.

```python
response = deepgram.manage.v("1").get_members(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/members/list).

[See The Example for more info](./examples/manage/members/main.py).

### Remove Member

Removes member account for specified member_id.

```python
response = deepgram.manage.v("1").remove_member(myProjectId, MemberId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/members/delete).

[See The Example for more info](./examples/manage/members/main.py).

## Scopes

### Get Member Scopes

Retrieves scopes of the specified member in the specified project.

```python
response = deepgram.manage.v("1").get_member_scopes(myProjectId, memberId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/scopes/list).

[See The Example for more info](./examples/manage/scopes/main.py).

### Update Scope

Updates the scope for the specified member in the specified project.

```python
response = deepgram.manage.v("1").update_member_scope(myProjectId, memberId, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/scopes/update).

[See The Example for more info](./examples/manage/scopes/main.py).

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

## Usage

### Get All Requests

Retrieves all requests associated with the provided project_id based on the provided options.

```python
response = deepgram.manage.v("1").get_usage_requests(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/usage/list-requests).

### Get Request

Retrieves a specific request associated with the provided project_id

```python
response = deepgram.manage.v("1").get_usage_request(myProjectId, RequestId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/usage/get-request).

### Get Fields

Lists the features, models, tags, languages, and processing method used for requests in the specified project.

```python
response = deepgram.manage.v("1").get_usage_fields(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/usage/list-fields).

### Summarize Usage

`Deprecated` Retrieves the usage for a specific project. Use Get Project Usage Breakdown for a more comprehensive usage summary.

```python
response = deepgram.manage.v("1").get_usage_summary(myProjectId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/management-api/usage/get).

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

```python
response = deepgram.selfhosted.v("1").get_selfhosted_credentials(projectId, distributionCredentialsId)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/get-credentials).

### Create On-Prem credentials

```python
response = deepgram.selfhosted.v("1").create_selfhosted_credentials(project_id, options)
```

[See our API reference for more info](https://developers.deepgram.com/reference/self-hosted-api/create-credentials).

### Delete On-Prem credentials

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
