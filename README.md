# Deepgram Python SDK

[![Discord](https://dcbadge.vercel.app/api/server/xWRaCDBtW4?style=flat)](https://discord.gg/xWRaCDBtW4) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepgram/deepgram-python-sdk/CI)](https://github.com/deepgram/deepgram-python-sdk/actions/workflows/CI.yml) [![PyPI](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.org/project/deepgram-sdk/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](./.github/CODE_OF_CONDUCT.md)

Official Python SDK for [Deepgram](https://www.deepgram.com/). Power your apps with world-class speech and Language AI models.

- [Deepgram Python SDK](#deepgram-python-sdk)
- [Documentation](#documentation)
- [Getting an API Key](#getting-an-api-key)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstarts](#quickstarts)
  - [PreRecorded Audio Transcription Quickstart](#prerecorded-audio-transcription-quickstart)
  - [Live Audio Transcription Quickstart](#live-audio-transcription-quickstart)
- [Examples](#examples)
- [Development and Contributing](#development-and-contributing)
- [Getting Help](#getting-help)

# Documentation

You can learn more about the Deepgram API at [developers.deepgram.com](https://developers.deepgram.com/docs).

# Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

# Requirements

[Python](https://www.python.org/downloads/) (version ^3.10)

# Installation

To install the latest version available (which will guarantee change over time):

```sh
pip install deepgram-sdk
```

If you are going to write an application to consume this SDK, it's [highly recommended](https://discuss.python.org/t/how-to-pin-a-package-to-a-specific-major-version-or-lower/17077) and a [programming staple](https://www.easypost.com/dependency-pinning-guide) to pin to at **least** a major version of an SDK (ie `==2.*`) or **with due diligence**, to a minor and/or specific version (ie `==2.1.*` or `==2.12.0`, respectively). If you are unfamiliar with [semantic versioning or semver](https://semver.org/), it's a must-read.

In a `requirements.txt` file, pinning to a major (or minor) version, like if you want to stick to using the SDK `v2.12.0` release, that can be done like this:

```
deepgram-sdk==2.*
```

Or using pip:

```sh
pip install deepgram-sdk==2.*
```

Pinning to a specific version can be done like this in a `requirements.txt` file:

```
deepgram-sdk==2.12.0
```

Or using pip:

```sh
pip install deepgram-sdk==2.12.0
```

We guarantee that major interfaces will not break in a given major semver (ie `2.*` release). However, all bets are off moving from a `2.*` to `3.*` major release. This follows standard semver best-practices.

# Quickstarts

This SDK aims to reduce complexity and abtract/hide some internal Deepgram details that clients shouldn't need to know about.  However you can still tweak options and settings if you need.

## PreRecorded Audio Transcription Quickstart

You can find a [walkthrough](https://developers.deepgram.com/docs/pre-recorded-audio-transcription) on our documentation site. Transcribing Pre-Recorded Audio can be done using the following sample code:

```python
AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}

# STEP 1 Create a Deepgram client using the API key from environment variables
deepgram = DeepgramClient()

# STEP 2 Call the transcribe_url method on the prerecorded class
options = PrerecordedOptions(
    model="nova",
    smart_format=True,
    summarize="v2",
)
url_response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
print(url_response)
```

## Live Audio Transcription Quickstart

You can find a [walkthrough](https://developers.deepgram.com/docs/live-streaming-audio-transcription) on our documentation site. Transcribing Live Audio can be done using the following sample code:

```python
deepgram = DeepgramClient()

# Create a websocket connection to Deepgram
options = LiveOptions(
    punctuate=True,
    language="en-US",
    encoding="linear16",
    channels=1,
    sample_rate=16000,
)

def on_message(result=None):
    if result is None:
        return
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    print(f"speaker: {sentence}")

def on_metadata(metadata=None):
    if metadata is None:
        return
    print(f"\n{metadata}\n")


def on_error(error=None):
    if error is None:
        return
    print(f"\n{error}\n")

dg_connection = deepgram.listen.live.v("1")
dg_connection.start(options)

dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
dg_connection.on(LiveTranscriptionEvents.Error, on_error)

# create microphone
microphone = Microphone(dg_connection.send)

# start microphone
microphone.start()

# wait until finished
input("Press Enter to stop recording...\n\n")

# Wait for the microphone to close
microphone.finish()

# Indicate that we've finished
dg_connection.finish()

print("Finished")
```

# Examples

There are examples for **every** API call in this SDK. You can find all of these examples in the [examples folder](https://github.com/deepgram/deepgram-python-sdk/tree/main/examples) at the root of this repo.

These examples provide:

- PreRecorded Audio Transcription:

    - From an Audio File - [examples/prerecorded/file](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/prerecorded/file/main.py)
    - From an URL - [examples/prerecorded/url](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/prerecorded/url/main.py)

- Live Audio Transcription:

    - From a Microphone - [examples/streaming/microphone](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/streaming/microphone/main.py)
    - From an HTTP Endpoint - [examples/streaming/http](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/streaming/http/main.py)

- Management API exercise the full [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations for:

    - Balances - [examples/manage/balances](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/balances/main.py)
    - Invitations - [examples/manage/invitations](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/invitations/main.py)
    - Keys - [examples/manage/keys](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/keys/main.py)
    - Members - [examples/manage/members](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/members/main.py)
    - Projects - [examples/manage/projects](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/projects/main.py)
    - Scopes - [examples/manage/scopes](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/scopes/main.py)
    - Usage - [examples/manage/usage](https://github.com/deepgram/deepgram-python-sdk/blob/main/examples/manage/usage/main.py)

To run each example set the `DEEPGRAM_API_KEY` as an environment variable, then `cd` into each example folder and execute the example: `go run main.py`.

# Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](https://github.com/deepgram/deepgram-python-sdk/blob/main/.github/CODE_OF_CONDUCT.md). Then see the
[Contribution](https://github.com/deepgram/deepgram-python-sdk/blob/main/.github/CONTRIBUTING.md) guidelines for more information.

## Prerequisites

In order to develop new features for the SDK itself, you first need to uninstall any previous installation of the `deepgram-sdk` and then install/pip the dependencies contained in the `requirements.txt` then instruct python (via pip) to use the SDK by installing it locally.

From the root of the repo, that would entail:

```bash
pip uninstall deepgram-sdk
pip install -r requirements.txt
pip install -e .
```

## Testing

If you are looking to contribute or modify pytest code, then you need to install the following dependencies:

```bash
pip install -r requirements-dev.txt
```

# Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue in this repository](https://github.com/deepgram/deepgram-python-sdk/issues/new)
- [Join the Deepgram Github Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)
