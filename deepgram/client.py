# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional
from importlib import import_module
import logging, verboselogs
import os

# listen client
from .clients import Listen, Read

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
    ErrorResponse,
    CloseResponse,
)

# prerecorded
from .clients import PreRecordedClient, AsyncPreRecordedClient
from .clients import (
    FileSource,
    PrerecordedSource,
    UrlSource,
    BufferSource,
    ReadStreamSource,
    PrerecordedOptions,
    Sentiment,
)

# prerecorded client responses
from .clients import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# analyze
from .clients import AnalyzeClient, AsyncAnalyzeClient
from .clients import (
    AnalyzeSource,
    TextSource,
    UrlSource,
    BufferSource,
    AnalyzeStreamSource,
    AnalyzeOptions,
    Sentiment,
)

# read client responses
from .clients import (
    AsyncAnalyzeResponse,
    AnalyzeResponse,
    SyncAnalyzeResponse,
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
from .clients.onprem.client import OnPremClient
from .clients.onprem.v1.async_client import AsyncOnPremClient

from .options import DeepgramClientOptions, ClientOptionsFromEnv
from .errors import DeepgramApiKeyError, DeepgramModuleError


class Deepgram:
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
        onprem: (Preferred) Returns an Threaded OnPremClient instance for interacting with Deepgram's on-premises API.

        asyncmanage: Returns an (Async) ManageClient instance for managing Deepgram resources.
        asynconprem: Returns an (Async) OnPremClient instance for interacting with Deepgram's on-premises API.
    """

    def __init__(
        self,
        api_key: str = "",
        config: Optional[DeepgramClientOptions] = None,
    ):
        verboselogs.install()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

        if api_key == "" and config is not None:
            self.logger.info("Attempting to set API key from config object")
            api_key = config.api_key
        if api_key == "":
            self.logger.info("Attempting to set API key from environment variable")
            api_key = os.getenv("DEEPGRAM_API_KEY", "")
        if api_key == "":
            self.logger.warning("WARNING: API key is missing")

        self.api_key = api_key
        if config is None:  # Use default configuration
            self.config = DeepgramClientOptions(self.api_key)
        else:
            config.set_apikey(self.api_key)
            self.config = config

    @property
    def listen(self):
        return Listen(self.config)

    @property
    def read(self):
        return Read(self.config)

    @property
    def manage(self):
        return self.Version(self.config, "manage")

    @property
    def asyncmanage(self):
        return self.Version(self.config, "asyncmanage")

    @property
    def onprem(self):
        return self.Version(self.config, "onprem")

    @property
    def asynconprem(self):
        return self.Version(self.config, "asynconprem")

    # INTERNAL CLASSES
    class Version:
        def __init__(self, config, parent: str):
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(config.verbose)
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
            self.logger.debug("Version.v ENTER")
            self.logger.info("version: %s", version)
            if len(version) == 0:
                self.logger.error("version is empty")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Invalid module version")

            parent = ""
            fileName = ""
            className = ""
            match self.parent:
                case "manage":
                    parent = "manage"
                    fileName = "client"
                    className = "ManageClient"
                case "asyncmanage":
                    parent = "manage"
                    fileName = "async_client"
                    className = "AsyncManageClient"
                case "onprem":
                    parent = "onprem"
                    fileName = "client"
                    className = "OnPremClient"
                case "asynconprem":
                    parent = "onprem"
                    fileName = "async_client"
                    className = "AsyncOnPremClient"
                case _:
                    self.logger.error("parent unknown: %s", self.parent)
                    self.logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            # create class path
            path = f"deepgram.clients.{parent}.v{version}.{fileName}"
            self.logger.info("path: %s", path)
            self.logger.info("className: %s", className)

            # import class
            mod = import_module(path)
            if mod is None:
                self.logger.error("module path is None")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, className)
            if my_class is None:
                self.logger.error("my_class is None")
                self.logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find class")

            # instantiate class
            myClass = my_class(self.config)
            self.logger.notice("Version.v succeeded")
            self.logger.debug("Version.v LEAVE")
            return myClass
