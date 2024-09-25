# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import Dict, Union, Optional, cast
import io

import httpx

import deprecation  # type: ignore
from ..... import __version__

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ....common import AbstractSyncRestClient
from ....common import DeepgramError, DeepgramTypeError
from .helpers import is_text_source

from .options import SpeakRESTOptions, FileSource
from .response import SpeakRESTResponse


class SpeakRESTClient(AbstractSyncRestClient):
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

    # pylint: disable=too-many-positional-arguments

    def stream_raw(
        self,
        source: FileSource,
        options: Optional[Union[Dict, SpeakRESTOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
        **kwargs,
    ) -> httpx.Response:
        """
        Speak from a text source and store as a Iterator[byte].

        Args:
            source (TextSource): The text source to speak.
            options (SpeakRESTOptions): Additional options for the ingest (default is None).
            addons (Dict): Additional options for the request (default is None).
            headers (Dict): Additional headers for the request (default is None).
            timeout (httpx.Timeout): The timeout for the request (default is None).
            endpoint (str): The endpoint to use for the request (default is "v1/speak").

        Returns:
            httpx.Response: The direct httpx.Response object from the speak request.
            For more information, see https://www.python-httpx.org/api/#response

            IMPORTANT: The response object's `close()` method should be called when done
            in order to prevent connection leaks.

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

        if isinstance(options, SpeakRESTOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("SpeakClient.stream LEAVE")
            raise DeepgramError("Fatal speak options error")

        self._logger.info("url: %s", url)
        self._logger.info("source: %s", source)
        if isinstance(options, SpeakRESTOptions):
            self._logger.info("SpeakRESTOptions switching class -> dict")
            options = options.to_dict()
        self._logger.info("options: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)

        result = self.post_raw(
            url,
            options=options,
            addons=addons,
            headers=headers,
            json=body,
            timeout=timeout,
            **kwargs,
        )

        self._logger.info("result: %s", str(result))
        self._logger.notice("speak succeeded")
        self._logger.debug("SpeakClient.stream LEAVE")
        return result

    def stream_memory(
        self,
        source: FileSource,
        options: Optional[Union[Dict, SpeakRESTOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
        **kwargs,
    ) -> SpeakRESTResponse:
        """
        Speak from a text source and store in memory.

        Args:
            source (TextSource): The text source to speak.
            options (SpeakRESTOptions): Additional options for the ingest (default is None).
            addons (Dict): Additional options for the request (default is None).
            headers (Dict): Additional headers for the request (default is None).
            timeout (httpx.Timeout): The timeout for the request (default is None).
            endpoint (str): The endpoint to use for the request (default is "v1/speak").

        Returns:
            SpeakRESTResponse: The response from the speak request.

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

        if isinstance(options, SpeakRESTOptions) and not options.check():
            self._logger.error("options.check failed")
            self._logger.debug("SpeakClient.stream LEAVE")
            raise DeepgramError("Fatal speak options error")

        self._logger.info("url: %s", url)
        self._logger.info("source: %s", source)
        if isinstance(options, SpeakRESTOptions):
            self._logger.info("SpeakRESTOptions switching class -> dict")
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
        result = self.post_memory(
            url,
            options=options,
            addons=addons,
            headers=headers,
            json=body,
            timeout=timeout,
            file_result=return_vals,
            **kwargs,
        )

        self._logger.info("result: %s", result)
        resp = SpeakRESTResponse(
            content_type=str(result["content-type"]),
            request_id=str(result["request-id"]),
            model_uuid=str(result["model-uuid"]),
            model_name=str(result["model-name"]),
            characters=int(str(result["char-count"])),
            transfer_encoding=str(result["transfer-encoding"]),
            date=str(result["date"]),
            stream=cast(io.BytesIO, result["stream"]),
            stream_memory=cast(io.BytesIO, result["stream"]),
        )
        self._logger.verbose("resp Object: %s", resp)
        self._logger.notice("speak succeeded")
        self._logger.debug("SpeakClient.stream LEAVE")
        return resp

    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="SpeakRESTClient.stream is deprecated. Use SpeakRESTClient.stream_memory instead.",
    )
    def stream(
        self,
        source: FileSource,
        options: Optional[Union[Dict, SpeakRESTOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
        **kwargs,
    ) -> SpeakRESTResponse:
        """
        DEPRECATED: stream() is deprecated. Use stream_memory() instead.
        """
        return self.stream_memory(
            source,
            options=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            endpoint=endpoint,
            **kwargs,
        )

    async def file(
        self,
        filename: str,
        source: FileSource,
        options: Optional[Union[Dict, SpeakRESTOptions]] = None,
        addons: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
        **kwargs,
    ) -> SpeakRESTResponse:
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
            **kwargs,
        )

    def save(
        self,
        filename: str,
        source: FileSource,
        options: Optional[Union[Dict, SpeakRESTOptions]] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        endpoint: str = "v1/speak",
        **kwargs,
    ) -> SpeakRESTResponse:
        """
        Speak from a text source and save to a file.

        Args:
            source (TextSource): The text source to speak.
            options (SpeakRESTOptions): Additional options for the ingest (default is None).
            addons (Dict): Additional options for the request (default is None).
            headers (Dict): Additional headers for the request (default is None).
            timeout (httpx.Timeout): The timeout for the request (default is None).
            endpoint (str): The endpoint to use for the request (default is "v1/speak").

        Returns:
            SpeakRESTResponse: The response from the speak request.

        Raises:
            DeepgramTypeError: Raised for known API errors.
        """
        self._logger.debug("SpeakClient.save ENTER")

        res = self.stream_memory(
            source,
            options=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            endpoint=endpoint,
            **kwargs,
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

    # pylint: enable=too-many-positional-arguments
