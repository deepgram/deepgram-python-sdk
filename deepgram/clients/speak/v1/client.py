# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Dict, Union, Optional, cast
import io

import httpx

from deepgram.utils import verboselogs
from ....options import DeepgramClientOptions
from ...abstract_sync_client import AbstractSyncRestClient
from ..errors import DeepgramError, DeepgramTypeError
from .helpers import is_text_source

from .options import SpeakOptions, FileSource
from .response import SpeakResponse


class SpeakClient(AbstractSyncRestClient):
    """
    A client class for doing Text-to-Speech.
    Provides methods for speaking from text.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config
        super().__init__(config)

    def stream(
        self,
        source: FileSource,
        options: Optional[Union[Dict, SpeakOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        """
        Speak from a text source and store in memory.

        Args:
            source (TextSource): The text source to speak.
            options (SpeakOptions): Additional options for the ingest (default is None).
            addons (Dict): Additional options for the request (default is None).
            headers (Dict): Additional headers for the request (default is None).
            timeout (httpx.Timeout): The timeout for the request (default is None).
            endpoint (str): The endpoint to use for the request (default is "v1/speak").

        Returns:
            SpeakResponse: The response from the speak request.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("SpeakClient.stream ENTER")

        url = f"{self._config.url}/{endpoint}"
        if is_text_source(source):
            body = source
        else:
            self._logger.error("Unknown speak source type")
            self._logger.debug("SpeakClient.stream LEAVE")
            raise DeepgramTypeError("Unknown speak source type")

        if isinstance(options, SpeakOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("SpeakClient.stream LEAVE")
            raise DeepgramError("Fatal speak options error")

        self._logger.info("url: %s", url)
        self._logger.info("source: %s", source)
        if isinstance(options, SpeakOptions):
            self._logger.info("SpeakOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)

        return_vals = [
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
            file_result=return_vals,
        )

        self._logger.info("result: %s", result)
        resp = SpeakResponse(
            content_type=str(result["content-type"]),
            request_id=str(result["request-id"]),
            model_uuid=str(result["model-uuid"]),
            model_name=str(result["model-name"]),
            characters=int(str(result["char-count"])),
            transfer_encoding=str(result["transfer-encoding"]),
            date=str(result["date"]),
            stream=cast(io.BytesIO, result["stream"]),
        )
        self._logger.verbose("result: %s", resp)
        self._logger.notice("speak succeeded")
        self._logger.debug("SpeakClient.stream LEAVE")
        return resp

    async def file(
        self,
        filename: str,
        source: FileSource,
        options: Optional[Union[Dict, SpeakOptions]] = None,
        addons: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        """
        Speak from a text source and save to a file.
        """
        return self.save(
            filename,
            source,
            options=options,
            addons=addons,
            timeout=timeout,
            endpoint=endpoint,
        )

    def save(
        self,
        filename: str,
        source: FileSource,
        options: Optional[Union[Dict, SpeakOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
    ) -> SpeakResponse:
        """
        Speak from a text source and save to a file.

        Args:
            source (TextSource): The text source to speak.
            options (SpeakOptions): Additional options for the ingest (default is None).
            addons (Dict): Additional options for the request (default is None).
            headers (Dict): Additional headers for the request (default is None).
            timeout (httpx.Timeout): The timeout for the request (default is None).
            endpoint (str): The endpoint to use for the request (default is "v1/speak").

        Returns:
            SpeakResponse: The response from the speak request.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("SpeakClient.save ENTER")

        res = self.stream(
            source,
            options=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            endpoint=endpoint,
        )

        if res.stream is None:
            self._logger.error("stream is None")
            self._logger.debug("SpeakClient.save LEAVE")
            raise DeepgramError("BytesIO stream is None")

        # save to file
        with open(filename, "wb+") as file:
            file.write(res.stream.getbuffer())
            file.flush()

        # add filename to response
        res.stream = None
        res.filename = filename

        self._logger.debug("SpeakClient.save LEAVE")
        return res
