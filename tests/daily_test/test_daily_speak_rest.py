# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import contextlib
import os
import json
import pytest
import hashlib

from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions, FileSource

from tests.utils import save_metadata_string

TTS_MODEL = "aura-asteria-en"
STT_MODEL = "2-general-nova"

# response constants
TEXT1 = "Hello, world."

# Create a list of tuples to store the key-value pairs
input_output = [
    (
        TEXT1,
        SpeakOptions(model=TTS_MODEL, encoding="linear16", sample_rate=24000),
        PrerecordedOptions(model="nova-2", smart_format=True),
        {"results.channels.0.alternatives.0.transcript": [TEXT1]},
    ),
]


@pytest.mark.parametrize(
    "text, tts_options, stt_options, expected_output", input_output
)
def test_daily_speak_rest(text, tts_options, stt_options, expected_output):
    # Save the options
    input_sha256sum = hashlib.sha256(text.encode()).hexdigest()
    option_sha256sum = hashlib.sha256(tts_options.to_json().encode()).hexdigest()

    unique = f"{option_sha256sum}-{input_sha256sum}"

    # filenames
    audio_file = f"tests/response_data/speak/rest/{unique}.wav"
    file_cmd = f"tests/response_data/speak/rest/{unique}.cmd"
    file_options = f"tests/response_data/speak/rest/{unique}-options.json"
    file_resp = f"tests/response_data/speak/rest/{unique}-response.json"
    file_error = f"tests/response_data/speak/rest/{unique}-error.json"

    # clean up
    with contextlib.suppress(FileNotFoundError):
        os.remove(audio_file)
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

    # input text
    input_text = {"text": text}

    # Send the URL to Deepgram
    response = deepgram.speak.rest.v("1").stream_memory(input_text, tts_options)

    # Save all the things
    save_metadata_string(file_cmd, text)
    save_metadata_string(file_options, tts_options.to_json())
    save_metadata_string(file_resp, response.to_json())

    with open(audio_file, "wb+") as file:
        file.write(response.stream_memory.getbuffer())
        file.flush()

    # Check the response
    # file buffer
    with open(audio_file, "rb") as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }

    # Send the URL to Deepgram
    response = deepgram.listen.rest.v("1").transcribe_file(payload, stt_options)

    # Check the response
    for key, value in response.metadata.model_info.items():
        assert (
            value.name == STT_MODEL
        ), f"Test ID: {unique} - Expected: {STT_MODEL}, Actual: {value.name}"

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
