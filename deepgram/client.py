import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Optional

from .options import DeepgramClientOptions
from .errors import DeepgramError

from .clients.listen import ListenClient
from .clients.manage.client import ManageClient
from .clients.onprem.client import OnPremClient

class DeepgramClient:
    """
    Represents a client for interacting with the Deepgram API.

    This class provides a client for making requests to the Deepgram API with various configuration options.

    Attributes:
        api_key (str): The Deepgram API key used for authentication.
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Raises:
        DeepgramError: If the API key is missing or invalid.

    Methods:
        listen: Returns a ListenClient instance for interacting with Deepgram's transcription services.
        manage: Returns a ManageClient instance for managing Deepgram resources.
        onprem: Returns an OnPremClient instance for interacting with Deepgram's on-premises API.

    """
    def __init__(self, api_key: str, config_options: Optional[DeepgramClientOptions] = None):
        if not api_key:
            raise DeepgramError("Deepgram API key is required")

        self.api_key = api_key
        
        """
        This block is responsible for determining the client's configuration options and headers based on the provided or default settings.
        """

        if config_options is None: # Use default configuration
            self.config_options = DeepgramClientOptions(self.api_key).global_options
            self.headers = DeepgramClientOptions(self.api_key).global_options['headers']
        else: # Use custom configuration
            self.config_options = config_options['global_options']
            if config_options['global_options'].get('headers'):
                self.headers = {**config_options['global_options']['headers'], **DeepgramClientOptions(self.api_key).global_options['headers']}
            else:
                self.headers = DeepgramClientOptions(self.api_key).global_options['headers']
        self.url = self._get_url(self.config_options)

    def _get_url(self, config_options):
        url = config_options['url']
        if not re.match(r'^https?://', url, re.IGNORECASE):
            url = 'https://' + url
        return url.strip('/')
    
    @property
    def listen(self):
        return ListenClient(self.url, self.api_key, self.headers)
    
    @property
    def manage(self):
        return ManageClient(self.url, self.headers)
    
    @property
    def onprem(self):
        return OnPremClient(self.url, self.headers)
