# Deepgram Python SDK Examples

This directory contains comprehensive examples demonstrating how to use the Deepgram Python SDK. Examples are organized by feature area, with each section starting at a multiple of 10.

## Examples Overview

### 01-09: Authentication

- **01-authentication-api-key.py** - API key authentication
- **02-authentication-access-token.py** - Access token authentication

### 10-19: Transcription (Listen)

- **10-transcription-prerecorded-url.py** - Transcribe audio from URL
- **11-transcription-prerecorded-file.py** - Transcribe audio from local file
- **12-transcription-prerecorded-callback.py** - Async transcription with callbacks
- **13-transcription-live-websocket.py** - Live transcription via WebSocket (Listen V1)
- **14-transcription-live-websocket-v2.py** - Live transcription via WebSocket (Listen V2)
- **15-transcription-advanced-options.py** - Advanced transcription options

### 20-29: Text-to-Speech (Speak)

- **20-text-to-speech-single.py** - Single request TTS (REST API)
- **21-text-to-speech-streaming.py** - Streaming TTS via WebSocket

### 30-39: Voice Agent

- **30-voice-agent.py** - Voice Agent configuration and usage

### 40-49: Text Intelligence (Read)

- **40-text-intelligence.py** - Text analysis using AI features

### 50-59: Management API

- **50-management-projects.py** - Project management (list, get, update, delete)
- **51-management-keys.py** - API key management (list, get, create, delete)
- **52-management-members.py** - Member management (list, remove, scopes)
- **53-management-invites.py** - Invitation management (list, send, delete, leave)
- **54-management-usage.py** - Usage statistics and request information
- **55-management-billing.py** - Billing and balance information
- **56-management-models.py** - Model information

### 60-69: On-Premises

- **60-onprem-credentials.py** - On-premises credentials management

### 70-79: Configuration & Advanced

- **70-request-options.py** - Request options including additional query parameters
- **71-error-handling.py** - Error handling patterns

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
