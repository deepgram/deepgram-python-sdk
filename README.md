# Deepgram Python SDK

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepgram/deepgram-python-sdk/CI)](https://github.com/deepgram/deepgram-python-sdk/actions/workflows/CI.yml) [![PyPI](https://img.shields.io/pypi/v/deepgram-sdk)](https://pypi.org/project/deepgram-sdk/) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](./.github/CODE_OF_CONDUCT.md)

Official Python SDK for [Deepgram](https://www.deepgram.com/). Start building with our powerful transcription & speech understanding API.

> This SDK only supports hosted usage of api.deepgram.com.

## Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

## Documentation

Complete documentation of the Python SDK can be found at [Deepgram Docs](https://developers.deepgram.com/docs/python-sdk).

You can learn more about the Deepgram API at [developers.deepgram.com](https://developers.deepgram.com/docs).

## Getting Started

```sh
pip install deepgram-sdk
```

## Usage

#### Transcribe an Existing File or Pre-recorded Audio

```python
from deepgram import Deepgram
import json

DEEPGRAM_API_KEY = 'YOUR_API_KEY'
PATH_TO_FILE = 'some/file.wav'

def main():
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.sync_prerecorded(source, {'punctuate': True})
        print(json.dumps(response, indent=4))

main()
```

#### Transcribe an Existing File or Pre-recorded Audio Asynchronously

```python
from deepgram import Deepgram
import asyncio, json

DEEPGRAM_API_KEY = 'YOUR_API_KEY'
PATH_TO_FILE = 'some/file.wav'

async def main():
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
        print(json.dumps(response, indent=4))

asyncio.run(main())
```

#### Transcribe Audio in Real-Time or Streaming Audio

```python
from deepgram import Deepgram
import asyncio
import aiohttp

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'YOUR_API_KEY'

# URL for the audio you would like to stream
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'

async def main():
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Create a websocket connection to Deepgram
  # In this example, punctuation is turned on, interim results are turned off, and language is set to US English.
  try:
    deepgramLive = await deepgram.transcription.live({ 'punctuate': True, 'interim_results': False, 'language': 'en-US' })
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

# Listen for the connection to close
  deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

  # Listen for any transcripts received from Deepgram and write them to the console
  deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)

  # Listen for the connection to open and send streaming audio from the URL to Deepgram
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
      while True:
        data = await audio.content.readany()
        deepgramLive.send(data)

        # If there's no data coming from the livestream then break out of the loop
        if not data:
            break

  # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
  await deepgramLive.finish()

asyncio.run(main())
```

### Parameters

Query parameters like `punctuate` are added as part of the `TranscriptionOptions` `dict` in the `.prerecorded`/`.live` transcription call.
Multiple query parameters can be added similarly, and any dict will do - the types are provided for reference/convenience.

```python
response = await dg_client.transcription.prerecorded(source, {'punctuate': True, 'keywords': ['first:5', 'second']})
```

Depending on your preference, you can also add parameters as named arguments, instead.

```python
response = await dg_client.transcription.prerecorded(source, punctuate=True, keywords=['first:5', 'second'])
```

## Code Samples

To run the sample code, you may want to create a virtual environment to isolate your Python projects, but it's not required. You can learn how to make and activate these virtual environments in [this article](https://blog.deepgram.com/python-virtual-environments/) on our Deepgram blog.

#### Prerecorded Audio Code Samples

In the `sample-projects/prerecorded-audio` folder, there is a quickstart project to get you quickly started transcribing prerecorded audio (from a local file or a remote file) with Deepgram.

- Quickstart

#### Streaming Audio Code Samples

In the `sample-projects/streaming-audio` folder, there are examples from four different Python web frameworks of how to do live streaming audio transcription with Deepgram. These include:

- Flask 2.0
- FastAPI
- Django
- Quart

There is also a Quickstart that you can use to get up and running without a Python web framework.

- Quickstart

## Testing

### Setup

```
pip install pytest
pip install pytest-cov
```

### Run All Tests

```
pytest --api-key <key> tests/
```

### Test Coverage Report

```
pytest --cov=deepgram --api-key <key> tests/
```

### Using Example Projects to test new features

Contributors to the SDK can test their changes locally by running the projects in the `examples` folder. This can be done when making changes without adding a unit test, but of course it is recommended that you add unit tests for any feature additions made to the SDK.

Go to the folder `examples` and look for these two projects, which can be used to test out features in the Deepgram Python SDK:

- prerecorded
- streaming

These are standalone projects, so you will need to follow the instructions in the `README.md` files for each project to get it running.

## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](./.github/CODE_OF_CONDUCT.md). Then see the
[Contribution](./.github/CONTRIBUTING.md) guidelines for more information.

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue in this repository](https://github.com/deepgram/deepgram-python-sdk/issues/new)
- [Join the Deepgram Github Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)

[license]: LICENSE.txt
