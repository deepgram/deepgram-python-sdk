# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Optional

import httpx

from ....utils import verboselogs
from ....options import DeepgramClientOptions
from ...abstract_sync_client import AbstractSyncRestClient


class SelfHostedClient(AbstractSyncRestClient):
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
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        List all on-premises distribution credentials for a project.
        """
        return self.list_selfhosted_credentials(project_id, timeout=timeout, **kwargs)

    def list_selfhosted_credentials(
        self,
        project_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        List all on-premises distribution credentials for a project.
        """
        self._logger.debug("SelfHostedClient.list_selfhosted_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/selfhosted/distribution/credentials"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        res = self.get(url, timeout=timeout, **kwargs)
        self._logger.verbose("result: %s", res)
        self._logger.notice("list_selfhosted_credentials succeeded")
        self._logger.debug("SelfHostedClient.list_selfhosted_credentials LEAVE")
        return res

    def get_onprem_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Get a specific on-premises distribution credential for a project.
        """
        return self.get_selfhosted_credentials(
            project_id, distribution_credentials_id, timeout=timeout, **kwargs
        )

    def get_selfhosted_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Get a specific on-premises distribution credential for a project.
        """
        self._logger.debug("SelfHostedClient.get_selfhosted_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/selfhosted/distribution/credentials/{distribution_credentials_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info(
            "distribution_credentials_id: %s", distribution_credentials_id
        )
        res = self.get(url, timeout=timeout, **kwargs)
        self._logger.verbose("result: %s", res)
        self._logger.notice("get_selfhosted_credentials succeeded")
        self._logger.debug("SelfHostedClient.get_selfhosted_credentials LEAVE")
        return res

    def create_onprem_credentials(
        self,
        project_id: str,
        options,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Create a new on-premises distribution credential for a project.
        """
        return self.create_selfhosted_credentials(
            project_id, options, timeout=timeout, **kwargs
        )

    def create_selfhosted_credentials(
        self,
        project_id: str,
        options,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Create a new on-premises distribution credential for a project.
        """
        self._logger.debug("SelfHostedClient.create_selfhosted_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/selfhosted/distribution/credentials/"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("options: %s", options)
        res = self.post(url, json=options, timeout=timeout, **kwargs)
        self._logger.verbose("result: %s", res)
        self._logger.notice("create_selfhosted_credentials succeeded")
        self._logger.debug("SelfHostedClient.create_selfhosted_credentials LEAVE")
        return res

    def delete_onprem_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Delete an on-premises distribution credential for a project.
        """
        return self.delete_selfhosted_credentials(
            project_id, distribution_credentials_id, timeout=timeout, **kwargs
        )

    def delete_selfhosted_credentials(
        self,
        project_id: str,
        distribution_credentials_id: str,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ):
        """
        Delete an on-premises distribution credential for a project.
        """
        self._logger.debug("SelfHostedClient.delete_selfhosted_credentials ENTER")
        url = f"{self._config.url}/{self._endpoint}/{project_id}/selfhosted/distribution/credentials/{distribution_credentials_id}"
        self._logger.info("url: %s", url)
        self._logger.info("project_id: %s", project_id)
        self._logger.info("distrbution_credentials_id: %s", distribution_credentials_id)
        res = self.delete(url, timeout=timeout, **kwargs)
        self._logger.verbose("result: %s", res)
        self._logger.notice("delete_selfhosted_credentials succeeded")
        self._logger.debug("SelfHostedClient.delete_selfhosted_credentials LEAVE")
        return res
