# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib

from deepgram import DeepgramClient, PrerecordedOptions

from tests.utils import save_metadata_string

MODEL = "general-nova-3"

# response constants
URL1 = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}
URL1_SMART_FORMAT = "Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it."
URL1_SUMMARIZE = "Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it."

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        URL1,
        PrerecordedOptions(model="nova-3", smart_format=True),
        {"results.channels.0.alternatives.0.transcript": [URL1_SMART_FORMAT]},
    ),
    (
        URL1,
        PrerecordedOptions(model="nova-3", smart_format=True, summarize="v2"),
        {
            "results.channels.0.alternatives.0.transcript": [URL1_SMART_FORMAT],
            "results.summary.short": [URL1_SUMMARIZE],
        },
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("url, options, expected_output", input_output)
async def test_daily_async_listen_rest_url(url, options, expected_output):
    # Save the options
    urlstr = json.dumps(url)
    input_sha256sum = hashlib.sha256(urlstr.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_cmd = f"tests/response_data/listen/rest/{unique}.cmd"
    file_options = f"tests/response_data/listen/rest/{unique}-options.json"
    file_resp = f"tests/response_data/listen/rest/{unique}-response.json"
    file_error = f"tests/response_data/listen/rest/{unique}-error.json"

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
    deepgram = DeepgramClient()

    # Send the URL to Deepgram
    response = await deepgram.listen.asyncrest.v("1").transcribe_url(url, options)

    # Save all the things
    save_metadata_string(file_cmd, urlstr)
    save_metadata_string(file_options, options.to_json())
    save_metadata_string(file_resp, response.to_json())

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
