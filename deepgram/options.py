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
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
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

    def _update_headers(self, headers: Optional[Dict] = None):
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
        api_key: str = "",
        url: str = "",
        verbose: int = logging.WARNING,
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
    ):
        verboselogs.install()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.WARNING)  # temporary set for setup

        if api_key == "":
            api_key = os.getenv("DEEPGRAM_API_KEY", "")
            if api_key == "":
                self.logger.critical("Deepgram API KEY is not set")
                raise DeepgramApiKeyError("Deepgram API KEY is not set")

        if url == "":
            url = os.getenv("DEEPGRAM_HOST", "api.deepgram.com")
            self.logger.notice(f"Deepgram host is set to {url}")

        if verbose == logging.WARNING:
            _loglevel = os.getenv("DEEPGRAM_LOGGING", "")
            if _loglevel != "":
                verbose = int(_loglevel)
            if type(verbose) != int:
                match verbose:
                    case "NOTSET":
                        self.logger.notice("Logging level is set to NOTSET")
                        verbose = logging.NOTSET
                    case "SPAM":
                        self.logger.notice("Logging level is set to SPAM")
                        verbose = logging.SPAM
                    case "DEBUG":
                        self.logger.notice("Logging level is set to DEBUG")
                        verbose = logging.DEBUG
                    case "VERBOSE":
                        self.logger.notice("Logging level is set to VERBOSE")
                        verbose = logging.VERBOSE
                    case "NOTICE":
                        self.logger.notice("Logging level is set to NOTICE")
                        verbose = logging.NOTICE
                    case "WARNING":
                        self.logger.notice("Logging level is set to WARNING")
                        verbose = logging.WARNING
                    case "SUCCESS":
                        self.logger.notice("Logging level is set to SUCCESS")
                        verbose = logging.SUCCESS
                    case "ERROR":
                        self.logger.notice("Logging level is set to ERROR")
                        verbose = logging.ERROR
                    case "CRITICAL":
                        self.logger.notice("Logging level is set to CRITICAL")
                        verbose = logging.CRITICAL
                    case _:
                        self.logger.notice("Logging level is set to WARNING")
                        verbose = logging.WARNING
        self.logger.notice(f"Logging level is set to {verbose}")

        if headers is None:
            headers = dict()
            for x in range(0, 20):
                header = os.getenv(f"DEEPGRAM_HEADER_{x}", None)
                if header is not None:
                    headers[header] = os.getenv(f"DEEPGRAM_HEADER_VALUE_{x}", None)
                    self.logger.debug(
                        f"Deepgram header {header} is set with value {headers[header]}"
                    )
                else:
                    break
            if len(headers) == 0:
                self.logger.notice("Deepgram headers are not set")
                headers = None

        if options is None:
            options = dict()
            for x in range(0, 20):
                param = os.getenv(f"DEEPGRAM_PARAM_{x}", None)
                if param is not None:
                    options[param] = os.getenv(f"DEEPGRAM_PARAM_VALUE_{x}", None)
                    self.logger.debug(
                        f"Deepgram option {param} is set with value {options[param]}"
                    )
                else:
                    break
            if len(options) == 0:
                self.logger.notice("Deepgram options are not set")
                options = None

        super().__init__(
            api_key=api_key, url=url, verbose=verbose, headers=headers, options=options
        )
