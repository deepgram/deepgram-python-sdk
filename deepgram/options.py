# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging, verboselogs
from typing import Dict, Optional
from .errors import DeepgramApiKeyError
import re
import os


class DeepgramClientOptions:
    """
    Represents options for configuring a Deepgram client.

    This class allows you to customize various options for interacting with the Deepgram API.

    Attributes:
        api_key: (Optional) A Deepgram API key used for authentication. Default uses the `DEEPGRAM_API_KEY` environment variable.
        verbose: (Optional) The logging level for the client. Defaults to `logging.WARNING`.
        url: (Optional) The URL used to interact with production, On-prem, and other Deepgram environments. Defaults to `api.deepgram.com`.
        headers: (Optional) Headers for initializing the client.
        options: (Optional) Additional options for initializing the client.
    """

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
        verbose: int = logging.WARNING,
        headers: Dict[str, str] = None,
        options: Dict[str, str] = None,
    ):
        verboselogs.install()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

        self.verbose = verbose
        self.api_key = api_key
        self._update_headers(headers=headers)
        if len(url) == 0:
            url = "api.deepgram.com"
        self.url = self._get_url(url)
        if options is None:
            options = dict()
        self.options = options

    def set_apikey(self, api_key: str):
        self.api_key = api_key
        self._update_headers()

    def _get_url(self, url):
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = "https://" + url
        return url.strip("/")

    def _update_headers(self, headers: Optional[Dict[str, str]] = None):
        if not hasattr(self, "headers") or self.headers is None:
            self.headers = {}
        self.headers["Accept"] = "application/json"
        if self.api_key:
            self.headers["Authorization"] = f"Token {self.api_key}"
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]
        # Overwrite / add any headers that were passed in
        if headers:
            self.headers.update(headers)


class ClientOptionsFromEnv(DeepgramClientOptions):
    def __init__(
        self,
        verbose: int = logging.WARNING,
        headers: Dict[str, str] = None,
        options: Dict[str, str] = None,
    ):
        apiKey = os.getenv("DEEPGRAM_API_KEY", None)
        if apiKey is None:
            raise DeepgramApiKeyError("Deepgram API KEY is not set")

        url = os.getenv("DEEPGRAM_URL", None)
        if url is None:
            url = "api.deepgram.com"

        super().__init__(
            api_key=apiKey, url=url, verbose=verbose, headers=headers, options=options
        )
