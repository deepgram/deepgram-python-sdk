# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs
import json
import aiofiles

from ...abstract_async_client import AbstractAsyncRestClient
from ..errors import DeepgramError, DeepgramTypeError
from ..helpers import is_text_source
from ..source import SpeakSource, TextSource

from .options import SpeakOptions
from .response import SpeakResponse


class AsyncSpeakClient(AbstractAsyncRestClient):
    """
    A client class for doing Text-to-Speech.
    Provides methods for speaking from text.
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)
        self.config = config
        super().__init__(config)

    """
    Speak from a text source.

    Args:
        source (TextSource): The text source to speak.
        options (SpeakOptions): Additional options for the ingest (default is None).
        endpoint (str): The API endpoint for the ingest (default is "v1/speak").

    Returns:
        SpeakResponse: The response from the speak request.

    Raises:
        DeepgramTypeError: Raised for known API errors.
    """

    async def stream(
        self,
        source: TextSource,
        options: SpeakOptions = None,
        addons: dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/speak",
    ):
        self.logger.debug("AsyncSpeakClient.stream ENTER")

        url = f"{self.config.url}/{endpoint}"
        if is_text_source(source):
            body = source
        else:
            self.logger.error("Unknown speak source type")
            self.logger.debug("AsyncSpeakClient.stream LEAVE")
            raise DeepgramTypeError("Unknown speak source type")

        if options is not None and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("AsyncSpeakClient.stream LEAVE")
            raise DeepgramError("Fatal speak options error")

        self.logger.info("url: %s", url)
        self.logger.info("source: %s", source)
        if isinstance(options, SpeakOptions):
            self.logger.info("SpeakOptions switching class -> json")
            options = json.loads(options.to_json())
        self.logger.info("options: %s", options)
        self.logger.info("addons: %s", addons)

        returnVals = [
            "content-type",
            "request-id",
            "model-uuid",
            "model-name",
            "char-count",
            "transfer-encoding",
            "date",
        ]
        result = await self.post(
            url,
            options=options,
            addons=addons,
            json=body,
            timeout=timeout,
            file_result=returnVals,
        )
        self.logger.info("result: %s", result)
        sResp = SpeakResponse(
            content_type=result["content-type"],
            request_id=result["request-id"],
            model_uuid=result["model-uuid"],
            model_name=result["model-name"],
            characters=result["char-count"],
            transfer_encoding=result["transfer-encoding"],
            date=result["date"],
            stream=result["stream"],
        )

        self.logger.verbose("result: %s", sResp)
        self.logger.notice("speak succeeded")
        self.logger.debug("AsyncSpeakClient.stream LEAVE")
        return sResp

    async def save(
        self,
        filename: str,
        source: TextSource,
        options: SpeakOptions = None,
        addons: dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        self.logger.debug("AsyncSpeakClient.save ENTER")

        res = await self.stream(source, options, addons, timeout, endpoint)

        # save to file
        async with aiofiles.open(filename, "wb") as out:
            await out.write(res.stream)
            await out.flush()

        # add filename to response
        res.stream = None
        res.filename = filename

        self.logger.debug("AsyncSpeakClient.save LEAVE")
        return res
