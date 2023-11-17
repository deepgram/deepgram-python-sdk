# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .errors import DeepgramTypeError
from ..abstract_client import AbstractRestfulClient

from .helpers import is_buffer_source, is_readstream_source, is_url_source
from .source import UrlSource, FileSource
from .v1_options import PrerecordedOptionsV1
from .v1_response import AsyncPrerecordedResponseV1, PrerecordedResponseV1

class PreRecordedClientV1(AbstractRestfulClient):
    """
    A client class for handling pre-recorded audio data. Provides methods for transcribing audio from URLs and files.
    """
    def __init__(self, config):
        """
        Initializes a new instance of the PreRecordedClient.

        Args:
            config (DeepgramClientOptions): all the options for the client.
        """
        self.config = config
        super().__init__(config)
    
    async def transcribe_url(
        self, source: UrlSource, options: PrerecordedOptionsV1 = None, endpoint: str="v1/listen"
    ) -> PrerecordedResponseV1:
        """
        Transcribes audio from a URL source.

        Args:
            source (UrlSource): The URL source of the audio to transcribe.
            options (PrerecordedOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/listen").

        Returns:
            SyncPrerecordedResponse: An object containing the transcription result.

        Raises:
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.config.url}/{endpoint}"
        if options is not None and "callback" in options:
            return await self.transcribe_url_callback(source, options["callback"], options, endpoint)
        if is_url_source(source):
            body = source
        else:
            raise DeepgramTypeError("Unknown transcription source type")
        return await self.post(url, options, json=body)
        
    async def transcribe_url_callback( self, source: UrlSource, callback:str, options: PrerecordedOptionsV1 = None, endpoint: str="v1/listen") -> AsyncPrerecordedResponseV1:
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
            DeepgramError: If the "callback" option is provided for a synchronous transcription.
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            Exception: For any other unexpected exceptions.
        """
        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = {}
        options['callback'] = callback
        if is_url_source(source):
            body = source
        else:
            raise DeepgramTypeError("Unknown transcription source type")
        return await self.post(url, options, json=body)

    
    async def transcribe_file(self, source: FileSource, options: PrerecordedOptionsV1=None, endpoint: str = "v1/listen") -> PrerecordedResponseV1:
        """
        Transcribes audio from a local file source.

        Args:
            source (FileSource): The local file source of the audio to transcribe.
            options (PrerecordedOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/listen").

        Returns:
            SyncPrerecordedResponse: An object containing the transcription result or an error message.

        Raises:

            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.config.url}/{endpoint}"
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            raise DeepgramTypeError("Unknown transcription source type")
        return await self.post(url, options, content=body)

    async def transcribe_file_callback(self, source: FileSource, callback:str, options: PrerecordedOptionsV1 = None, endpoint: str="v1/listen") -> AsyncPrerecordedResponseV1:
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
            DeepgramError: If the "callback" option is provided for a synchronous transcription.
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.config.url}/{endpoint}"
        if options is None:
            options = {}
        options['callback'] = callback
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            raise DeepgramTypeError("Unknown transcription source type")
        return await self.post(url, options, content=body)
