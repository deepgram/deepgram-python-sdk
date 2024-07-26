# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib

from deepgram import DeepgramClient, AnalyzeOptions, FileSource

from tests.utils import save_metadata_string

# response constants
FILE1 = "conversation.txt"
FILE1_SUMMARIZE1 = "*"

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        FILE1,
        AnalyzeOptions(language="en", summarize=True),
        {
            "results.summary.text": [
                FILE1_SUMMARIZE1,
            ]
        },
    ),
]


@pytest.mark.parametrize("filename, options, expected_output", input_output)
def test_daily_analyze_rest_file(filename, options, expected_output):
    # Save the options
    filenamestr = json.dumps(filename)
    input_sha256sum = hashlib.sha256(filenamestr.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    file_cmd = f"tests/response_data/read/rest/{unique}.cmd"
    file_options = f"tests/response_data/read/rest/{unique}-options.json"
    file_resp = f"tests/response_data/read/rest/{unique}-response.json"
    file_error = f"tests/response_data/read/rest/{unique}-error.json"

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

    # file buffer
    with open(f"tests/daily_test/{filename}", "rb") as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }

    # Send the URL to Deepgram
    response = deepgram.read.analyze.v("1").analyze_text(payload, options)

    # Save all the things
    save_metadata_string(file_cmd, filenamestr)
    save_metadata_string(file_options, options.to_json())
    save_metadata_string(file_resp, response.to_json())

    # Check the response
    for key, value in expected_output.items():
        actual = response.eval(key)
        expected = value

        try:
            assert (
                actual in expected or expected != "*"
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
