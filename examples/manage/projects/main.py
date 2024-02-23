# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import sys
from dotenv import load_dotenv

from deepgram import DeepgramClient, ProjectOptions

load_dotenv()

# environment variables
DELETE_PROJECT_BY_NAME = os.getenv("DG_DELETE_PROJECT_BY_NAME")


def main():
    try:
        # Create a Deepgram client using the API key
        deepgram: DeepgramClient = DeepgramClient()

        # get projects
        listResp = deepgram.manage.v("1").get_projects()
        if listResp is None:
            print(f"ListProjects failed.")
            sys.exit(1)

        myId = None
        myName = None
        myDeleteId = None
        for project in listResp.projects:
            if project.name == DELETE_PROJECT_BY_NAME:
                myDeleteId = project.project_id
            myId = project.project_id
            myName = project.name
            print(f"ListProjects() - ID: {myId}, Name: {myName}")

        # get project
        getResp = deepgram.manage.v("1").get_project(myId)
        print(f"GetProject() - Name: {getResp.name}")

        # update project
        updateOptions: ProjectOptions = {
            "name": "My TEST RENAME Example",
        }

        updateResp = deepgram.manage.v("1").update_project_option(myId, updateOptions)
        if updateResp is None:
            print(f"UpdateProject failed.")
            sys.exit(1)
        print(f"UpdateProject() - Msg: {updateResp.message}")

        # get project
        getResp = deepgram.manage.v("1").get_project(myId)
        if getResp is None:
            print(f"GetProject failed.")
            sys.exit(1)
        print(f"GetProject() - Name: {getResp.name}")

        # update project
        updateResp = deepgram.manage.v("1").update_project(myId, name=myName)
        if updateResp is None:
            print(f"UpdateProject failed.")
            sys.exit(1)
        print(f"UpdateProject() - Msg: {updateResp.message}")

        # get project
        getResp = deepgram.manage.v("1").get_project(myId)
        if getResp is None:
            print(f"GetProject failed.")
            sys.exit(1)
        print(f"GetProject() - Name: {getResp.name}")

        # delete project
        if myDeleteId == None:
            print("")
            print(
                'This example requires a project who already exists who name is in the value "DELETE_PROJECT_ID".'
            )
            print(
                "This is required to exercise the UpdateProject and DeleteProject function."
            )
            print("In the absence of this, this example will exit early.")
            print("")
            sys.exit(1)

        respDelete = deepgram.manage.v("1").delete_project(myDeleteId)
        if respDelete is None:
            print(f"DeleteProject failed.")
            sys.exit(1)
        print(f"DeleteProject() - Msg: {respDelete.message}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
