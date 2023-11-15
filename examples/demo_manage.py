import asyncio
import os
from deepgram import DeepgramClient
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('DG_API_KEY_MANAGE')
PROJECT_ID = os.getenv('DG_PROJECT_ID')
UPDATE_PROJECT_OPTIONS = {
    "name": "example_project_name",
    "company": "deepgram"
}
CREATE_KEY_OPTIONS = {
    "comment": "this is a comment",  # requred
    "scopes": ["keys:read", "owners:read"],
    "tags": ["my_name", "sdk_test"],
    "testkey": "test value",
    "time_to_live_in_seconds": 60000,
}

# Create a Deepgram client using the API key
deepgram: DeepgramClient = DeepgramClient(API_KEY)

async def main():
    response = await deepgram.manage.get_projects()
    # response = await deepgram.manage.get_project(PROJECT_ID)
    # response = await deepgram.manage.update_project(PROJECT_ID, UPDATE_PROJECT_OPTIONS)
    # response = await deepgram.manage.create_project_key(PROJECT_ID, CREATE_KEY_OPTIONS)

    print(response)

if __name__ == "__main__":
    asyncio.run(main())
