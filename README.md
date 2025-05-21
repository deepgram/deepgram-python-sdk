# Deepgram Python SDK

[![Discord](https://dcbadge.vercel.app/api/server/xWRaCDBtW4?style=flat)](https://discord.gg/xWRaCDBtW4) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepgram/deepgram-python-sdk/CI)](https://github.com/deepgram/deepgram-python-sdk/actions/workflows/CI.yml) [![PyPI](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.org/project/deepgram-sdk/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](./.github/CODE_OF_CONDUCT.md)

Official Python SDK for [Deepgram](https://www.deepgram.com/). Power your apps with world-class speech and Language AI models.

- [Transcription (Synchronous)](#transcription-synchronous)
  - [Remote Files](#remote-files)
  - [Local Files](#local-files)
- [Transcription (Asynchronous / Callbacks)](#transcription-asynchronous--callbacks)
  - [Remote Files](#remote-files-1)
  - [Local Files](#local-files-1)
- [Transcription (Live / Streaming)](#transcription-live--streaming)
  - [Live Audio](#live-audio)
- [Transcribing to Captions](#transcribing-to-captions)
- [Voice Agent](#voice-agent)
- [Text to Speech](#text-to-speech)
- [Text Intelligence](#text-intelligence)
- [Authentication](#authentication)
  - [Get Token Details](#get-token-details)
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
  - [Get All Models](#get-all-models)
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

## Transcription (Synchronous)

### Remote Files (Synchronous)

``` python
from deepgram import DeepgramClient, PrerecordedOptions

response = DeepgramClient().listen.rest.v("1").transcribe_url(
    source={"url": "https://dpgr.am/spacewalk.wav"},
    options=PrerecordedOptions(model="nova-3")
)
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/sync/url/main.py).

### Local Files

``` python
@TODO
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/file/main.py).

## Transcription (Asynchronous / Callbacks)

### Remote Files (Asynchronous)

``` python
@TODO
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

[See the Example for more info](./examples/speech-to-text/rest/async_file/main.py).

### Local Files (Asynchronous)

``` python
@TODO
```

[See our API reference for more info](https://developers.deepgram.com/reference/speech-to-text-api/listen).

## Transcription (Live / Streaming)

### Live Audio

``` python
@TODO
```

[See our API reference for more info](https://developers.deepgram.com/reference/streaming-api)

[See the Example for more info](./examples/speech-to-text/streaming/main.py)

## Transcribing to Captions

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/captions-api)

## Voice Agent

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/voice-agent-api)

[See the Example for more info](./examples/voice-agent/main.py)

## Text to Speech

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/text-to-speech-api)

[See the Example for more info](./examples/text-to-speech/main.py)

## Text Intelligence

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/text-intelligence-api)

[See the Example for more info](./examples/text-intelligence/main.py)

## Authentication

### Get Token Details

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/authentication-api)

[See the Example for more info](./examples/authentication/main.py)

## Projects

### Get Projects

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/projects-api)

### Get Project

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/projects-api)

### Update Project

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/projects-api)

### Delete Project

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/projects-api)

## Keys

### List Keys

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/keys-api)

### Get Key

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/keys-api)

### Create Key

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/keys-api)

### Delete Key

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/keys-api)

## Members

### Get Members

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/members-api)

### Remove Member

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/members-api)

## Scopes

### Get Member Scopes

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/scopes-api)

### Update Scope

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/scopes-api)

## Invitations

### List Invites

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/invites-api)

### Send Invite

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/invites-api)

### Delete Invite

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/invites-api)

### Leave Project

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/projects-api)

## Usage

### Get All Requests

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/requests-api)

### Get Request

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/requests-api)

### Summarize Usage

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/usage-api)

### Get Fields

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/usage-api)

## Billing

### Get All Balances

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/balances-api)

### Get Balance

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/balances-api)

## Models

### Get All Models

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/models-api)

### Get Model

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/models-api)

## On-Prem APIs

### List On-Prem credentials

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/on-prem-api)

### Get On-Prem credentials

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/on-prem-api)

### Create On-Prem credentials

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/on-prem-api)

### Delete On-Prem credentials

@TODO

[See our API reference for more info](https://developers.deepgram.com/reference/on-prem-api)

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
