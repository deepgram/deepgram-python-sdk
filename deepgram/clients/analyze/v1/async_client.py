# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs
import json
from typing import Dict, Union

from ...abstract_async_client import AbstractAsyncRestClient
from ..errors import DeepgramError, DeepgramTypeError
from .helpers import is_buffer_source, is_readstream_source, is_url_source
from ..enums import Sentiment

from .options import (
    AnalyzeOptions,
    UrlSource,
    BufferSource,
    StreamSource,
    TextSource,
    AnalyzeSource,
)
from .response import AsyncAnalyzeResponse, AnalyzeResponse


class AsyncAnalyzeClient(AbstractAsyncRestClient):
    """
    A client class for handling text data.
    Provides methods for transcribing text from URLs and files.
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        super().__init__(config)

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

    async def analyze_url(
        self,
        source: UrlSource,
        options: Union[AnalyzeOptions, Dict] = None,
        addons: Dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/read",
    ) -> AnalyzeResponse:
        self.logger.debug("AsyncAnalyzeClient.analyze_url ENTER")

        if options is not None and options["callback"] is not None:
            self.logger.debug("AsyncAnalyzeClient.analyze_url LEAVE")
            return await self.analyze_url_callback(
                source, options["callback"], options, addons, timeout, endpoint
            )

        url = f"{self.config.url}/{endpoint}"
        if is_url_source(source):
            body = source
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("AsyncAnalyzeClient.analyze_url LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncAnalyzeClient.analyze_url LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self.logger.info("url: %s", url)
        self.logger.info("source: %s", source)
        if isinstance(options, AnalyzeOptions):
            self.logger.info("AnalyzeOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(
            url, options=options, addons=addons, json=body, timeout=timeout
        )
        self.logger.info("json: %s", result)
        res = AnalyzeResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("analyze_url succeeded")
        self.logger.debug("AsyncAnalyzeClient.analyze_url LEAVE")
        return res

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

    async def analyze_url_callback(
        self,
        source: UrlSource,
        callback: str,
        options: Union[AnalyzeOptions, Dict] = None,
        addons: Dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/read",
    ) -> AsyncAnalyzeResponse:
        self.logger.debug("AnalyzeClient.analyze_url_callback ENTER")

        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = dict()
        if isinstance(options, AnalyzeOptions):
            options.callback = callback
        else:
            options["callback"] = callback
        if is_url_source(source):
            body = source
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self.logger.info("url: %s", url)
        self.logger.info("source: %s", source)
        if isinstance(options, AnalyzeOptions):
            self.logger.info("AnalyzeOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(
            url, options=options, addons=addons, json=body, timeout=timeout
        )
        self.logger.info("json: %s", result)
        res = AsyncAnalyzeResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("analyze_url_callback succeeded")
        self.logger.debug("AnalyzeClient.analyze_url_callback LEAVE")
        return res

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

    async def analyze_text(
        self,
        source: TextSource,
        options: Union[AnalyzeOptions, Dict] = None,
        addons: Dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/read",
    ) -> AnalyzeResponse:
        self.logger.debug("AsyncAnalyzeClient.analyze_text ENTER")

        if options is not None and options["callback"] is not None:
            self.logger.debug("AsyncAnalyzeClient.analyze_text LEAVE")
            return await self.analyze_text_callback(
                source, options["callback"], options, addons, timeout, endpoint
            )

        url = f"{self.config.url}/{endpoint}"
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("AsyncAnalyzeClient.analyze_text LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncAnalyzeClient.analyze_text LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self.logger.info("url: %s", url)
        if isinstance(options, AnalyzeOptions):
            self.logger.info("AnalyzeOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(
            url, options=options, addons=addons, content=body, timeout=timeout
        )
        self.logger.info("json: %s", result)
        res = AnalyzeResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("analyze_text succeeded")
        self.logger.debug("AsyncAnalyzeClient.analyze_text LEAVE")
        return res

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

    async def analyze_text_callback(
        self,
        source: TextSource,
        callback: str,
        options: Union[AnalyzeOptions, Dict] = None,
        addons: Dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/read",
    ) -> AsyncAnalyzeResponse:
        self.logger.debug("AnalyzeClient.analyze_text_callback ENTER")

        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = dict()
        if isinstance(options, AnalyzeOptions):
            options.callback = callback
        else:
            options["callback"] = callback
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("AnalyzeClient.analyze_text_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        if isinstance(options, AnalyzeOptions) and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AnalyzeClient.analyze_text_callback LEAVE")
            raise DeepgramError("Fatal transcription options error")

        self.logger.info("url: %s", url)
        if isinstance(options, AnalyzeOptions):
            self.logger.info("AnalyzeOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(
            url, options=options, addons=addons, json=body, timeout=timeout
        )
        self.logger.info("json: %s", result)
        res = AsyncAnalyzeResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("analyze_text_callback succeeded")
        self.logger.debug("AnalyzeClient.analyze_text_callback LEAVE")
        return res
