# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from importlib import import_module
import logging

from .speak.v1.rest.client import SpeakRESTClient
from ..utils import verboselogs
from ..options import DeepgramClientOptions
from .errors import DeepgramModuleError


class Speak:
    """
    This class provides a Speak Clients for making requests to the Deepgram API with various configuration options.

    Attributes:
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Methods:
        rest: (Preferred) Returns a Threaded REST Client instance for interacting with Deepgram's transcription services.
        websocket: (Preferred) Returns an Threaded WebSocket Client instance for interacting with Deepgram's prerecorded transcription services.

        asyncrest: Returns an Async REST Client instance for interacting with Deepgram's transcription services.
        asyncwebsocket: Returns an Async WebSocket Client instance for interacting with Deepgram's prerecorded transcription services.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config

    # TODO: legacy
    def v(self, version: str = ""):
        """
        TODO: legacy
        """
        return SpeakRESTClient(self._config)

    @property
    def rest(self):
        """
        Returns a Threaded REST Client instance for interacting with Deepgram's prerecorded Text-to-Speech services.
        """
        return self.Version(self._config, "rest")

    @property
    def asyncrest(self):
        """
        Returns an Async REST Client instance for interacting with Deepgram's prerecorded Text-to-Speech services.
        """
        return self.Version(self._config, "asyncrest")

    @property
    def websocket(self):
        """
        Returns a Threaded WebSocket Client instance for interacting with Deepgram's Text-to-Speech services.
        """
        return self.Version(self._config, "websocket")

    @property
    def asyncwebsocket(self):
        """
        Returns an Async WebSocket Client instance for interacting with Deepgram's Text-to-Speech services.
        """
        return self.Version(self._config, "asyncwebsocket")

    # INTERNAL CLASSES
    class Version:
        """
        Represents a version of the Deepgram API.
        """

        _logger: verboselogs.VerboseLogger
        _config: DeepgramClientOptions
        _parent: str

        def __init__(self, config, parent: str):
            self._logger = verboselogs.VerboseLogger(__name__)
            self._logger.addHandler(logging.StreamHandler())
            self._logger.setLevel(config.verbose)
            self._config = config
            self._parent = parent

        # FUTURE VERSIONING:
        # When v2 or v1.1beta1 or etc. This allows easy access to the latest version of the API.
        # @property
        # def latest(self):
        #     match self._parent:
        #         case "live":
        #             return LiveClient(self._config)
        #         case "prerecorded":
        #             return PreRecordedClient(self._config)
        #         case _:
        #             raise DeepgramModuleError("Invalid parent")

        def v(self, version: str = ""):
            """
            Returns a specific version of the Deepgram API.
            """
            self._logger.debug("Version.v ENTER")
            self._logger.info("version: %s", version)
            if len(version) == 0:
                self._logger.error("version is empty")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Invalid module version")

            type = ""
            file_name = ""
            class_name = ""
            match self._parent:
                case "websocket":
                    type = "websocket"
                    file_name = "client"
                    class_name = "SpeakWebSocketClient"
                case "asyncwebsocket":
                    type = "websocket"
                    file_name = "async_client"
                    class_name = "AsyncSpeakWebSocketClient"
                case "rest":
                    type = "rest"
                    file_name = "client"
                    class_name = "SpeakRESTClient"
                case "asyncrest":
                    type = "rest"
                    file_name = "async_client"
                    class_name = "AsyncSpeakRESTClient"
                case _:
                    self._logger.error("parent unknown: %s", self._parent)
                    self._logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.speak.v{version}.{type}.{file_name}"
            self._logger.info("path: %s", path)
            self._logger.info("class_name: %s", class_name)

            # import class
            mod = import_module(path)
            if mod is None:
                self._logger.error("module path is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, class_name)
            if my_class is None:
                self._logger.error("my_class is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find class")

            # instantiate class
            my_class = my_class(self._config)
            self._logger.notice("Version.v succeeded")
            self._logger.debug("Version.v LEAVE")
            return my_class
