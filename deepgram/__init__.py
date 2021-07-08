from ._types import Options
from .keys import Keys
from .transcription import Transcription
from .projects import Projects
from .usage import Usage
from typing import Union

class Deepgram:
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