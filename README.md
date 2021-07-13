# Deepgram Python SDK

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-rounded)](CODE_OF_CONDUCT.md)

> This is a pre-release SDK and is very likely to have breaking changes. Feel free to provide
> feedback via GitHub issues and suggest new features.

Official Python SDK for [Deepgram](https://www.deepgram.com/)'s automated
speech recognition APIs.

To access the API you will need a Deepgram account. Sign up for free at
[https://console.deepgram.com/](console.deepgram.com).

You can learn more about the full Deepgram API at [https://developers.deepgram.com](https://developers.deepgram.com).

## Getting Started

```sh
pip install deepgram-sdk
```

```python
from deepgram import Deepgram

dg_client = Deepgram(YOUR_API_KEY)
# or, fully specify for an alternate endpoint
dg_client = Deepgram({
    'api_key': YOUR_API_KEY,
    'api_url': YOUR_API_URL
})
```

## Usage

Basic transcription can be done like so:

#### Batch processing

```python
from deepgram import Deepgram
import asyncio, json

DEEPGRAM_API_KEY = 'YOUR_API_KEY'
PATH_TO_FILE = 'some/file.wav'

async def main():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await dg_client.transcription.prerecorded(source)
        print(json.dumps(response, indent=4))

asyncio.run(main())
```

#### "Fake" streaming processing:

```python
from deepgram import Deepgram
import asyncio, json

DEEPGRAM_API_KEY = 'YOUR_API_KEY'
PATH_TO_FILE = 'some/file.wav'

async def main():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    # Creates a websocket connection to Deepgram
    try:
        socket = await dg_client.transcription.live()
    except Exception as e:
        print(f'Could not open socket: {e}')
        return
    # Handle sending audio to the socket
    async def process_audio(connection):
        # Open the file
        with open(PATH_TO_FILE, 'rb') as audio:
            # Chunk up the audio to send
            CHUNK_SIZE_BYTES = 8192
            CHUNK_RATE_SEC = 0.001
            chunk = audio.read(CHUNK_SIZE_BYTES)
            while chunk:
                connection.send(chunk)
                await asyncio.sleep(CHUNK_RATE_SEC)
                chunk = audio.read(CHUNK_SIZE_BYTES)
        # Indicate that we've finished sending data
        await connection.finish()

    # Listen for the connection to close
    socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
    # Print incoming transcription objects
    socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, print)

    # Send the audio to the socket
    await process_audio(socket)

asyncio.run(main())
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
