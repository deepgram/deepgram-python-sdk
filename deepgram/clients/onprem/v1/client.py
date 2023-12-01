# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging, verboselogs

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
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        self.endpoint = "v1/projects"
        super().__init__(config)

    async def list_onprem_credentials(self, project_id: str):
        self.logger.debug("OnPremClient.list_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        res = await self.get(url)
        self.logger.verbose("result: %s", res)
        self.logger.notice("list_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.list_onprem_credentials LEAVE")
        return res

    async def get_onprem_credentials(
        self, project_id: str, distribution_credentials_id: str
    ):
        self.logger.debug("OnPremClient.get_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("distribution_credentials_id: %s", distribution_credentials_id)
        res = await self.get(url)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.get_onprem_credentials LEAVE")
        return res

    async def create_onprem_credentials(self, project_id: str, options):
        self.logger.debug("OnPremClient.create_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        res = await self.post(url, json=options)
        self.logger.verbose("result: %s", res)
        self.logger.notice("create_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.create_onprem_credentials LEAVE")
        return res

    async def delete_onprem_credentials(
        self, project_id: str, distribution_credentials_id: str
    ):
        self.logger.debug("OnPremClient.delete_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("distrbution_credentials_id: %s", distribution_credentials_id)
        res = await self.delete(url)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.delete_onprem_credentials LEAVE")
        return res
