# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import sys
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

import httpx

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

AUDIO_FILE = "sample.mp3"


def main():
    try:
        # Create a Deepgram client using the API key
        # config: DeepgramClientOptions = DeepgramClientOptions(verbose=verboselogs.SPAM)
        config: DeepgramClientOptions = DeepgramClientOptions()
        deepgram: DeepgramClient = DeepgramClient("", config)

        # get projects
        projectResp = deepgram.manage.v("1").get_projects()
        if projectResp is None:
            print(f"ListProjects failed.")
            sys.exit(1)

        myId = None
        myName = None
        for project in projectResp.projects:
            myId = project.project_id
            myName = project.name
            print(f"ListProjects() - ID: {myId}, Name: {myName}")
            break

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options: PrerecordedOptions = PrerecordedOptions(
            callback="http://example.com",
            model="nova-3",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        request_id = (
            response.request_id
        )  # without callback: response.metadata.request_id
        print(f"request_id: {request_id}")

        # get request
        getResp = deepgram.manage.v("1").get_usage_request(myId, request_id)
        if getResp is None:
            print("No request found")
        else:
            print(f"GetUsageRequest() - getResp: {getResp}")
        print("\n\n\n")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
