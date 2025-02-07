# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib
import time

from websocket_server import WebsocketServer, WebsocketServerThread

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)

from tests.utils import save_metadata_string

MODEL = "general-nova-3"

# response constants
INPUT1 = '{"channel": {"alternatives": [{"transcript": "Testing 123. Testing 123.", "confidence": 0.97866726, "words": [{"word": "testing", "start": 1.12, "end": 1.62, "confidence": 0.97866726, "punctuated_word": "Testing"}, {"word": "123", "start": 1.76, "end": 1.8399999, "confidence": 0.73616695, "punctuated_word": "123."}, {"word": "testing", "start": 1.8399999, "end": 2.34, "confidence": 0.99529773, "punctuated_word": "Testing"}, {"word": "123", "start": 2.8799999, "end": 3.3799999, "confidence": 0.9773819, "punctuated_word": "123."}]}]}, "metadata": {"model_info": {"name": "2-general-nova", "version": "2024-01-18.26916", "arch": "nova-3"}, "request_id": "0d2f1ddf-b9aa-40c9-a761-abcd8cf5734f", "model_uuid": "c0d1a568-ce81-4fea-97e7-bd45cb1fdf3c"}, "type": "Results", "channel_index": [0, 1], "duration": 3.69, "start": 0.0, "is_final": true, "from_finalize": false, "speech_final": true}'
OUTPUT1 = "Testing 123. Testing 123."

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        LiveOptions(
            language="en-US",
            smart_format=True,
            encoding="mulaw",
            channels=1,
            sample_rate=8000,
            punctuate=True,
        ),
        INPUT1,
        OUTPUT1,
    ),
]

response = ""


@pytest.mark.parametrize("options, input, output", input_output)
def test_unit_listen_websocket(options, input, output):
    # Save the options
    input_sha256sum = hashlib.sha256(input.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_options = f"tests/response_data/listen/websocket/{unique}-options.json"
    file_input = f"tests/response_data/listen/websocket/{unique}-input.cmd"
    file_resp = f"tests/response_data/listen/websocket/{unique}-response.json"
    file_error = f"tests/response_data/listen/websocket/{unique}-error.json"

    # clean up
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_input)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_options)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_resp)
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_error)

    # server
    def new_client(client, server):
        server.send_message_to_all(input)

    # start websocket server
    server = WebsocketServer(host="127.0.0.1", port=13254)
    server.set_fn_new_client(new_client)

    server.daemon = True
    server.thread = WebsocketServerThread(
        target=server.serve_forever, daemon=True, logger=None
    )
    server.thread.start()

    # Create a Deepgram client
    config = DeepgramClientOptions(
        url="ws://127.0.0.1:13254", options={"keepalive": "true"}
    )
    deepgram: DeepgramClient = DeepgramClient("", config)

    # Send the URL to Deepgram
    dg_connection = deepgram.listen.websocket.v("1")

    def on_message(self, result, **kwargs):
        global response
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        if result.is_final:
            if len(response) > 0:
                response = response + " "
            response = response + sentence

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # connect
    assert dg_connection.start(options) == True
    time.sleep(0.5)

    # each iteration is 0.5 seconds * 20 iterations = 10 second timeout
    timeout = 0
    exit = False
    while dg_connection.is_connected() and timeout < 20 and not exit:
        if response == output:
            exit = True
            break
        timeout = timeout + 1
        time.sleep(0.5)

    # close client
    dg_connection.finish()
    time.sleep(0.25)

    # close server
    server.shutdown_gracefully()

    # Check the response
    if response == "":
        assert response != "", f"Test ID: {unique} - No response received"
    elif response == "" and timeout > 20:
        assert (
            timeout < 20
        ), f"Test ID: {unique} - Timed out OR the value is not in the expected_output"

    # Check the response
    actual = response
    expected = output

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
