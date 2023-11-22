# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Optional

from .options import DeepgramClientOptions
from .errors import DeepgramApiKeyError

from .clients.listen import ListenClient
from .clients.manage.client import ManageClient # FUTURE VERSIONINING:, ManageClientV1
from .clients.onprem.client import OnPremClient # FUTURE VERSIONINING: , OnPremClientV1

class DeepgramClient:
    """
    Represents a client for interacting with the Deepgram API.

    This class provides a client for making requests to the Deepgram API with various configuration options.

    Attributes:
        api_key (str): The Deepgram API key used for authentication.
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Raises:
        DeepgramApiKeyError: If the API key is missing or invalid.

    Methods:
        listen: Returns a ListenClient instance for interacting with Deepgram's transcription services.
        manage: Returns a ManageClient instance for managing Deepgram resources.
        onprem: Returns an OnPremClient instance for interacting with Deepgram's on-premises API.

    """
    def __init__(self, api_key: str, config: Optional[DeepgramClientOptions] = None):
        if not api_key:
            raise DeepgramApiKeyError("Deepgram API key is required")

        self.api_key = api_key
        if config is None: # Use default configuration
            self.config = DeepgramClientOptions(self.api_key)
        else:
            config.set_apikey(self.api_key)
            self.config = config
    
    @property
    def listen(self):
        return ListenClient(self.config)
    
    @property
    def manage(self):
        return ManageClient(self.config)
    
    # FUTURE VERSIONINING:
    # @property
    # def manage_v1(self):
    #     return ManageClientV1(self.config)
    
    @property
    def onprem(self):
        return OnPremClient(self.config)
    
    # FUTURE VERSIONINING:
    # @property
    # def onprem_v1(self):
    #     return OnPremClientV1(self.config)
