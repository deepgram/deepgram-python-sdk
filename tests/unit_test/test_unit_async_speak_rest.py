# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib
from http import HTTPStatus

import httpx

from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions, FileSource

from tests.utils import read_metadata_string, save_metadata_string

MODEL = "aura-2-thalia-en"

# response constants
TEXT1 = "Hello, world."

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        TEXT1,
        SpeakOptions(model=MODEL, encoding="linear16", sample_rate=24000),
        {
            "content_type": ["audio/wav"],
            "model_name": ["aura-2-thalia-en"],
            "characters": ["13"],
        },
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("text, options, expected_output", input_output)
async def test_unit_async_speak_rest(text, options, expected_output):
    # Save the options
    input_sha256sum = hashlib.sha256(text.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_resp = f"tests/response_data/speak/rest/{unique}-response.json"
    file_error = f"tests/response_data/speak/rest/{unique}-error.json"

    # clean up
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_error)

    # read metadata
    response_data = read_metadata_string(file_resp)
    response_data = response_data.replace("_", "-")
    response_data = response_data.replace("characters", "char-count")

    # convert to json to fix the char-count to string
    headers = json.loads(response_data)
    headers["char-count"] = str(headers.get("char-count"))

    # Create a Deepgram client
    deepgram = DeepgramClient()

    # input text
    input_text = {"text": text}

    # Send the URL to Deepgram
    transport = httpx.MockTransport(
        lambda request: httpx.Response(HTTPStatus.OK, headers=headers)
    )
    response = await deepgram.speak.asyncrest.v("1").stream_memory(
        input_text, options, transport=transport
    )
    # convert to string
    response["characters"] = str(response["characters"])

    # Check the response
    for key, value in expected_output.items():
        actual = response.eval(key)
        expected = value

        try:
            assert (
                actual in expected
            ), f"Test ID: {unique} - Key: {key}, Expected: {expected}, Actual: {actual}"
        finally:
            # if asserted
            if not (actual in expected):
                failure = {
                    "actual": actual,
                    "expected": expected,
                }
                failuresstr = json.dumps(failure)
                save_metadata_string(file_error, failuresstr)
