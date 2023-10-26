from .prerecorded_client import PreRecordedClient
from .live_client import LiveClient
from typing import Dict, Any, Optional


class ListenClient:
    def __init__(self, url: str, api_key: str, headers: Optional[Dict[str, Any]]):
        self.url = url
        self.api_key = api_key
        self.headers = headers
    print('hey')

    @property
    def prerecorded(self):
        return PreRecordedClient(self.url, self.headers)

    @property
    def live(self):
        return LiveClient(self.url, self.api_key, self.headers)
