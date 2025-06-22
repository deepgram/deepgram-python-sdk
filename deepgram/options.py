# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import sys
import re
import os
from typing import Dict, Optional
import logging
import numbers

from deepgram import __version__
from .utils import verboselogs
from .errors import DeepgramApiKeyError


class DeepgramClientOptions:  # pylint: disable=too-many-instance-attributes
    """
    Represents options for configuring a Deepgram client.

    This class allows you to customize various options for interacting with the Deepgram API.

    Attributes:
        api_key: (Optional) A Deepgram API key used for authentication. Default uses the `DEEPGRAM_API_KEY` environment variable.
        access_token: (Optional) A Deepgram access token used for authentication. Default uses the `DEEPGRAM_ACCESS_TOKEN` environment variable.
        url: (Optional) The URL used to interact with production, On-prem, and other Deepgram environments. Defaults to `api.deepgram.com`.
        verbose: (Optional) The logging level for the client. Defaults to `verboselogs.WARNING`.
        headers: (Optional) Headers for initializing the client.
        options: (Optional) Additional options for initializing the client.
    """

    _logger: verboselogs.VerboseLogger
    _inspect_listen: bool = False
    _inspect_speak: bool = False

    def __init__(
        self,
        api_key: str = "",
        access_token: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
    ):  # pylint: disable=too-many-positional-arguments
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())

        if api_key is None:
            api_key = ""
        if access_token is None:
            access_token = ""

        self.verbose = verbose
        self.api_key = api_key
        self.access_token = access_token

        if headers is None:
            headers = {}
        # Store custom headers for preservation during auth updates
        self._custom_headers = headers.copy()
        self._update_headers(headers=headers)

        if len(url) == 0:
            url = "api.deepgram.com"
        self.url = self._get_url(url)

        if options is None:
            options = {}
        self.options = options

        if self.is_auto_flush_reply_enabled():
            self._inspect_listen = True
        if self.is_auto_flush_speak_enabled():
            self._inspect_speak = True

    def set_apikey(self, api_key: str):
        """
        set_apikey: Sets the API key for the client.

        Args:
            api_key: The Deepgram API key used for authentication.
        """
        self.api_key = api_key
        self.access_token = ""  # Clear access token when setting API key
        self._update_headers(headers=getattr(self, '_custom_headers', {}))

    def set_access_token(self, access_token: str):
        """
        set_access_token: Sets the access token for the client.

        Args:
            access_token: The Deepgram access token used for authentication.
        """
        self.access_token = access_token
        self.api_key = ""  # Clear API key when setting access token
        self._update_headers(headers=getattr(self, '_custom_headers', {}))

    def _get_url(self, url) -> str:
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = "https://" + url
        return url.strip("/")

    def _update_headers(self, headers: Optional[Dict] = None):
        # Initialize headers if not already set, otherwise preserve existing custom headers
        if not hasattr(self, 'headers') or self.headers is None:
            self.headers = {}
        else:
            # Preserve existing custom headers but allow auth headers to be updated
            existing_custom_headers = {k: v for k, v in self.headers.items()
                                       if k not in ['Accept', 'Authorization', 'User-Agent']}
            self.headers = existing_custom_headers

        self.headers["Accept"] = "application/json"

        # Set authorization header based on available credentials
        # Prefer api_key over access_token for backward compatibility
        if self.api_key:
            self.headers["Authorization"] = f"Token {self.api_key}"
        elif self.access_token:
            self.headers["Authorization"] = f"Bearer {self.access_token}"

        self.headers[
            "User-Agent"
        ] = f"@deepgram/sdk/{__version__} python/{sys.version_info[1]}.{sys.version_info[2]}"
        # Overwrite / add any headers that were passed in
        if headers:
            self.headers.update(headers)

    def is_keep_alive_enabled(self) -> bool:
        """
        is_keep_alive_enabled: Returns True if the client is configured to keep the connection alive.
        """
        return self.options.get("keepalive", False) or self.options.get(
            "keep_alive", False
        )

    def is_auto_flush_reply_enabled(self) -> bool:
        """
        is_auto_flush_reply_enabled: Returns True if the client is configured to auto-flush for listen.
        """
        auto_flush_reply_delta = float(
            self.options.get("auto_flush_reply_delta", 0))
        return (
            isinstance(auto_flush_reply_delta, numbers.Number)
            and auto_flush_reply_delta > 0
        )

    def is_auto_flush_speak_enabled(self) -> bool:
        """
        is_auto_flush_speak_enabled: Returns True if the client is configured to auto-flush for speak.
        """
        auto_flush_speak_delta = float(
            self.options.get("auto_flush_speak_delta", 0))
        return (
            isinstance(auto_flush_speak_delta, numbers.Number)
            and auto_flush_speak_delta > 0
        )

    def is_inspecting_listen(self) -> bool:
        """
        is_inspecting_listen: Returns True if the client is inspecting listen messages.
        """
        return self._inspect_listen

    def is_inspecting_speak(self) -> bool:
        """
        is_inspecting_speak: Returns True if the client is inspecting speak messages.
        """
        return self._inspect_speak


class ClientOptionsFromEnv(
    DeepgramClientOptions
):  # pylint: disable=too-many-branches, too-many-statements
    """
    This class extends DeepgramClientOptions and will attempt to use environment variables first before defaults.
    """

    _logger: verboselogs.VerboseLogger

    def __init__(
        self,
        api_key: str = "",
        access_token: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict] = None,
        options: Optional[Dict] = None,
    ):  # pylint: disable=too-many-positional-arguments
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(verboselogs.WARNING)  # temporary set for setup

        if api_key is None:
            api_key = ""
        if access_token is None:
            access_token = ""

        # Prioritize API key for backward compatibility, fallback to access token
        # This ensures existing DEEPGRAM_API_KEY users continue working as before
        if api_key == "":
            api_key = os.getenv("DEEPGRAM_API_KEY", "")

        if access_token == "" and api_key == "":
            access_token = os.getenv("DEEPGRAM_ACCESS_TOKEN", "")

        # Require at least one form of authentication
        if api_key == "" and access_token == "":
            self._logger.critical(
                "Neither Deepgram API KEY nor ACCESS TOKEN is set")
            raise DeepgramApiKeyError(
                "Neither Deepgram API KEY nor ACCESS TOKEN is set")

        if url == "":
            url = os.getenv("DEEPGRAM_HOST", "api.deepgram.com")
            self._logger.notice(f"Deepgram host is set to {url}")

        if verbose == verboselogs.WARNING:
            _loglevel = os.getenv("DEEPGRAM_LOGGING", "")
            if _loglevel != "":
                verbose = int(_loglevel)
            if isinstance(verbose, str):
                match verbose:
                    case "NOTSET":
                        self._logger.notice("Logging level is set to NOTSET")
                        verbose = verboselogs.NOTSET
                    case "SPAM":
                        self._logger.notice("Logging level is set to SPAM")
                        verbose = verboselogs.SPAM
                    case "DEBUG":
                        self._logger.notice("Logging level is set to DEBUG")
                        verbose = verboselogs.DEBUG
                    case "VERBOSE":
                        self._logger.notice("Logging level is set to VERBOSE")
                        verbose = verboselogs.VERBOSE
                    case "NOTICE":
                        self._logger.notice("Logging level is set to NOTICE")
                        verbose = verboselogs.NOTICE
                    case "WARNING":
                        self._logger.notice("Logging level is set to WARNING")
                        verbose = verboselogs.WARNING
                    case "SUCCESS":
                        self._logger.notice("Logging level is set to SUCCESS")
                        verbose = verboselogs.SUCCESS
                    case "ERROR":
                        self._logger.notice("Logging level is set to ERROR")
                        verbose = verboselogs.ERROR
                    case "CRITICAL":
                        self._logger.notice("Logging level is set to CRITICAL")
                        verbose = verboselogs.CRITICAL
                    case _:
                        self._logger.notice("Logging level is set to WARNING")
                        verbose = verboselogs.WARNING
        self._logger.notice(f"Logging level is set to {verbose}")

        if headers is None:
            headers = {}
            for x in range(0, 20):
                header = os.getenv(f"DEEPGRAM_HEADER_{x}", None)
                if header is not None:
                    headers[header] = os.getenv(
                        f"DEEPGRAM_HEADER_VALUE_{x}", None)
                    self._logger.debug(
                        "Deepgram header %s is set with value %s",
                        header,
                        headers[header],
                    )
                else:
                    break
            if len(headers) == 0:
                self._logger.notice("Deepgram headers are not set")
                headers = None

        if options is None:
            options = {}
            for x in range(0, 20):
                param = os.getenv(f"DEEPGRAM_PARAM_{x}", None)
                if param is not None:
                    options[param] = os.getenv(
                        f"DEEPGRAM_PARAM_VALUE_{x}", None)
                    self._logger.debug(
                        "Deepgram option %s is set with value %s", param, options[param]
                    )
                else:
                    break
            if len(options) == 0:
                self._logger.notice("Deepgram options are not set")
                options = None

        super().__init__(
            api_key=api_key, access_token=access_token, url=url, verbose=verbose, headers=headers, options=options
        )
