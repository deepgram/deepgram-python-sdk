# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from importlib import import_module
import logging

from deepgram.utils import verboselogs
from ..options import DeepgramClientOptions
from .errors import DeepgramModuleError


class Read:
    """
    Represents a client for interacting with the Deepgram API.

    This class provides a client for making requests to the Deepgram API with various configuration options.

    Attributes:
        api_key (str): The Deepgram API key used for authentication.
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Raises:
        DeepgramApiKeyError: If the API key is missing or invalid.

    Methods:
        read: (Preferred) Returns an Threaded AnalyzeClient instance for interacting with Deepgram's read transcription services.
        asyncread: Returns an (Async) AnalyzeClient instance for interacting with Deepgram's read transcription services.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config

    @property
    def analyze(self):
        """
        Returns an AnalyzeClient instance for interacting with Deepgram's read transcription services.
        """
        return self.Version(self._config, "analyze")

    @property
    def asyncanalyze(self):
        """
        Returns an AsyncAnalyzeClient instance for interacting with Deepgram's read transcription services.
        """
        return self.Version(self._config, "asyncanalyze")

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
        #         case "analyze":
        #             return AnalyzeClient(self._config)
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

            parent = ""
            file_name = ""
            class_name = ""
            match self._parent:
                case "analyze":
                    parent = "analyze"
                    file_name = "client"
                    class_name = "AnalyzeClient"
                case "asyncanalyze":
                    parent = "analyze"
                    file_name = "async_client"
                    class_name = "AsyncAnalyzeClient"
                case _:
                    self._logger.error("parent unknown: %s", self._parent)
                    self._logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.{parent}.v{version}.{file_name}"
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
