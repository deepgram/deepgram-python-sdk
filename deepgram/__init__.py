from typing import Union
from ._types import Options
from .keys import Keys
from .transcription import Transcription
from .transcription_ import Transcription as Transcription_
from .projects import Projects
from .usage import Usage
from .billing import Billing
from .members import Members
from .scopes import Scopes
from .invitations import Invitations


class Deepgram:
    def __init__(self, options: Union[str, Options]) -> None:
        if not isinstance(options, str) and not options.get('api_url'):
            raise ValueError("DG: API URL must be valid or omitted")
        t_options: Options = {
            'api_key': options
        } if isinstance(options, str) else options
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
    def transcription_(self) -> Transcription_:
        return Transcription_(self.options)

    @property
    def projects(self) -> Projects:
        return Projects(self.options)

    @property
    def usage(self) -> Usage:
        return Usage(self.options)

    @property
    def billing(self) -> Billing:
        return Billing(self.options)

    @property
    def members(self) -> Members:
        return Members(self.options)

    @property
    def scopes(self) -> Scopes:
        return Scopes(self.options)

    @property
    def invitations(self) -> Invitations:
        return Invitations(self.options)



__all__ = ["Deepgram"]
