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

    async def grant_token(self, ttl_seconds: int = None):
        """
        Generates a temporary JWT with a configurable TTL.

        Args:
            ttl_seconds (int, optional): Time to live in seconds for the token.
                Must be between 1 and 3600 seconds. Defaults to 30 seconds.

        Returns:
            GrantTokenResponse: An object containing the authentication token and its expiration time.

        Raises:
            DeepgramTypeError: Raised for known API errors.
            ValueError: Raised when ttl_seconds is not within valid range.
        """
        self._logger.debug("AuthRestClient.grant_token ENTER")

        # Validate ttl_seconds if provided
        if ttl_seconds is not None:
            if not isinstance(ttl_seconds, int) or isinstance(ttl_seconds, bool) or ttl_seconds < 1 or ttl_seconds > 3600:
                raise ValueError("ttl_seconds must be an integer between 1 and 3600")

        url = f"{self._config.url}/{self._endpoint}"
        self._logger.info("url: %s", url)

        # Prepare request body
        request_body = {}
        if ttl_seconds is not None:
            request_body["ttl_seconds"] = ttl_seconds

        # Make the request
        if request_body:
            result = await self.post(
                url,
                headers={"Authorization": f"Token {self._config.api_key}"},
                json=request_body
            )
        else:
            result = await self.post(
                url, headers={"Authorization": f"Token {self._config.api_key}"}
            )

        self._logger.info("json: %s", result)
        res = GrantTokenResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("grant_token succeeded")
        self._logger.debug("AuthRestClient.grant_token LEAVE")
        return res
