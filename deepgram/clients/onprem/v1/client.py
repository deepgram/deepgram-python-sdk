# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs

from ...abstract_sync_client import AbstractSyncRestClient


class OnPremClient(AbstractSyncRestClient):
    """
    Client for interacting with Deepgram's on-premises API.

    This class provides methods to manage and interact with on-premises projects and distribution credentials.

    Args:
        config (DeepgramClientOptions): all the options for the client.
    """
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        self.endpoint = "v1/projects"
        super().__init__(config)

    def list_onprem_credentials(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("OnPremClient.list_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        res = self.get(url, timeout=timeout)
        self.logger.verbose("result: %s", res)
        self.logger.notice("list_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.list_onprem_credentials LEAVE")
        return res

    def get_onprem_credentials(self, project_id: str, distribution_credentials_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("OnPremClient.get_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("distribution_credentials_id: %s", distribution_credentials_id)
        res = self.get(url, timeout=timeout)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.get_onprem_credentials LEAVE")
        return res

    def create_onprem_credentials(self, project_id: str, options, timeout: httpx.Timeout = None):
        self.logger.debug("OnPremClient.create_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        res = self.post(url, json=options, timeout=timeout)
        self.logger.verbose("result: %s", res)
        self.logger.notice("create_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.create_onprem_credentials LEAVE")
        return res

    def delete_onprem_credentials(
        self, project_id: str, distribution_credentials_id: str, timeout: httpx.Timeout = None
    ):
        self.logger.debug("OnPremClient.delete_onprem_credentials ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("distrbution_credentials_id: %s", distribution_credentials_id)
        res = self.delete(url, timeout=timeout)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_onprem_credentials succeeded")
        self.logger.debug("OnPremClient.delete_onprem_credentials LEAVE")
        return res
