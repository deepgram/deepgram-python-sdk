# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import sys
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    UsageFieldsOptions,
    UsageSummaryOptions,
    UsageRequestOptions,
)

load_dotenv()

def main():
    try:
        # Create a Deepgram client using the API key
        deepgram = DeepgramClient()

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

        # list requests
        requestId = None
        options: UsageRequestOptions = {}
        listResp = deepgram.manage.v("1").get_usage_requests(myId, options)
        if listResp is None:
            print("No requests found")
        else:
            for request in listResp.requests:
                requestId = request.request_id
                print(f"GetUsageRequests() - ID: {requestId}, Path: {request.path}")
        print(f"request_id: {requestId}")
        print("")

        # get request
        reqResp = deepgram.manage.v("1").get_usage_request(myId, requestId)
        if reqResp is None:
            print("No request found")
        else:
            for request in listResp.requests:
                print(
                    f"GetUsageRequest() - ID: {request.request_id}, Path: {request.path}"
                )
        print("")

        # get fields
        options: UsageFieldsOptions = {}
        listResp = deepgram.manage.v("1").get_usage_fields(myId, options)
        if listResp is None:
            print(f"UsageFields not found.")
            sys.exit(1)
        else:
            for model in listResp.models:
                print(
                    f"GetUsageFields Models - ID: {model.model_id}, Name: {model.name}"
                )
            for method in listResp.processing_methods:
                print(f"GetUsageFields Methods: {method}")
        print("")

        # list usage
        options: UsageSummaryOptions = {}
        listResp = deepgram.manage.v("1").get_usage_summary(myId, options)
        if listResp is None:
            print("UsageSummary not found")
        else:
            for item in listResp.results:
                print(f"GetSummary - {item.requests} Calls/{listResp.resolution.units}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
