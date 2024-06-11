# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import sys
import re
import os
from typing import Dict, Optional
import logging

from deepgram import __version__
from deepgram.utils import verboselogs
from .errors import DeepgramApiKeyError


class DeepgramClientOptions:
    """
    Represents options for configuring a Deepgram client.

    This class allows you to customize various options for interacting with the Deepgram API.

    Attributes:
        api_key: (Optional) A Deepgram API key used for authentication. Default uses the `DEEPGRAM_API_KEY` environment variable.
        url: (Optional) The URL used to interact with production, On-prem, and other Deepgram environments. Defaults to `api.deepgram.com`.
        verbose: (Optional) The logging level for the client. Defaults to `verboselogs.WARNING`.
        headers: (Optional) Headers for initializing the client.
        options: (Optional) Additional options for initializing the client.
    """

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
    ):
        self.logger = verboselogs.VerboseLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

        if api_key is None:
            api_key = ""

        self.verbose = verbose
        self.api_key = api_key
        self._update_headers(headers=headers)

        if len(url) == 0:
            url = "api.deepgram.com"
        self.url = self._get_url(url)

        if options is None:
            options = {}
        self.options = options

    def set_apikey(self, api_key: str):
        """
        set_apikey: Sets the API key for the client.

        Args:
            api_key: The Deepgram API key used for authentication.
        """
        self.api_key = api_key
        self._update_headers()

    def _get_url(self, url):
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = "https://" + url
        return url.strip("/")

    def _update_headers(self, headers: Optional[Dict] = None):
        self.headers = {}
        self.headers["Accept"] = "application/json"
        if self.api_key:
            self.headers["Authorization"] = f"Token {self.api_key}"
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]
        self.headers["User-Agent"] = (
            f"@deepgram/sdk/{__version__} python/{sys.version_info[1]}.{sys.version_info[2]}"
        )
        # Overwrite / add any headers that were passed in
        if headers:
            self.headers.update(headers)


class ClientOptionsFromEnv(
    DeepgramClientOptions
):  # pylint: disable=too-many-branches, too-many-statements
    """
    This class extends DeepgramClientOptions and will attempt to use environment variables first before defaults.
    """

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
    ):
        self.logger = verboselogs.VerboseLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(verboselogs.WARNING)  # temporary set for setup

        if api_key is None:
            api_key = ""

        if api_key == "":
            api_key = os.getenv("DEEPGRAM_API_KEY", "")
            if api_key == "":
                self.logger.critical("Deepgram API KEY is not set")
                raise DeepgramApiKeyError("Deepgram API KEY is not set")

        if url == "":
            url = os.getenv("DEEPGRAM_HOST", "api.deepgram.com")
            self.logger.notice(f"Deepgram host is set to {url}")

        if verbose == verboselogs.WARNING:
            _loglevel = os.getenv("DEEPGRAM_LOGGING", "")
            if _loglevel != "":
                verbose = int(_loglevel)
            if isinstance(verbose, str):
                match verbose:
                    case "NOTSET":
                        self.logger.notice("Logging level is set to NOTSET")
                        verbose = verboselogs.NOTSET
                    case "SPAM":
                        self.logger.notice("Logging level is set to SPAM")
                        verbose = verboselogs.SPAM
                    case "DEBUG":
                        self.logger.notice("Logging level is set to DEBUG")
                        verbose = verboselogs.DEBUG
                    case "VERBOSE":
                        self.logger.notice("Logging level is set to VERBOSE")
                        verbose = verboselogs.VERBOSE
                    case "NOTICE":
                        self.logger.notice("Logging level is set to NOTICE")
                        verbose = verboselogs.NOTICE
                    case "WARNING":
                        self.logger.notice("Logging level is set to WARNING")
                        verbose = verboselogs.WARNING
                    case "SUCCESS":
                        self.logger.notice("Logging level is set to SUCCESS")
                        verbose = verboselogs.SUCCESS
                    case "ERROR":
                        self.logger.notice("Logging level is set to ERROR")
                        verbose = verboselogs.ERROR
                    case "CRITICAL":
                        self.logger.notice("Logging level is set to CRITICAL")
                        verbose = verboselogs.CRITICAL
                    case _:
                        self.logger.notice("Logging level is set to WARNING")
                        verbose = verboselogs.WARNING
        self.logger.notice(f"Logging level is set to {verbose}")

        if headers is None:
            headers = {}
            for x in range(0, 20):
                header = os.getenv(f"DEEPGRAM_HEADER_{x}", None)
                if header is not None:
                    headers[header] = os.getenv(f"DEEPGRAM_HEADER_VALUE_{x}", None)
                    self.logger.debug(
                        "Deepgram header %s is set with value %s",
                        header,
                        headers[header],
                    )
                else:
                    break
            if len(headers) == 0:
                self.logger.notice("Deepgram headers are not set")
                headers = None

        if options is None:
            options = {}
            for x in range(0, 20):
                param = os.getenv(f"DEEPGRAM_PARAM_{x}", None)
                if param is not None:
                    options[param] = os.getenv(f"DEEPGRAM_PARAM_VALUE_{x}", None)
                    self.logger.debug(
                        "Deepgram option %s is set with value %s", param, options[param]
                    )
                else:
                    break
            if len(options) == 0:
                self.logger.notice("Deepgram options are not set")
                options = None

        super().__init__(
            api_key=api_key, url=url, verbose=verbose, headers=headers, options=options
        )
