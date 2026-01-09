# Deepgram Python SDK Examples

This directory contains comprehensive examples demonstrating how to use the Deepgram Python SDK. These examples cover all major use cases and demonstrate production-ready patterns.

## Examples Overview

### Authentication

- **01-authentication-api-key.py** - API key authentication
- **02-authentication-access-token.py** - Access token authentication

### Transcription

- **04-transcription-prerecorded-url.py** - Transcribe audio from URL
- **05-transcription-prerecorded-file.py** - Transcribe audio from local file
- **06-transcription-prerecorded-callback.py** - Async transcription with callbacks
- **07-transcription-live-websocket.py** - Live transcription via WebSocket (Listen V1)
- **22-transcription-advanced-options.py** - Advanced transcription options
- **26-transcription-live-websocket-v2.py** - Live transcription via WebSocket (Listen V2)

### Voice Agent

- **09-voice-agent.py** - Voice Agent configuration and usage

### Text-to-Speech

- **10-text-to-speech-single.py** - Single request TTS
- **11-text-to-speech-streaming.py** - Streaming TTS via WebSocket
- **25-text-builder-demo.py** - TextBuilder demo (no API key required)
- **25-text-builder-helper.py** - TextBuilder with live TTS generation

### Text Intelligence

- **12-text-intelligence.py** - Text analysis using AI features

### Management API

- **13-management-projects.py** - Project management (list, get, update, delete)
- **14-management-keys.py** - API key management (list, get, create, delete)
- **15-management-members.py** - Member management (list, remove, scopes)
- **16-management-invites.py** - Invitation management (list, send, delete, leave)
- **17-management-usage.py** - Usage statistics and request information
- **18-management-billing.py** - Billing and balance information
- **19-management-models.py** - Model information

### On-Premises

- **20-onprem-credentials.py** - On-premises credentials management

### Configuration & Advanced

- **23-request-options.py** - Request options including additional query parameters
- **24-error-handling.py** - Error handling patterns

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your API key as an environment variable:

```bash
export DEEPGRAM_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```bash
DEEPGRAM_API_KEY=your-api-key-here
```

3. Run an example:

```bash
python examples/01-authentication-api-key.py
```

## Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

## Documentation

For more information, see:

- [API Reference](https://developers.deepgram.com/reference/deepgram-api-overview)
- [SDK README](../README.md)
- [Reference Documentation](../reference.md)

## Notes

- All examples use production-ready patterns, not testing patterns
- Examples demonstrate both synchronous and async usage (see comments in each file)
- Replace placeholder values (API keys, project IDs, etc.) with actual values
- Some examples require specific file paths or URLs - adjust as needed for your environment
- Each example includes comments showing variations (async, access tokens, etc.)
