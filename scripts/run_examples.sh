#!/bin/bash

# Check for DEEPGRAM_API_KEY in environment or .env file
if [ -z "$DEEPGRAM_API_KEY" ] && [ ! -f .env ] || ([ -f .env ] && ! grep -q "DEEPGRAM_API_KEY" .env); then
    echo "❌ DEEPGRAM_API_KEY not found in environment variables or .env file"
    echo "Please set up your Deepgram API key before running examples"
    echo "You can:"
    echo "  1. Export it: export DEEPGRAM_API_KEY=your_key_here"
    echo "  2. Add it to a .env file: echo 'DEEPGRAM_API_KEY=your_key_here' > .env"
    exit 1
fi

echo "✅ DEEPGRAM_API_KEY found, proceeding with examples..."
echo ""


echo "✨✨✨✨ Running speak/v1/audio/generate/ examples ✨✨✨✨"

echo "Running speak/v1/audio/generate/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/audio/generate/main.py
echo "Running speak/v1/audio/generate/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/audio/generate/async.py
echo "Running speak/v1/audio/generate/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/audio/generate/with_raw_response.py
echo "Running speak/v1/audio/generate/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/audio/generate/with_auth_token.py

echo "✨✨✨✨ Running speak/v1/connect/ examples ✨✨✨✨"

echo "Running speak/v1/connect/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/connect/main.py
echo "Running speak/v1/connect/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/connect/async.py
echo "Running speak/v1/connect/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/connect/with_raw_response.py
echo "Running speak/v1/connect/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/speak/v1/connect/with_auth_token.py

echo "✨✨✨✨ Running read/v1/text/analyze/ examples ✨✨✨✨"

echo "Running read/v1/text/analyze/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/read/v1/text/analyze/main.py
echo "Running read/v1/text/analyze/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/read/v1/text/analyze/async.py
echo "Running read/v1/text/analyze/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/read/v1/text/analyze/with_raw_response.py
echo "Running read/v1/text/analyze/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/read/v1/text/analyze/with_auth_token.py

echo "✨✨✨✨ Running listen/v1/connect/ examples ✨✨✨✨"

echo "Running listen/v1/connect/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/connect/main.py
echo "Running listen/v1/connect/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/connect/async.py
echo "Running listen/v1/connect/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/connect/with_raw_response.py
echo "Running listen/v1/connect/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/connect/with_auth_token.py

echo "✨✨✨✨ Running listen/v1/media/transcribe_file/ examples ✨✨✨✨"

echo "Running listen/v1/media/transcribe_file/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_file/main.py
echo "Running listen/v1/media/transcribe_file/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_file/async.py
echo "Running listen/v1/media/transcribe_file/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_file/with_raw_response.py
echo "Running listen/v1/media/transcribe_file/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_file/with_auth_token.py

echo "✨✨✨✨ Running listen/v1/media/transcribe_url/ examples ✨✨✨✨"

echo "Running listen/v1/media/transcribe_url/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_url/main.py
echo "Running listen/v1/media/transcribe_url/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_url/async.py
echo "Running listen/v1/media/transcribe_url/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_url/with_raw_response.py
echo "Running listen/v1/media/transcribe_url/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v1/media/transcribe_url/with_auth_token.py

echo "✨✨✨✨ Running listen/v2/connect/ examples ✨✨✨✨"

echo "Running listen/v2/connect/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v2/connect/main.py
echo "Running listen/v2/connect/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v2/connect/async.py
echo "Running listen/v2/connect/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v2/connect/with_raw_response.py
echo "Running listen/v2/connect/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/listen/v2/connect/with_auth_token.py

echo "✨✨✨✨ Running agent/v1/connect/ examples ✨✨✨✨"

echo "Running agent/v1/connect/main.py"
DEEPGRAM_DEBUG=1 poetry run python examples/agent/v1/connect/main.py
echo "Running agent/v1/connect/async.py"
DEEPGRAM_DEBUG=1 poetry run python examples/agent/v1/connect/async.py
echo "Running agent/v1/connect/with_raw_response.py"
DEEPGRAM_DEBUG=1 poetry run python examples/agent/v1/connect/with_raw_response.py
echo "Running agent/v1/connect/with_auth_token.py"
DEEPGRAM_DEBUG=1 poetry run python examples/agent/v1/connect/with_auth_token.py