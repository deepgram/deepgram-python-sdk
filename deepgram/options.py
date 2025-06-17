# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import sys
import re
import os
from typing import Dict, Optional, Any
import logging
import numbers

from deepgram import __version__
from .utils import verboselogs
from .errors import DeepgramApiKeyError


class DeepgramClientOptions:
    """
    Represents options for configuring a Deepgram client.
    """

    _logger: verboselogs.VerboseLogger
    _inspect_listen: bool = False
    _inspect_speak: bool = False

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict[str, str]] = None,
        options: Optional[Dict[str, Any]] = None,
    ):
        self._logger = verboselogs.VerboseLogger(__name__)
        if not self._logger.hasHandlers():
            self._logger.addHandler(logging.StreamHandler())

        self.verbose = verbose
        self.api_key = api_key or ""

        self._update_headers(headers or {})

        self.url = self._get_url(url or "api.deepgram.com")

        self.options = options or {}

        self._inspect_listen = self.is_auto_flush_reply_enabled()
        self._inspect_speak = self.is_auto_flush_speak_enabled()

    def set_apikey(self, api_key: str) -> None:
        """
        Sets the API key for the client.
        """
        self.api_key = api_key
        self._update_headers()

    def _get_url(self, url: str) -> str:
        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = f"https://{url}"
        return url.rstrip("/")

    def _update_headers(self, headers: Optional[Dict[str, str]] = None) -> None:
        self.headers: Dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": f"@deepgram/sdk/{__version__} python/{sys.version_info[1]}.{sys.version_info[2]}"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Token {self.api_key}"
        if headers:
            self.headers.update(headers)

    def is_keep_alive_enabled(self) -> bool:
        """
        Returns True if the client is configured to keep the connection alive.
        """
        return self.options.get("keepalive", False) or self.options.get("keep_alive", False)

    def is_auto_flush_reply_enabled(self) -> bool:
        """
        Returns True if the client is configured to auto-flush for listen.
        """
        try:
            auto_flush_reply_delta = float(self.options.get("auto_flush_reply_delta", 0))
        except (TypeError, ValueError):
            auto_flush_reply_delta = 0
        return auto_flush_reply_delta > 0

    def is_auto_flush_speak_enabled(self) -> bool:
        """
        Returns True if the client is configured to auto-flush for speak.
        """
        try:
            auto_flush_speak_delta = float(self.options.get("auto_flush_speak_delta", 0))
        except (TypeError, ValueError):
            auto_flush_speak_delta = 0
        return auto_flush_speak_delta > 0

    def is_inspecting_listen(self) -> bool:
        """
        Returns True if the client is inspecting listen messages.
        """
        return self._inspect_listen

    def is_inspecting_speak(self) -> bool:
        """
        Returns True if the client is inspecting speak messages.
        """
        return self._inspect_speak


class ClientOptionsFromEnv(DeepgramClientOptions):
    """
    Extends DeepgramClientOptions and will attempt to use environment variables first before defaults.
    """

    _logger: verboselogs.VerboseLogger

    def __init__(
        self,
        api_key: str = "",
        url: str = "",
        verbose: int = verboselogs.WARNING,
        headers: Optional[Dict[str, str]] = None,
        options: Optional[Dict[str, Any]] = None,
    ):
        self._logger = verboselogs.VerboseLogger(__name__)
        if not self._logger.hasHandlers():
            self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(verboselogs.WARNING)

        api_key = api_key or os.getenv("DEEPGRAM_API_KEY", "")
        if not api_key:
            self._logger.critical("Deepgram API KEY is not set")
            raise DeepgramApiKeyError("Deepgram API KEY is not set")

        url = url or os.getenv("DEEPGRAM_HOST", "api.deepgram.com")
        self._logger.notice(f"Deepgram host is set to {url}")

        if verbose == verboselogs.WARNING:
            _loglevel = os.getenv("DEEPGRAM_LOGGING", "")
            if _loglevel:
                try:
                    verbose = int(_loglevel)
                except ValueError:
                    verbose = getattr(verboselogs, _loglevel.upper(), verboselogs.WARNING)
            self._logger.notice(f"Logging level is set to {verbose}")

        if headers is None:
            headers = {
                os.getenv(f"DEEPGRAM_HEADER_{i}"): os.getenv(f"DEEPGRAM_HEADER_VALUE_{i}")
                for i in range(20)
                if os.getenv(f"DEEPGRAM_HEADER_{i}") is not None
            }
            if not headers:
                self._logger.notice("Deepgram headers are not set")
                headers = None
            else:
                for k, v in headers.items():
                    self._logger.debug(f"Deepgram header {k} is set with value {v}")

        if options is None:
            options = {
                os.getenv(f"DEEPGRAM_PARAM_{i}"): os.getenv(f"DEEPGRAM_PARAM_VALUE_{i}")
                for i in range(20)
                if os.getenv(f"DEEPGRAM_PARAM_{i}") is not None
            }
            if not options:
                self._logger.notice("Deepgram options are not set")
                options = None
            else:
                for k, v in options.items():
                    self._logger.debug(f"Deepgram option {k} is set with value {v}")

        super().__init__(
            api_key=api_key, url=url, verbose=verbose, headers=headers, options=options
        )
