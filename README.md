# Deepgram Python SDK

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](CODE_OF_CONDUCT.md)

> This SDK is under active development; feel free to provide
> feedback via GitHub issues and suggest new features.

Official Python SDK for [Deepgram](https://www.deepgram.com/)'s automated
speech recognition APIs.

To access the API you will need a Deepgram account. Sign up for free at
[console.deepgram.com](https://console.deepgram.com/signup?utm_medium=github&utm_source=DEVREL&utm_content=python-sdk).

You can learn more about the full Deepgram API at [developers.deepgram.com](https://developers.deepgram.com).

## Getting Started

```sh
pip install deepgram-sdk
```

## Usage

#### Transcribe an Existing File

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
        response = deepgram.transcription_.prerecorded(source, {'punctuate': True})
        print(json.dumps(response, indent=4))

main()
```

#### Transcribe an Existing File Asynchronously

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

#### Transcribe Audio in Real-Time

```python
from deepgram import Deepgram
import asyncio
import aiohttp

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'YOUR_API_KEY'

# URL for the audio you would like to stream
# URL for the example resource will change depending on whether user is outside or inside the UK
# Outside the UK
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourlw_online_nonuk'
# Inside the UK
# URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm'

async def main():
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Create a websocket connection to Deepgram
  # In this example, punctuation is turned on, interim results are turned off, and language is set to UK English.
  try:
    deepgramLive = await deepgram.transcription.live({ 'punctuate': True, 'interim_results': False, 'language': 'en-GB' })
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

## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](./CODE_OF_CONDUCT.md). Then see the
[Contribution](./CONTRIBUTING.md) guidelines for more information.

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue](https://github.com/deepgram/python-sdk/issues/new) on this repository
- Tweet at us! We're [@DeepgramDevs on Twitter](https://twitter.com/DeepgramDevs)

## Further Reading

Check out the Developer Documentation at [https://developers.deepgram.com/](https://developers.deepgram.com/)
