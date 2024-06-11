# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Optional

import httpx

from deepgram.utils import verboselogs
from ....options import DeepgramClientOptions
from ...abstract_sync_client import AbstractSyncRestClient


class OnPremClient(AbstractSyncRestClient):
    """
    Client for interacting with Deepgram's on-premises API.

    This class provides methods to manage and interact with on-premises projects and distribution credentials.

    Args:
        config (DeepgramClientOptions): all the options for the client.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config
        self._endpoint = "v1/projects"
        super().__init__(config)

    def list_onprem_credentials(
        self, project_id: str, timeout: Optional[httpx.Timeout] = None
    ):
        """
        List all on-premises distribution credentials for a project.
        """
        self._logger.debug("OnPremClient.list_onprem_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/onprem/distribution/credentials"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        res = self.get(url, timeout=timeout)
        self._logger.verbose("result: %s", res)
        self._logger.notice("list_onprem_credentials succeeded")
        self._logger.debug("OnPremClient.list_onprem_credentials LEAVE")
        return res

    def get_onprem_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
    ):
        """
        Get a specific on-premises distribution credential for a project.
        """
        self._logger.debug("OnPremClient.get_onprem_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info(
            "distribution_credentials_id: %s", distribution_credentials_id
        )
        res = self.get(url, timeout=timeout)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_onprem_credentials succeeded")
        self._logger.debug("OnPremClient.get_onprem_credentials LEAVE")
        return res

    def create_onprem_credentials(
        self, project_id: str, options, timeout: Optional[httpx.Timeout] = None
    ):
        """
        Create a new on-premises distribution credential for a project.
        """
        self._logger.debug("OnPremClient.create_onprem_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/onprem/distribution/credentials/"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("options: %s", options)
        res = self.post(url, json=options, timeout=timeout)
        self._logger.verbose("result: %s", res)
        self._logger.notice("create_onprem_credentials succeeded")
        self._logger.debug("OnPremClient.create_onprem_credentials LEAVE")
        return res

    def delete_onprem_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
    ):
        """
        Delete an on-premises distribution credential for a project.
        """
        self._logger.debug("OnPremClient.delete_onprem_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/onprem/distribution/credentials/{distribution_credentials_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("distrbution_credentials_id: %s", distribution_credentials_id)
        res = self.delete(url, timeout=timeout)
        self._logger.verbose("result: %s", res)
        self._logger.notice("delete_onprem_credentials succeeded")
        self._logger.debug("OnPremClient.delete_onprem_credentials LEAVE")
        return res
