# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Dict, Union, Optional

import httpx

from ....utils import verboselogs
from ....options import DeepgramClientOptions
from ...abstract_sync_client import AbstractSyncRestClient
from ..errors import DeepgramError, DeepgramTypeError

from .helpers import is_buffer_source, is_readstream_source, is_url_source
from .options import (
    AnalyzeOptions,
    UrlSource,
    FileSource,
)
from .response import AsyncAnalyzeResponse, AnalyzeResponse


class AnalyzeClient(AbstractSyncRestClient):
    """
    A client class for handling text data.
    Provides methods for transcribing text from URLs, files, etc.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config
        super().__init__(config)

    def analyze_url(
        self,
        source: UrlSource,
        options: Optional[Union[AnalyzeOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/read",
    ) -> Union[AnalyzeResponse, AsyncAnalyzeResponse]:
        """
        Analyze text from a URL source.

        Args:
            source (UrlSource): The URL source of the text to ingest.
            options (AnalyzeOptions): Additional options for the ingest (default is None).
            endpoint (str): The API endpoint for the ingest (default is "v1/read").

        Returns:
            AnalyzeResponse: An object containing the result.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("AnalyzeClient.analyze_url ENTER")

        if (
            isinstance(options, dict)
            and "callback" in options
            and options["callback"] is not None
        ) or (isinstance(options, AnalyzeOptions) and options.callback is not None):
            self._logger.debug("AnalyzeClient.analyze_url LEAVE")
            return self.analyze_url_callback(
                source,
                callback=options["callback"],
                options=options,
                addons=addons,
                headers=headers,
                timeout=timeout,
                endpoint=endpoint,
            )

        url = f"{self._config.url}/{endpoint}"
        if is_url_source(source):
            body = source
        else:
            self._logger.error("Unknown transcription source type")
            self._logger.debug("AnalyzeClient.analyze_url LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("AnalyzeClient.analyze_url LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self._logger.info("url: %s", url)
        self._logger.info("source: %s", source)
        if isinstance(options, AnalyzeOptions):
            self._logger.info("AnalyzeOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = self.post(
            url,
            options=options,
            addons=addons,
            headers=headers,
            json=body,
            timeout=timeout,
        )
        self._logger.info("json: %s", result)
        res = AnalyzeResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("analyze_url succeeded")
        self._logger.debug("AnalyzeClient.analyze_url LEAVE")
        return res

    def analyze_url_callback(
        self,
        source: UrlSource,
        callback: str,
        options: Optional[Union[AnalyzeOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/read",
    ) -> AsyncAnalyzeResponse:
        """
        Transcribes audio from a URL source and sends the result to a callback URL.

        Args:
            source (UrlSource): The URL source of the audio to transcribe.
            callback (str): The callback URL where the transcription results will be sent.
            options (AnalyzeOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/read").

        Returns:
            AsyncAnalyzeResponse: An object containing the request_id or an error message.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("AnalyzeClient.analyze_url_callback ENTER")

        url = f"{self._config.url}/{endpoint}"
        if options is None:
            options = {}
        if isinstance(options, AnalyzeOptions):
            options.callback = callback
        else:
            options["callback"] = callback
        if is_url_source(source):
            body = source
        else:
            self._logger.error("Unknown transcription source type")
            self._logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self._logger.info("url: %s", url)
        self._logger.info("source: %s", source)
        if isinstance(options, AnalyzeOptions):
            self._logger.info("AnalyzeOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = self.post(
            url,
            options=options,
            addons=addons,
            headers=headers,
            json=body,
            timeout=timeout,
        )
        self._logger.info("json: %s", result)
        res = AsyncAnalyzeResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("analyze_url_callback succeeded")
        self._logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
        return res

    def analyze_text(
        self,
        source: FileSource,
        options: Optional[Union[AnalyzeOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/read",
    ) -> Union[AnalyzeResponse, AsyncAnalyzeResponse]:
        """
        Analyze text from a local file source.

        Args:
            source (TextSource): The local file source of the text to ingest.
            options (AnalyzeOptions): Additional options for the ingest (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/read").

        Returns:
            AnalyzeResponse: An object containing the transcription result or an error message.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("AnalyzeClient.analyze_text ENTER")

        if (
            isinstance(options, dict)
            and "callback" in options
            and options["callback"] is not None
        ) or (isinstance(options, AnalyzeOptions) and options.callback is not None):
            self._logger.debug("AnalyzeClient.analyze_text LEAVE")
            return self.analyze_text_callback(
                source,
                callback=options["callback"],
                options=options,
                addons=addons,
                headers=headers,
                timeout=timeout,
                endpoint=endpoint,
            )

        url = f"{self._config.url}/{endpoint}"
        if is_buffer_source(source):
            body = source["buffer"]  # type: ignore
        elif is_readstream_source(source):
            body = source["stream"]  # type: ignore
        else:
            self._logger.error("Unknown transcription source type")
            self._logger.debug("AnalyzeClient.analyze_text LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("AnalyzeClient.analyze_text LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self._logger.info("url: %s", url)
        if isinstance(options, AnalyzeOptions):
            self._logger.info("AnalyzeOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = self.post(
            url,
            options=options,
            addons=addons,
            headers=headers,
            content=body,
            timeout=timeout,
        )
        self._logger.info("json: %s", result)
        res = AnalyzeResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("analyze_text succeeded")
        self._logger.debug("AnalyzeClient.analyze_text LEAVE")
        return res

    def analyze_text_callback(
        self,
        source: FileSource,
        callback: str,
        options: Optional[Union[AnalyzeOptions, Dict]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/read",
    ) -> AsyncAnalyzeResponse:
        """
        Transcribes audio from a local file source and sends the result to a callback URL.

        Args:
            source (TextSource): The local file source of the audio to transcribe.
            callback (str): The callback URL where the transcription results will be sent.
            options (AnalyzeOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/read").

        Returns:
            AsyncAnalyzeResponse: An object containing the request_id or an error message.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("AnalyzeClient.analyze_file_callback ENTER")

        url = f"{self._config.url}/{endpoint}"
        if options is None:
            options = {}
        if isinstance(options, AnalyzeOptions):
            options.callback = callback
        else:
            options["callback"] = callback
        if is_buffer_source(source):
            body = source["buffer"]  # type: ignore
        elif is_readstream_source(source):
            body = source["stream"]  # type: ignore
        else:
            self._logger.error("Unknown transcription source type")
            self._logger.debug("AnalyzeClient.analyze_file_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("AnalyzeClient.analyze_file_callback LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self._logger.info("url: %s", url)
        if isinstance(options, AnalyzeOptions):
            self._logger.info("AnalyzeOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        result = self.post(
            url,
            options=options,
            addons=addons,
            headers=headers,
            json=body,
            timeout=timeout,
        )
        self._logger.info("json: %s", result)
        res = AsyncAnalyzeResponse.from_json(result)
        self._logger.verbose("result: %s", res)
        self._logger.notice("analyze_file_callback succeeded")
        self._logger.debug("AnalyzeClient.analyze_file_callback LEAVE")
        return res
