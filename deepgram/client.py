# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional
from importlib import import_module

from .clients.listen import ListenClient
from .clients.manage.client import ManageClient
from .clients.onprem.client import OnPremClient

from .options import DeepgramClientOptions
from .errors import DeepgramApiKeyError, DeepgramModuleError

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
        return self.Version(self.config, "manage")
    
    @property
    def onprem(self):
        return self.Version(self.config, "onprem")

    # INTERNAL CLASSES
    class Version:
        def __init__(self, config, parent : str):
            self.config = config
            self.parent = parent

        # FUTURE VERSIONING:
        # When v2 or v1.1beta1 or etc. This allows easy access to the latest version of the API.
        # @property
        # def latest(self):
        #     match self.parent:
        #         case "manage":
        #             return ManageClient(self.config)
        #         case "onprem":
        #             return OnPremClient(self.config)
        #         case _:
        #             raise DeepgramModuleError("Invalid parent")

        def v(self, version: str = ""):
            # print(f"version: {version}")
            if len(version) == 0:
                raise DeepgramModuleError("Invalid module version")

            className = ""
            match self.parent:
                case "manage":
                    className = "ManageClient"
                case "onprem":
                    className = "OnPremClient"
                case _:
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.{self.parent}.v{version}.client"
            # print(f"path: {path}")
            # print(f"className: {className}")

            # import class
            mod = import_module(path)
            if mod is None:
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, className)
            if my_class is None:
                raise DeepgramModuleError("Unable to find class")

            # instantiate class
            myClass = my_class(self.config)
            return myClass
