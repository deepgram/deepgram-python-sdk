# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import logging, verboselogs

from ...abstract_async_client import AbstractAsyncRestClient
from ..errors import DeepgramTypeError
from ..helpers import is_buffer_source, is_readstream_source, is_url_source
from ..source import UrlSource, FileSource

from .options import PrerecordedOptions
from .response import AsyncPrerecordedResponse, PrerecordedResponse


class AsyncPreRecordedClient(AbstractAsyncRestClient):
    """
    A client class for handling pre-recorded audio data.
    Provides methods for transcribing audio from URLs and files.
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        super().__init__(config)

    """
    Transcribes audio from a URL or FILE source.

    A wrapped for transcribe_url and transcribe_file.
    Please see the documentation for those methods for more information.
    """

    async def transcribe(
        self,
        source: UrlSource,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> PrerecordedResponse:
        if "url" in source:
            return await self.transcribe_url(source, options, addons, endpoint)
        else:
            return await self.transcribe_file(source, options, addons, endpoint)

    """
    Transcribes audio from a URL or FILE source with a Callback.

    A wrapped for transcribe_url_callback and transcribe_file_callback.
    Please see the documentation for those methods for more information.
    """

    async def transcribe_callback(
        self,
        source: UrlSource,
        callback: str,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> AsyncPrerecordedResponse:
        if "url" in source:
            return await self.transcribe_url_callback(
                source, callback, options, addons, endpoint
            )
        else:
            return await self.transcribe_file_callback(
                source, callback, options, addons, endpoint
            )

    """
    Transcribes audio from a URL source.

    Args:
        source (UrlSource): The URL source of the audio to transcribe.
        options (PrerecordedOptions): Additional options for the transcription (default is None).
        endpoint (str): The API endpoint for the transcription (default is "v1/listen").

    Returns:
        PrerecordedResponse: An object containing the transcription result.

    Raises:
        DeepgramTypeError: Raised for known API errors.
    """

    async def transcribe_url(
        self,
        source: UrlSource,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> PrerecordedResponse:
        self.logger.debug("PreRecordedClient.transcribe_url ENTER")

        if options is not None and options.callback is not None:
            self.logger.debug("PreRecordedClient.transcribe_url LEAVE")
            return await self.transcribe_url_callback(
                source, options["callback"], options, addons, endpoint
            )

        url = f"{self.config.url}/{endpoint}"
        if is_url_source(source):
            body = source
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("PreRecordedClient.transcribe_url LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        self.logger.info("url: %s", url)
        self.logger.info("source: %s", source)
        if isinstance(options, PrerecordedOptions):
            self.logger.info("PrerecordedOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, options=options, addons=addons, json=body)
        self.logger.info("json: %s", result)
        res = PrerecordedResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("transcribe_url succeeded")
        self.logger.debug("PreRecordedClient.transcribe_url LEAVE")
        return res

    """
    Transcribes audio from a URL source and sends the result to a callback URL.

    Args:
        source (UrlSource): The URL source of the audio to transcribe.
        callback (str): The callback URL where the transcription results will be sent.
        options (PrerecordedOptions): Additional options for the transcription (default is None).
        endpoint (str): The API endpoint for the transcription (default is "v1/listen").

    Returns:
        AsyncPrerecordedResponse: An object containing the request_id or an error message.

    Raises:
        DeepgramTypeError: Raised for known API errors.
    """

    async def transcribe_url_callback(
        self,
        source: UrlSource,
        callback: str,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> AsyncPrerecordedResponse:
        self.logger.debug("PreRecordedClient.transcribe_url_callback ENTER")

        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = {}
        options["callback"] = callback
        if is_url_source(source):
            body = source
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("PreRecordedClient.transcribe_url_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        self.logger.info("url: %s", url)
        self.logger.info("source: %s", source)
        if isinstance(options, PrerecordedOptions):
            self.logger.info("PrerecordedOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, options=options, addons=addons, json=body)
        self.logger.info("json: %s", result)
        res = AsyncPrerecordedResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("transcribe_url_callback succeeded")
        self.logger.debug("PreRecordedClient.transcribe_url_callback LEAVE")
        return res

    """
    Transcribes audio from a local file source.

    Args:
        source (FileSource): The local file source of the audio to transcribe.
        options (PrerecordedOptions): Additional options for the transcription (default is None).
        endpoint (str): The API endpoint for the transcription (default is "v1/listen").

    Returns:
        PrerecordedResponse: An object containing the transcription result or an error message.

    Raises:
        DeepgramTypeError: Raised for known API errors.
    """

    async def transcribe_file(
        self,
        source: FileSource,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> PrerecordedResponse:
        self.logger.debug("PreRecordedClient.transcribe_file ENTER")

        if options is not None and options.callback is not None:
            self.logger.debug("PreRecordedClient.transcribe_file LEAVE")
            return await self.transcribe_file_callback(
                source, options["callback"], options, addons, endpoint
            )

        url = f"{self.config.url}/{endpoint}"
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("PreRecordedClient.transcribe_file LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        self.logger.info("url: %s", url)
        if isinstance(options, PrerecordedOptions):
            self.logger.info("PrerecordedOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, options=options, addons=addons, content=body)
        self.logger.info("json: %s", result)
        res = PrerecordedResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("transcribe_file succeeded")
        self.logger.debug("PreRecordedClient.transcribe_file LEAVE")
        return res

    """
    Transcribes audio from a local file source and sends the result to a callback URL.

    Args:
        source (FileSource): The local file source of the audio to transcribe.
        callback (str): The callback URL where the transcription results will be sent.
        options (PrerecordedOptions): Additional options for the transcription (default is None).
        endpoint (str): The API endpoint for the transcription (default is "v1/listen").

    Returns:
        AsyncPrerecordedResponse: An object containing the request_id or an error message.

    Raises:
        DeepgramTypeError: Raised for known API errors.
    """

    async def transcribe_file_callback(
        self,
        source: FileSource,
        callback: str,
        options: PrerecordedOptions = None,
        addons: dict = None,
        endpoint: str = "v1/listen",
    ) -> AsyncPrerecordedResponse:
        self.logger.debug("PreRecordedClient.transcribe_file_callback ENTER")

        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = {}
        options["callback"] = callback
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            self.logger.error("Unknown transcription source type")
            self.logger.debug("PreRecordedClient.transcribe_file_callback LEAVE")
            raise DeepgramTypeError("Unknown transcription source type")

        self.logger.info("url: %s", url)
        if isinstance(options, PrerecordedOptions):
            self.logger.info("PrerecordedOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)
        result = await self.post(url, options=options, addons=addons, json=body)
        self.logger.info("json: %s", result)
        res = AsyncPrerecordedResponse.from_json(result)
        self.logger.verbose("result: %s", res)
        self.logger.notice("transcribe_file_callback succeeded")
        self.logger.debug("PreRecordedClient.transcribe_file_callback LEAVE")
        return res
