from ...errors import DeepgramError
from ..abstract_restful_client import AbstractRestfulClient

from .helpers import is_buffer_source, is_readstream_source, is_url_source
from .prerecorded_source import UrlSource, FileSource
from .transcription_options import PrerecordedOptions
from .prerecorded_response import AsyncPrerecordedResponse, SyncPrerecordedResponse


class PreRecordedClient(AbstractRestfulClient):
    """
    A client class for handling pre-recorded audio data. Provides methods for transcribing audio from URLs and files.
    """

    def __init__(self, url, headers):
        """
        Initializes a new instance of the PreRecordedClient.

        Args:
            url (str): The URL for API requests.
            headers (dict): Headers to include in API requests.
        """
        self.url = url
        self.headers = headers
        super().__init__(url, headers)

    async def transcribe_url(
        self, source: UrlSource, options: PrerecordedOptions = None, endpoint: str = "v1/listen"
    ) -> SyncPrerecordedResponse:
        """
        Transcribes audio from a URL source.

        Args:
            source (UrlSource): The URL source of the audio to transcribe.
            options (PrerecordedOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/listen").

        Returns:
            SyncPrerecordedResponse: An object containing the transcription result.

        Raises:
            DeepgramError: If the "callback" option is provided for a synchronous transcription.
            DeepgramError: If the source type is unknown.
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            DeepgramUnknownError: Raised for unexpected errors not specific to the API.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.url}/{endpoint}"
        if options is not None and "callback" in options:
            raise DeepgramError(
                "Callback cannot be provided as an option to a synchronous transcription. Use `transcribe_url_callback` instead.")
        if is_url_source(source):
            body = source
        else:
            raise DeepgramError("Unknown transcription source type")
        return await self.post(url, options, json=body)

    async def transcribe_url_callback(self, source: UrlSource, callback: str, options: PrerecordedOptions = None, endpoint: str = "v1/listen") -> AsyncPrerecordedResponse:
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
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            DeepgramUnknownError: Raised for unexpected errors not specific to the API.
            Exception: For any other unexpected exceptions.
        """
        url = f"{self.url}/{endpoint}"
        if options is None:
            options = {}
        options['callback'] = callback
        if is_url_source(source):
            body = source
        else:
            raise DeepgramError("Unknown transcription source type")
        return await self.post(url, options, json=body)

    async def transcribe_file(self, source: FileSource, options: PrerecordedOptions = None, endpoint: str = "v1/listen") -> SyncPrerecordedResponse:
        """
        Transcribes audio from a local file source.

        Args:
            source (FileSource): The local file source of the audio to transcribe.
            options (PrerecordedOptions): Additional options for the transcription (default is None).
            endpoint (str): The API endpoint for the transcription (default is "v1/listen").

        Returns:
            SyncPrerecordedResponse: An object containing the transcription result or an error message.

        Raises:
            DeepgramError: If the "callback" option is provided for a synchronous transcription.
            DeepgramError: If the source type is unknown.
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            DeepgramUnknownError: Raised for unexpected errors not specific to the API.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.url}/{endpoint}"
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            raise DeepgramError("Unknown transcription source type")
        return await self.post(url, options, content=body)

    async def transcribe_file_callback(self, source: FileSource, callback: str, options: PrerecordedOptions = None, endpoint: str = "v1/listen") -> AsyncPrerecordedResponse:
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
            DeepgramError: If the source type is unknown.
            DeepgramApiError: Raised for known API errors.
            DeepgramUnknownApiError: Raised for unknown API errors.
            DeepgramUnknownError: Raised for unexpected errors not specific to the API.
            Exception: For any other unexpected exceptions.
        """

        url = f"{self.url}/{endpoint}"
        if options is None:
            options = {}
        options['callback'] = callback
        if is_buffer_source(source):
            body = source["buffer"]
        elif is_readstream_source(source):
            body = source["stream"]
        else:
            raise DeepgramError("Unknown transcription source type")
        return await self.post(url, options, content=body)
