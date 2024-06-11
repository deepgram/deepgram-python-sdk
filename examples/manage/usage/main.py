# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import sys
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    UsageFieldsOptions,
    UsageSummaryOptions,
    UsageRequestOptions,
)

load_dotenv()


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

        # list requests
        requestId = None
        options: UsageRequestOptions = {}
        listResp = deepgram.manage.v("1").get_usage_requests(myId, options)
        if listResp is None:
            print("No requests found")
        else:
            print(f"GetUsageRequests() - listResp: {listResp}")
            for request in listResp.requests:
                requestId = request.request_id
                break
        print(f"request_id: {requestId}")
        print("")

        # get request
        reqResp = deepgram.manage.v("1").get_usage_request(myId, requestId)
        if reqResp is None:
            print("No request found")
        else:
            print(f"GetUsageRequest() - listResp: {listResp}")
        print("")

        # get fields
        options: UsageFieldsOptions = {}
        listResp = deepgram.manage.v("1").get_usage_fields(myId, options)
        if listResp is None:
            print(f"UsageFields not found.")
            sys.exit(1)
        else:
            print(f"GetUsageFields Models - listResp: {listResp}")
        print("")

        # list usage
        options: UsageSummaryOptions = {}
        listResp = deepgram.manage.v("1").get_usage_summary(myId, options)
        if listResp is None:
            print("UsageSummary not found")
        else:
            print(f"GetSummary - listResp: {listResp}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
