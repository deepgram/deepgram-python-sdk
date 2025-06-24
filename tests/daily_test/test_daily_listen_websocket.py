# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib
import time
import soundfile as sf

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)

from tests.utils import save_metadata_string

MODEL = "general-nova-3"

# test files
FILE1 = "testing-websocket.wav"
FILE2 = "preamble-websocket.wav"

# Create a list of tuples to store the key-value pairs for testing
input_output = [
    (
        FILE1,
        LiveOptions(
            language="en-US",
            smart_format=True,
            encoding="mulaw",
            channels=1,
            sample_rate=8000,
            punctuate=True,
        ),
    ),
    (
        FILE2,
        LiveOptions(
            language="en-US",
            smart_format=True,
            encoding="mulaw",
            channels=1,
            sample_rate=8000,
            punctuate=True,
        ),
    ),
]

transcript_received = False
message_structure_valid = False
raw_json = ""


@pytest.mark.parametrize("filename, options", input_output)
def test_daily_listen_websocket(filename, options):
    global transcript_received, message_structure_valid, raw_json
    transcript_received = False
    message_structure_valid = False
    raw_json = ""

    # Save the options
    filenamestr = json.dumps(filename)
    input_sha256sum = hashlib.sha256(filenamestr.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_cmd = f"tests/response_data/listen/websocket/{unique}.cmd"
    file_options = f"tests/response_data/listen/websocket/{unique}-options.json"
    file_resp = f"tests/response_data/listen/websocket/{unique}-response.json"
    file_error = f"tests/response_data/listen/websocket/{unique}-error.json"

    # clean up
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_cmd)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_options)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_resp)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_error)

    # Create a Deepgram client
    config = DeepgramClientOptions(options={"keepalive": "true"})
    deepgram: DeepgramClient = DeepgramClient("", config)

    # Send the URL to Deepgram
    dg_connection = deepgram.listen.websocket.v("1")

    def on_message(self, result, **kwargs):
        global transcript_received, message_structure_valid, raw_json

        # Validate message structure - should have expected fields
        try:
            # Check if we can access the transcript (validates structure)
            transcript = result.channel.alternatives[0].transcript

            # Validate that essential fields exist
            assert hasattr(
                result, 'channel'), "Result should have channel field"
            assert hasattr(
                result, 'is_final'), "Result should have is_final field"
            assert hasattr(
                result, 'metadata'), "Result should have metadata field"
            assert hasattr(
                result.channel, 'alternatives'), "Channel should have alternatives"
            assert len(
                result.channel.alternatives) > 0, "Should have at least one alternative"

            message_structure_valid = True
            raw_json = result.to_json()

            # We received a transcript event (regardless of content)
            transcript_received = True

        except Exception as e:
            print(f"Message structure validation failed: {e}")
            message_structure_valid = False

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # Test connection establishment
    connection_started = dg_connection.start(options)
    assert connection_started == True, f"Test ID: {unique} - WebSocket connection should start successfully"

    # Verify connection is active
    time.sleep(0.5)
    assert dg_connection.is_connected(
    ), f"Test ID: {unique} - WebSocket should be connected"

    # Read and send audio data
    data, samplerate = sf.read(
        f"tests/daily_test/{filename}",
        dtype="int16",
        channels=1,
        format="RAW",
        subtype="PCM_16",
        samplerate=8000,
    )

    # Stream the audio frames in chunks
    chunk_size = 4096
    for i in range(0, len(data), chunk_size):
        chunk = data[i: i + chunk_size].tobytes()
        dg_connection.send(chunk)
        time.sleep(0.25)

    # Wait for transcript event (up to 10 seconds)
    timeout = 0
    while not transcript_received and timeout < 20:
        timeout += 1
        time.sleep(0.5)

    # Close connection
    dg_connection.finish()
    time.sleep(0.25)

    # Save test metadata
    save_metadata_string(file_cmd, filenamestr)
    save_metadata_string(file_options, options.to_json())
    if raw_json:
        save_metadata_string(file_resp, raw_json)

    # Infrastructure tests - verify connection and message structure
    assert transcript_received, f"Test ID: {unique} - Should receive at least one transcript event"
    assert message_structure_valid, f"Test ID: {unique} - Transcript message structure should be valid"

    # Verify connection closed properly
    assert not dg_connection.is_connected(
    ), f"Test ID: {unique} - WebSocket should be disconnected after finish()"
