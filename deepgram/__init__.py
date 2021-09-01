from ._types import Options
from .keys import Keys
from .transcription import Transcription
from .projects import Projects
from .usage import Usage
from typing import Union


class Deepgram:
    """
    The Deepgram API client.

    The client provides all the transcription, usage, key management, and project management
    facilities. For example, to transcribe a pre-recorded file using the default API endpoint
    of api.deepgram.com:

    .. code-block::

        import asyncio
        import json
        import deepgram

        async def main():
            client = deepgram.Deepgram("your api key")
            with open ("path/to/file.wav", "rb") as audio:
                source = {"buffer": audio, "mimetype": "audio/wav"}
                options = {"punctuate": True}
                response = client.transcription.prerecorded(source, options)
                print(json.dumps(response, indent=4))

        asyncio.run(main())

    To use a self-hosted Deepgram API, specify the URL when then creating the client:

    .. code-block::

        client = deepgram.Deepgram({"api_key": "your api key", "api_url": "https://your.endpoint.com/"})

    For details on transcription methods, refer to :class:`deepgram.transcription.Transcription`

    Args:
        options: The client configuration :class:`Options` or the Deepgram API key as a string.

    Raises:
        ValueError: If the Deepgram API URL is invalid or if the API key is missing.
    """
    def __init__(self, options: Union[str, Options]) -> None:
        if 'api_url' in options and not options.get('api_url'):
            raise ValueError("DG: API URL must be valid or omitted")
        t_options: Options = {'api_key': options} if isinstance(options, str) else options 
        if 'api_key' not in t_options:
            raise ValueError("DG: API key is required")
        self.options = t_options

    @property
    def keys(self) -> Keys:
        return Keys(self.options)

    @property
    def transcription(self) -> Transcription:
        return Transcription(self.options)

    @property
    def projects(self) -> Projects:
        return Projects(self.options)

    @property
    def usage(self) -> Usage:
        return Usage(self.options)

__all__ = [Deepgram]