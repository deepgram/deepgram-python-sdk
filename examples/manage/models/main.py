# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import sys
from dotenv import load_dotenv

from deepgram import DeepgramClient

load_dotenv()


def main():
    try:
        # Create a Deepgram client using the API key
        deepgram: DeepgramClient = DeepgramClient()

        # get projects
        projectResp = deepgram.manage.v("1").get_projects()
        if projectResp is None:
            print("ListProjects failed.")
            sys.exit(1)

        myProjectId = None
        myProjectName = None
        for project in projectResp.projects:
            myProjectId = project.project_id
            myProjectName = project.name
            print(f"ListProjects() - ID: {myProjectId}, Name: {myProjectName}")
            break
        print("\n\n")

        # get models
        myModelId = None
        listModels = deepgram.manage.v("1").get_models()
        if listModels is None:
            print("No models found")
        else:
            if listModels.stt:
                for stt in listModels.stt:
                    print(
                        f"general.get_models() - Name: {stt.name}, Amount: {stt.uuid}"
                    )
                    myModelId = stt.uuid
            if listModels.tts:
                for tts in listModels.tts:
                    print(
                        f"general.get_models() - Name: {tts.name}, Amount: {tts.uuid}"
                    )
        print("\n\n")

        # get model
        listModel = deepgram.manage.v("1").get_model(myModelId)
        if listModel is None:
            print(f"No model for {myModelId} found")
        else:
            print(f"get_model() - Name: {listModel.name}, Amount: {listModel.uuid}")
        print("\n\n")

        # get project models
        myModelId = None
        listProjModels = deepgram.manage.v("1").get_project_models(myProjectId)
        if listProjModels is None:
            print(f"No model for project id {myProjectId} found")
        else:
            if listProjModels.stt:
                for stt in listProjModels.stt:
                    print(f"manage.get_models() - Name: {stt.name}, Amount: {stt.uuid}")
            if listProjModels.tts:
                for tts in listProjModels.tts:
                    print(f"manage.get_models() - Name: {tts.name}, Amount: {tts.uuid}")
                    myModelId = tts.uuid
        print("\n\n")

        # get project model
        listProjModel = deepgram.manage.v("1").get_project_model(myProjectId, myModelId)
        if listProjModel is None:
            print(f"No model {myModelId} for project id {myProjectId} found")
        else:
            print(
                f"get_model() - Name: {listProjModel.name}, Amount: {listProjModel.uuid}"
            )

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
