# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs
import json
from typing import Dict, Union, Optional

from ...abstract_sync_client import AbstractSyncRestClient
from ..errors import DeepgramError, DeepgramTypeError
from .helpers import is_text_source

from .options import SpeakOptions, SpeakSource, TextSource, SpeakStreamSource
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
        source: SpeakSource,
        options: Optional[Union[Dict, SpeakOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
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

        if isinstance(options, SpeakOptions) and not options.check():
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
        self.logger.info("headers: %s", headers)

        returnVals = [
            "content-type",
            "request-id",
            "model-uuid",
            "model-name",
            "char-count",
            "transfer-encoding",
            "date",
        ]
        result = self.post_file(
            url,
            options=options,
            addons=addons,
            headers=headers,
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
        self.logger.debug("SpeakClient.stream LEAVE")
        return sResp

    def save(
        self,
        filename: str,
        source: SpeakSource,
        options: Optional[Union[Dict, SpeakOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        self.logger.debug("SpeakClient.save ENTER")

        res = self.stream(
            source,
            options=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            endpoint=endpoint,
        )

        # save to file
        file = open(filename, "wb+")
        file.write(res.stream.getbuffer())
        file.flush()
        file.close()

        # add filename to response
        res.stream = None
        res.filename = filename

        self.logger.debug("SpeakClient.save LEAVE")
        return res
