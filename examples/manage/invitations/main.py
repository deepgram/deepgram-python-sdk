# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
import sys
from dotenv import load_dotenv

from deepgram import DeepgramClient, InviteOptions

load_dotenv()

# environment variables
API_KEY = os.getenv("DG_API_KEY")

# Create a Deepgram client using the API key
deepgram: DeepgramClient = DeepgramClient(API_KEY)

async def main():
    try:
        # get projects
        projectResp = await deepgram.manage.get_projects()
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

        # list invites
        listResp = await deepgram.manage.get_invites(myId)
        if listResp is None:
            print("No invites found")
        else:
            for invite in listResp.invites:
                print(f"GetInvites() - Name: {invite.email}, Amount: {invite.scope}")

        # send invite
        options: InviteOptions = {
            "email": "spam@spam.com",
            "scope": "member"
        }

        getResp = await deepgram.manage.send_invite_options(myId, options)
        print(f"SendInvite() - Msg: {getResp.message}")

        # list invites
        listResp = await deepgram.manage.get_invites(myId)
        if listResp is None:
            print("No invites found")
        else:
            for invite in listResp.invites:
                print(f"GetInvites() - Name: {invite.email}, Amount: {invite.scope}")

        # delete invite
        delResp = await deepgram.manage.delete_invite(myId, "spam@spam.com")
        print(f"DeleteInvite() - Msg: {delResp.message}")

        # # leave invite
        # delResp = await deepgram.manage.leave_project(myId)
        # print(f"LeaveProject() - Msg: {delResp.message}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
