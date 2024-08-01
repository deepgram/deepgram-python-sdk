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

MODEL = "2-general-nova"

# response constants
FILE1 = "testing-websocket.wav"
FILE2 = "preamble-websocket.wav"
FILE1_SMART_FORMAT = "Testing. 123. Testing. 123."
FILE2_SMART_FORMAT1 = "We, the people of the United States, in order to form a more perfect union, establish justice, ensure domestic tranquility, provide for the common defense, promote the general welfare, and secure the blessings of liberty to ourselves and our posterity to ordain and establish this constitution for the United States of America."
FILE2_SMART_FORMAT2 = "We, the people of the United States, order to form a more perfect union, establish justice, ensure domestic tranquility, provide for the common defense, promote the general welfare, secure the blessings of liberty to ourselves and our posterity to ordain and establish this constitution. For the United States of America."
FILE2_SMART_FORMAT3 = "We, the people of the United States, order to form a more perfect union, establish justice, ensure domestic tranquility, provide for the common defense, promote the general welfare, secure the blessings of liberty to ourselves and our posterity to ordain and establish this constitution for the United States of America."

# Create a list of tuples to store the key-value pairs
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
        {"output": [FILE1_SMART_FORMAT]},
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
        {"output": [FILE2_SMART_FORMAT1, FILE2_SMART_FORMAT2, FILE2_SMART_FORMAT3]},
    ),
]

response = ""
raw_json = ""


@pytest.mark.parametrize("filename, options, expected_output", input_output)
def test_daily_listen_websocket(filename, options, expected_output):
    global response, raw_json
    response = ""
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
        global response, raw_json
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        if result.is_final:
            raw_json = result.to_json()  # TODO: need to handle multiple results
            if len(response) > 0:
                response = response + " "
            response = response + sentence

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # connect
    assert dg_connection.start(options) == True
    time.sleep(0.5)

    # Read the mu-law encoded WAV file using soundfile
    data, samplerate = sf.read(
        f"tests/daily_test/{filename}",
        dtype="int16",
        channels=1,
        format="RAW",
        subtype="PCM_16",
        samplerate=8000,
    )

    # Stream the audio frames in chunks
    chunk_size = 4096  # Adjust as necessary
    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size].tobytes()
        dg_connection.send(chunk)
        time.sleep(0.25)

    # each iteration is 0.5 seconds * 20 iterations = 10 second timeout
    timeout = 0
    exit = False
    while dg_connection.is_connected() and timeout < 20 and not exit:
        for key, value in expected_output.items():
            if response in value:
                exit = True
                break
        timeout = timeout + 1
        time.sleep(0.5)

    # close
    dg_connection.finish()
    time.sleep(0.25)

    # Check the response
    if response == "":
        assert response != "", f"Test ID: {unique} - No response received"
    elif response == "" and timeout > 20:
        assert (
            timeout < 20
        ), f"Test ID: {unique} - Timed out OR the value is not in the expected_output"

    # Save all the things
    save_metadata_string(file_cmd, filenamestr)
    save_metadata_string(file_options, options.to_json())
    save_metadata_string(file_resp, raw_json)

    # Check the response
    for key, value in expected_output.items():
        actual = response
        expected = value

        try:
            assert (
                actual in expected
            ), f"Test ID: {unique} - Expected: {expected}, Actual: {actual}"
        finally:
            # if asserted
            if not (actual in expected):
                failure = {
                    "actual": actual,
                    "expected": expected,
                }
                failuresstr = json.dumps(failure)
                save_metadata_string(file_error, failuresstr)
