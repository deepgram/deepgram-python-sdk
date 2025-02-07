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

from deepgram import DeepgramClient, PrerecordedOptions, PrerecordedResponse
from tests.utils import read_metadata_string, save_metadata_string

MODEL = "general-nova-3"

# response constants
URL1 = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}
URL1_SMART_FORMAT1 = "Yep. I said it before and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it."
URL1_SUMMARIZE1 = "Yep. I said it before and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it."

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        URL1,
        PrerecordedOptions(model="nova-3", smart_format=True),
        {"results.channels.0.alternatives.0.transcript": [URL1_SMART_FORMAT1]},
    ),
    (
        URL1,
        PrerecordedOptions(model="nova-3", smart_format=True, summarize="v2"),
        {
            "results.channels.0.alternatives.0.transcript": [URL1_SMART_FORMAT1],
            "results.summary.short": [URL1_SUMMARIZE1],
        },
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("url, options, expected_output", input_output)
async def test_unit_async_listen_rest_url(url, options, expected_output):
    # options
    urlstr = json.dumps(url)
    input_sha256sum = hashlib.sha256(urlstr.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_resp = f"tests/response_data/listen/rest/{unique}-response.json"
    file_error = f"tests/response_data/listen/rest/{unique}-error.json"

    # clean up
    with contextlib.suppress(FileNotFoundError):
        os.remove(file_error)

    # read metadata
    response_data = read_metadata_string(file_resp)

    # Create a Deepgram client
    deepgram = DeepgramClient()

    # make request
    transport = httpx.MockTransport(
        lambda request: httpx.Response(HTTPStatus.OK, content=response_data)
    )
    response = await deepgram.listen.asyncrest.v("1").transcribe_url(
        url, options, transport=transport
    )

    # Check the response
    for key, value in response.metadata.model_info.items():
        assert (
            value.name == MODEL
        ), f"Test ID: {unique} - Expected: {MODEL}, Actual: {value.name}"

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
