# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from importlib import import_module
import logging
import deprecation  # type: ignore

from .. import __version__
from .listen.v1 import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    LiveClient,
    AsyncLiveClient,
)
from ..utils import verboselogs
from ..options import DeepgramClientOptions
from .errors import DeepgramModuleError


class ListenRouter:
    """
    Represents a client for interacting with the Deepgram API.

    This class provides a client for making requests to the Deepgram API with various configuration options.

    Attributes:
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Raises:
        DeepgramApiKeyError: If the API key is missing or invalid.

    Methods:
        live: (Preferred) Returns a Threaded LiveClient instance for interacting with Deepgram's transcription services.
        prerecorded: (Preferred) Returns an Threaded PreRecordedClient instance for interacting with Deepgram's prerecorded transcription services.

        asynclive: Returns an (Async) LiveClient instance for interacting with Deepgram's transcription services.
        asyncprerecorded: Returns an (Async) PreRecordedClient instance for interacting with Deepgram's prerecorded transcription services.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)
        self._config = config

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.listen.prerecorded is deprecated. Use deepgram.listen.rest instead.",
    )
    def prerecorded(self):
        """
        DEPRECATED: deepgram.listen.prerecorded is deprecated. Use deepgram.listen.rest instead.
        """
        return self.Version(self._config, "prerecorded")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.listen.asyncprerecorded is deprecated. Use deepgram.listen.asyncrest instead.",
    )
    def asyncprerecorded(self):
        """
        DEPRECATED: deepgram.listen.asyncprerecorded is deprecated. Use deepgram.listen.asyncrest instead.
        """
        return self.Version(self._config, "asyncprerecorded")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.listen.live is deprecated. Use deepgram.listen.websocket instead.",
    )
    def live(self):
        """
        DEPRECATED: deepgram.listen.live is deprecated. Use deepgram.listen.websocket instead.
        """
        return self.Version(self._config, "live")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.listen.asynclive is deprecated. Use deepgram.listen.asyncwebsocket instead.",
    )
    def asynclive(self):
        """
        DEPRECATED: deepgram.listen.asynclive is deprecated. Use deepgram.listen.asyncwebsocket instead.
        """
        return self.Version(self._config, "asynclive")

    @property
    def rest(self):
        """
        Returns a ListenRESTClient instance for interacting with Deepgram's prerecorded transcription services.
        """
        return self.Version(self._config, "rest")

    @property
    def asyncrest(self):
        """
        Returns an AsyncListenRESTClient instance for interacting with Deepgram's prerecorded transcription services.
        """
        return self.Version(self._config, "asyncrest")

    @property
    def websocket(self):
        """
        Returns a ListenWebSocketClient instance for interacting with Deepgram's transcription services.
        """
        return self.Version(self._config, "websocket")

    @property
    def asyncwebsocket(self):
        """
        Returns an AsyncListenWebSocketClient instance for interacting with Deepgram's transcription services.
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

            protocol = ""
            file_name = ""
            class_name = ""
            match self._parent:
                case "live":
                    return LiveClient(self._config)
                case "asynclive":
                    return AsyncLiveClient(self._config)
                case "prerecorded":
                    return PreRecordedClient(self._config)
                case "asyncprerecorded":
                    return AsyncPreRecordedClient(self._config)
                case "websocket":
                    protocol = "websocket"
                    file_name = "client"
                    class_name = "ListenWebSocketClient"
                case "asyncwebsocket":
                    protocol = "websocket"
                    file_name = "async_client"
                    class_name = "AsyncListenWebSocketClient"
                case "rest":
                    protocol = "rest"
                    file_name = "client"
                    class_name = "ListenRESTClient"
                case "asyncrest":
                    protocol = "rest"
                    file_name = "async_client"
                    class_name = "AsyncListenRESTClient"
                case _:
                    self._logger.error("parent unknown: %s", self._parent)
                    self._logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.listen.v{version}.{protocol}.{file_name}"
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
