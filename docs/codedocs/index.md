---
title: "Getting Started"
description: "Start using the Deepgram Python SDK for speech, text, and agent workflows."
---

The Deepgram Python SDK is the official Python client for Deepgram speech-to-text, text-to-speech, text analysis, management, and voice agent APIs.

## The Problem

- Speech applications usually need separate code paths for batch transcription, live streaming, synthesis, and admin APIs.
- Realtime voice workflows are hard to wire correctly because WebSocket setup, event handling, and message formats differ by endpoint.
- Authentication changes between server-side API keys, temporary access tokens, and custom transport requirements can leak into application code.
- Advanced options such as diarization, summaries, request tags, usage filters, and agent settings are easy to miss when you stay at raw HTTP level.

## The Solution

The SDK wraps Deepgram's API surface behind one root client, exposes sync and async variants, lazily loads domain clients such as `listen`, `speak`, `read`, `manage`, and `agent`, and turns streaming connections into typed socket clients with event callbacks. The hand-written `src/deepgram/client.py` layer adds `access_token`, `session_id`, and `transport_factory` support on top of the generated REST and WebSocket clients.

```python
from deepgram import DeepgramClient

client = DeepgramClient()

with open("audio.wav", "rb") as audio_file:
    response = client.listen.v1.media.transcribe_file(
        request=audio_file.read(),
        model="nova-3",
        smart_format=True,
        diarize=True,
    )

print(response.results.channels[0].alternatives[0].transcript)
```

<Callout type="info">This is a Python SDK, so the install commands below use Python package managers instead of JavaScript package managers.</Callout>

## Installation

" "pipx"]}>
<Tab value="pip">

```bash
pip install deepgram-sdk
```

</Tab>
<Tab value="uv">

```bash
uv add deepgram-sdk
```

</Tab>
<Tab value="poetry">

```bash
poetry add deepgram-sdk
```

</Tab>
<Tab value="pipx">

```bash
pipx install deepgram-sdk
```

</Tab>
</Tabs>

If you want the optional `aiohttp`-backed async transport, install the extra:

```bash
pip install "deepgram-sdk[aiohttp]"
```

## Quick Start

Set `DEEPGRAM_API_KEY` in your environment, then run the smallest useful transcription example:

```python
from deepgram import DeepgramClient

client = DeepgramClient()

response = client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
    model="nova-3",
    smart_format=True,
)

print(response.results.channels[0].alternatives[0].transcript)
```

Expected output is a transcript string from the first channel and first alternative, for example:

```text
Yeah, as I say, this mission is a very important step for us.
```

## Key Features

- Sync and async root clients: `DeepgramClient` and `AsyncDeepgramClient`.
- Batch speech-to-text via `client.listen.v1.media.transcribe_url()` and `transcribe_file()`.
- Realtime streaming over typed socket clients for Listen v1, Listen v2, Speak v1, and Agent v1.
- Text-to-speech over both REST (`speak.v1.audio.generate`) and WebSocket (`speak.v1.connect`).
- Text intelligence via `read.v1.text.analyze` for sentiment, summaries, topics, and intents.
- Project, key, usage, billing, self-hosted, and reusable voice-agent configuration APIs.
- Helper utilities such as `deepgram.helpers.TextBuilder` and per-request overrides through `RequestOptions`.

## Where To Go Next

<Cards>
  <Card title="Architecture" href="/docs/architecture">See how the root client, wrappers, transports, and domain modules fit together.</Card>
  <Card title="Core Concepts" href="/docs/client-lifecycle">Understand authentication, batch requests, streaming sockets, and agent workflows.</Card>
  <Card title="API Reference" href="/docs/api-reference/deepgram-client">Jump to the exact imports, signatures, and constructor options.</Card>
</Cards>
