# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs
import json

from ...abstract_sync_client import AbstractSyncRestClient
from ..errors import DeepgramError, DeepgramTypeError
from ..helpers import is_text_source
from ..source import SpeakSource, TextSource

from .options import SpeakOptions
from .response import SpeakResponse


class SpeakClient(AbstractSyncRestClient):
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

    def stream(
        self,
        source: TextSource,
        options: SpeakOptions = None,
        addons: dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        self.logger.debug("SpeakClient.stream ENTER")

        url = f"{self.config.url}/{endpoint}"
        if is_text_source(source):
            body = source
        else:
            self.logger.error("Unknown speak source type")
            self.logger.debug("SpeakClient.stream LEAVE")
            raise DeepgramTypeError("Unknown speak source type")

        if options is not None and not options.check():
            self.logger.error("options.check failed")
            self.logger.debug("SpeakClient.stream LEAVE")
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
            "x-dg-request-id",
            "x-dg-model-uuid",
            "x-dg-model-name",
            "x-dg-characters",
            "transfer-encoding",
            "date",
        ]
        result = self.post(
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
            request_id=result["x-dg-request-id"],
            model_uuid=result["x-dg-model-uuid"],
            model_name=result["x-dg-model-name"],
            characters=result["x-dg-characters"],
            transfer_encoding=result["transfer-encoding"],
            date=result["date"],
            stream=result["stream"],
        )
        self.logger.verbose("result: %s", sResp)
        self.logger.notice("speak succeeded")
        self.logger.debug("SpeakClient.stream LEAVE")
        return sResp

    def save(
        self,
        filename: str,
        source: TextSource,
        options: SpeakOptions = None,
        addons: dict = None,
        timeout: httpx.Timeout = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        self.logger.debug("SpeakClient.save ENTER")

        res = self.stream(source, options, addons, timeout, endpoint)

        # save to file
        file = open(filename, "wb+")
        file.write(res.stream)
        file.flush()
        file.close()

        # add filename to response
        res.stream = None
        res.filename = filename

        self.logger.debug("SpeakClient.save LEAVE")
        return res
