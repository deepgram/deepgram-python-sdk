# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ...abstract_client import AbstractRestfulClient


class OnPremClient(AbstractRestfulClient):
    """
    Client for interacting with Deepgram's on-premises API.

    This class provides methods to manage and interact with on-premises projects and distribution credentials.

    Args:
        config (DeepgramClientOptions): all the options for the client.

    Attributes:
        endpoint (str): The API endpoint for on-premises projects.

    Methods:
        list_onprem_credentials: Lists on-premises distribution credentials for a specific project.
        get_onprem_credentials: Retrieves details of a specific on-premises distribution credential for a project.
        create_onprem_credentials: Creates a new on-premises distribution credential for a project.
        delete_onprem_credentials: Deletes an on-premises distribution credential for a project.

    """

    def __init__(self, config):
        self.config = config
        self.endpoint = "v1/projects"
        super().__init__(config)

    async def list_onprem_credentials(self, project_id: str):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials"
        return await self.get(url)

    async def get_onprem_credentials(
        self, project_id: str, distribution_credentials_id: str
    ):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        return await self.get(url)

    async def create_onprem_credentials(self, project_id: str, options):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/"
        return await self.post(url, json=options)

    async def delete_onprem_credentials(
        self, project_id: str, distribution_credentials_id: str
    ):
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        return await self.delete(url)
