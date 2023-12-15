# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os
import sys
from dotenv import load_dotenv

from deepgram import DeepgramClient, KeyOptions

load_dotenv()

# environment variables
DELETE_MEMBER_BY_EMAIL = "enter-your-email@gmail.com"

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

        # list members
        delMemberId = None
        listResp = deepgram.manage.v("1").get_members(myId)
        if listResp is None:
            print("No members found")
        else:
            for member in listResp.members:
                if member.email == DELETE_MEMBER_BY_EMAIL:
                    delMemberId = member.member_id
                print(f"GetMembers() - ID: {member.member_id}, Email: {member.email}")

        # delete member
        if delMemberId == None:
            print("")
            print(
                'This example requires a project who already exists who name is in "DELETE_MEMBER_BY_EMAIL".'
            )
            print("This is required to exercise the RemoveMember function.")
            print("In the absence of this, this example will exit early.")
            print("")
            sys.exit(1)

        deleteResp = deepgram.manage.v("1").remove_member(myId, delMemberId)
        if deleteResp is None:
            print(f"RemoveMember failed.")
            sys.exit(1)
        else:
            print(f"RemoveMember() - Msg: {deleteResp.message}")

        # list members
        delMemberId = None
        listResp = deepgram.manage.v("1").get_members(myId)
        if listResp is None:
            print("No members found")
        else:
            for member in listResp.members:
                print(f"GetMembers() - ID: {member.member_id}, Email: {member.email}")
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
