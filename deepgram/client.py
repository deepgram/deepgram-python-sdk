# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional
from importlib import import_module
import os

import deprecation

from . import __version__
import logging
from .utils import verboselogs

# common
# pylint: disable=unused-import
from .clients import (
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
    UrlSource,
    Sentiment,
)

# listen client
from .clients import Listen, Read, Speak

# live
from .clients import LiveClient, AsyncLiveClient
from .clients import (
    LiveOptions,
    LiveTranscriptionEvents,
)

# live client responses
from .clients import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)

# prerecorded
from .clients import (
    PreRecordedClient,
    AsyncPreRecordedClient,
)
from .clients import (
    PrerecordedOptions,
    PreRecordedStreamSource,
    PrerecordedSource,
)

# prerecorded client responses
from .clients import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# read
from .clients import ReadClient, AsyncReadClient
from .clients import AnalyzeClient, AsyncAnalyzeClient
from .clients import (
    AnalyzeOptions,
    AnalyzeStreamSource,
    AnalyzeSource,
)

# read client responses
from .clients import (
    AsyncAnalyzeResponse,
    AnalyzeResponse,
    SyncAnalyzeResponse,
)

# speak
from .clients import (
    SpeakOptions,
    FileSource,
    SpeakWebSocketSource,
    SpeakSource,
)
from .clients import SpeakWebSocketEvents

## speak REST
from .clients import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)

from .clients import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

## speak WebSocket
from .clients import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
)
from .clients import (
    SpeakWebSocketResponse,
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
)

# manage client classes/input
from .clients import ManageClient, AsyncManageClient
from .clients import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)

# manage client responses
from .clients import (
    Message,
    Project,
    ProjectsResponse,
    MembersResponse,
    Key,
    KeyResponse,
    KeysResponse,
    ScopesResponse,
    InvitesResponse,
    UsageRequest,
    UsageRequestsResponse,
    UsageSummaryResponse,
    UsageFieldsResponse,
    Balance,
    BalancesResponse,
)

# on-prem
from .clients import (
    OnPremClient,
    AsyncOnPremClient,
    SelfHostedClient,
    AsyncSelfHostedClient,
)

# client errors and options
from .options import DeepgramClientOptions, ClientOptionsFromEnv
from .errors import DeepgramApiKeyError, DeepgramModuleError

# pylint: enable=unused-import


class Deepgram:  # pylint: disable=broad-exception-raised
    """
    The Deepgram class is no longer a class in version 3 of this SDK.
    """

    def __init__(self, *anything):
        raise Exception(
            """
            FATAL ERROR:
            You are attempting to instantiate a Deepgram object, which is no longer a class in version 3 of this SDK.

            To fix this issue:
                1. You need to revert to the previous version 2 of the SDK: pip install deepgram-sdk==2.12.0
                2. or, update your application's code to use version 3 of this SDK. See the README for more information.

            Things to consider:

                - This Version 3 of the SDK requires Python 3.10 or higher.
                  Older versions (3.9 and lower) of Python are nearing end-of-life: https://devguide.python.org/versions/
                  Understand the risks of using a version of Python nearing EOL.

                - Version 2 of the SDK will receive maintenance updates in the form of security fixes only.
                  No new features will be added to version 2 of the SDK.
            """
        )


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

        manage: (Preferred) Returns a Threaded ManageClient instance for managing Deepgram resources.
        selfhosted: (Preferred) Returns an Threaded SelfHostedClient instance for interacting with Deepgram's on-premises API.

        asyncmanage: Returns an (Async) ManageClient instance for managing Deepgram resources.
        asyncselfhosted: Returns an (Async) SelfHostedClient instance for interacting with Deepgram's on-premises API.
    """

    _config: DeepgramClientOptions
    _logger: verboselogs.VerboseLogger

    def __init__(
        self,
        api_key: str = "",
        config: Optional[DeepgramClientOptions] = None,
    ):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())

        if api_key == "" and config is not None:
            self._logger.info("Attempting to set API key from config object")
            api_key = config.api_key
        if api_key == "":
            self._logger.info("Attempting to set API key from environment variable")
            api_key = os.getenv("DEEPGRAM_API_KEY", "")
        if api_key == "":
            self._logger.warning("WARNING: API key is missing")

        self.api_key = api_key
        if config is None:  # Use default configuration
            self._config = DeepgramClientOptions(self.api_key)
        else:
            config.set_apikey(self.api_key)
            self._config = config

    @property
    def listen(self):
        """
        Returns a ListenClient instance for interacting with Deepgram's transcription services.
        """
        return Listen(self._config)

    @property
    def read(self):
        """
        Returns a ReadClient instance for interacting with Deepgram's read services.
        """
        return Read(self._config)

    @property
    def speak(self):
        """
        Returns a SpeakClient instance for interacting with Deepgram's speak services.
        """
        return Speak(self._config)

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.asyncspeak is deprecated. Use deepgram.speak.asyncrest instead.",
    )
    def asyncspeak(self):
        """
        DEPRECATED: deepgram.asyncspeak is deprecated. Use deepgram.speak.asyncrest instead.
        """
        return self.Version(self._config, "asyncspeak")

    @property
    def manage(self):
        """
        Returns a ManageClient instance for managing Deepgram resources.
        """
        return self.Version(self._config, "manage")

    @property
    def asyncmanage(self):
        """
        Returns an AsyncManageClient instance for managing Deepgram resources.
        """
        return self.Version(self._config, "asyncmanage")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.onprem is deprecated. Use deepgram.speak.selfhosted instead.",
    )
    def onprem(self):
        """
        DEPRECATED: deepgram.onprem is deprecated. Use deepgram.speak.selfhosted instead.
        """
        return self.Version(self._config, "selfhosted")

    @property
    def selfhosted(self):
        """
        Returns an SelfHostedClient instance for interacting with Deepgram's on-premises API.
        """
        return self.Version(self._config, "selfhosted")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.asynconprem is deprecated. Use deepgram.speak.asyncselfhosted instead.",
    )
    def asynconprem(self):
        """
        DEPRECATED: deepgram.asynconprem is deprecated. Use deepgram.speak.asyncselfhosted instead.
        """
        return self.Version(self._config, "asyncselfhosted")

    @property
    def asyncselfhosted(self):
        """
        Returns an AsyncSelfHostedClient instance for interacting with Deepgram's on-premises API.
        """
        return self.Version(self._config, "asyncselfhosted")

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
        #         case "manage":
        #             return ManageClient(self._config)
        #         case "selfhosted":
        #             return SelfHostedClient(self._config)
        #         case _:
        #             raise DeepgramModuleError("Invalid parent")

        def v(self, version: str = ""):
            # pylint: disable-msg=too-many-statements
            """
            Returns a client for the specified version of the API.
            """
            self._logger.debug("Version.v ENTER")
            self._logger.info("version: %s", version)
            if len(version) == 0:
                self._logger.error("version is empty")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Invalid module version")

            parent = ""
            filename = ""
            classname = ""
            match self._parent:
                case "manage":
                    parent = "manage"
                    filename = "client"
                    classname = "ManageClient"
                case "asyncmanage":
                    parent = "manage"
                    filename = "async_client"
                    classname = "AsyncManageClient"
                case "asyncspeak":
                    return AsyncSpeakRESTClient(self._config)
                case "selfhosted":
                    parent = "selfhosted"
                    filename = "client"
                    classname = "SelfHostedClient"
                case "asyncselfhosted":
                    parent = "selfhosted"
                    filename = "async_client"
                    classname = "AsyncSelfHostedClient"
                case _:
                    self._logger.error("parent unknown: %s", self._parent)
                    self._logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.{parent}.v{version}.{filename}"
            self._logger.info("path: %s", path)
            self._logger.info("classname: %s", classname)

            # import class
            mod = import_module(path)
            if mod is None:
                self._logger.error("module path is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, classname)
            if my_class is None:
                self._logger.error("my_class is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find class")

            # instantiate class
            my_class_instance = my_class(self._config)
            self._logger.notice("Version.v succeeded")
            self._logger.debug("Version.v LEAVE")
            return my_class_instance

        # pylint: enable-msg=too-many-statements
