# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import os
import sys
from dotenv import load_dotenv

from deepgram import DeepgramClient, KeyOptions

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

        # list keys
        listResp = await deepgram.manage.get_keys(myId)
        if listResp is None:
            print("No keys found")
        else:
            for key in listResp.api_keys:
                print(f"GetKeys() - ID: {key.api_key.api_key_id}, Member: {key.member.email}, Comment: {key.api_key.comment}, Scope: {key.api_key.scopes}")

        # create key
        options: KeyOptions = {
            "comment": "MyTestKey",
            "scopes": ["member"]
        }

        myKeyId = None
        createResp = await deepgram.manage.create_key(myId, options)
        if createResp is None:
            print(f"CreateKey failed.")
            sys.exit(1)
        else:
            myKeyId = createResp.api_key_id
            print(f"CreateKey() - ID: {myKeyId}, Comment: {createResp.comment} Scope: {createResp.scopes}")

        # list keys
        listResp = await deepgram.manage.get_keys(myId)
        if listResp is None:
            print("No keys found")
        else:
            for key in listResp.api_keys:
                print(f"GetKeys() - ID: {key.api_key.api_key_id}, Member: {key.member.email}, Comment: {key.api_key.comment}, Scope: {key.api_key.scopes}")

        # get key
        getResp = await deepgram.manage.get_key(myId, myKeyId)
        if getResp is None:
            print(f"GetKey failed.")
            sys.exit(1)
        else:
            print(f"GetKey() - ID: {key.api_key.api_key_id}, Member: {key.member.email}, Comment: {key.api_key.comment}, Scope: {key.api_key.scopes}")

        # delete key
        deleteResp = await deepgram.manage.delete_key(myId, myKeyId)
        if deleteResp is None:
            print(f"DeleteKey failed.")
            sys.exit(1)
        else:
            print(f"DeleteKey() - Msg: {deleteResp.message}")

        # list keys
        listResp = await deepgram.manage.get_keys(myId)
        if listResp is None:
            print("No keys found")
        else:
            for key in listResp.api_keys:
                print(f"GetKeys() - ID: {key.api_key.api_key_id}, Member: {key.member.email}, Comment: {key.api_key.comment}, Scope: {key.api_key.scopes}")
    except Exception as e:
        print(f"Exception: {e}")
 
if __name__ == "__main__":
    asyncio.run(main())
