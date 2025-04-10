# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging

from ....utils import verboselogs
from ....options import DeepgramClientOptions
from ...common import AbstractAsyncRestClient
from .response import GrantTokenResponse


class AsyncAuthRESTClient(AbstractAsyncRestClient):
    """
    A client class for handling authentication endpoints.
    Provides method for generating a temporary JWT token.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config
        self._endpoint = "v1/auth/grant"
        super().__init__(config)

    async def grant_token(self):
        """
        Generates a temporary JWT with a 30 second TTL.

        Returns:
            GrantTokenResponse: An object containing the authentication token and its expiration time.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("AuthRestClient.grant_token ENTER")

        url = f"{self._config.url}/{self._endpoint}"
        self._logger.info("url: %s", url)
        result = await self.post(url, headers={"Authorization": f"Token {self._config.api_key}"})
        self._logger.info("json: %s", result)
        res = GrantTokenResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("grant_token succeeded")
        self._logger.debug("AuthRestClient.grant_token LEAVE")
        return res
