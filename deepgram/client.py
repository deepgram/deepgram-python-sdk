# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional
from importlib import import_module
import os
import logging
import deprecation  # type: ignore

from . import __version__
from .utils import verboselogs

# common
# pylint: disable=unused-import
from .clients import (
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
    UrlSource,
)
from .clients import BaseResponse
from .clients import (
    Average,
    Intent,
    Intents,
    IntentsInfo,
    Segment,
    SentimentInfo,
    Sentiment,
    Sentiments,
    SummaryInfo,
    Topic,
    Topics,
    TopicsInfo,
)
from .clients import (
    ModelInfo,
    Hit,
    Search,
)
from .clients import (
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)
from .clients import (
    DeepgramError,
    DeepgramTypeError,
    DeepgramModuleError,
    DeepgramApiError,
    DeepgramUnknownApiError,
)

# listen client
from .clients import ListenRouter, ReadRouter, SpeakRouter, AgentRouter

# speech-to-text
from .clients import LiveClient, AsyncLiveClient  # backward compat
from .clients import (
    ListenWebSocketClient,
    AsyncListenWebSocketClient,
)
from .clients import (
    ListenWebSocketOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)

# live client responses
from .clients import (
    # top level
    LiveResultResponse,
    ListenWSMetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    # common websocket response
    # OpenResponse,
    # CloseResponse,
    # ErrorResponse,
    # UnhandledResponse,
    # unique
    ListenWSMetadata,
    ListenWSAlternative,
    ListenWSChannel,
    ListenWSWord,
)

# prerecorded
from .clients import (
    # common
    # UrlSource,
    # BufferSource,
    # StreamSource,
    # TextSource,
    # FileSource,
    # unique
    PreRecordedStreamSource,
    PrerecordedSource,
    ListenRestSource,
)

from .clients import (
    PreRecordedClient,
    AsyncPreRecordedClient,
)  # backward compat
from .clients import (
    ListenRESTClient,
    AsyncListenRESTClient,
)
from .clients import (
    ListenRESTOptions,
    PrerecordedOptions,
)

# rest client responses
from .clients import (
    # top level
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
    # shared
    # Average,
    # Intent,
    # Intents,
    # IntentsInfo,
    # Segment,
    # SentimentInfo,
    # Sentiment,
    # Sentiments,
    # SummaryInfo,
    # Topic,
    # Topics,
    # TopicsInfo,
    # between rest and websocket
    # ModelInfo,
    # Alternative,
    # Hit,
    # Search,
    # Channel,
    # Word,
    # unique
    Entity,
    ListenRESTMetadata,
    Paragraph,
    Paragraphs,
    ListenRESTResults,
    Sentence,
    Summaries,
    SummaryV1,
    SummaryV2,
    Translation,
    Utterance,
    Warning,
    ListenRESTAlternative,
    ListenRESTChannel,
    ListenRESTWord,
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
    # top level
    AsyncAnalyzeResponse,
    SyncAnalyzeResponse,
    AnalyzeResponse,
    # shared
    # Average,
    # Intent,
    # Intents,
    # IntentsInfo,
    # Segment,
    # SentimentInfo,
    # Sentiment,
    # Sentiments,
    # SummaryInfo,
    # Topic,
    # Topics,
    # TopicsInfo,
    # unique
    AnalyzeMetadata,
    AnalyzeResults,
    AnalyzeSummary,
)

# speak
# speak REST
from .clients import (
    # top level
    SpeakRESTOptions,
    SpeakOptions,  # backward compat
    # common
    # TextSource,
    # BufferSource,
    # StreamSource,
    # FileSource,
    # unique
    SpeakSource,
    SpeakRestSource,
    SpeakRESTSource,
)

from .clients import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)

from .clients import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

# speak WebSocket
from .clients import SpeakWebSocketEvents, SpeakWebSocketMessage

from .clients import (
    SpeakWSOptions,
)

from .clients import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)

from .clients import (
    # top level
    SpeakWSMetadataResponse,
    FlushedResponse,
    ClearedResponse,
    WarningResponse,
    # common websocket response
    # OpenResponse,
    # CloseResponse,
    # UnhandledResponse,
    # ErrorResponse,
)

# auth client classes
from .clients import AuthRESTClient, AsyncAuthRESTClient

# auth client responses
from .clients import (
    GrantTokenResponse,
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
    # top level
    Message,
    ProjectsResponse,
    ModelResponse,
    ModelsResponse,
    MembersResponse,
    KeyResponse,
    KeysResponse,
    ScopesResponse,
    InvitesResponse,
    UsageRequest,
    UsageResponse,
    UsageRequestsResponse,
    UsageSummaryResponse,
    UsageFieldsResponse,
    BalancesResponse,
    # shared
    Project,
    STTDetails,
    TTSMetadata,
    TTSDetails,
    Member,
    Key,
    Invite,
    Config,
    STTUsageDetails,
    Callback,
    TokenDetail,
    SpeechSegment,
    TTSUsageDetails,
    STTTokens,
    TTSTokens,
    UsageSummaryResults,
    Resolution,
    UsageModel,
    Balance,
)

# on-prem
from .clients import (
    OnPremClient,
    AsyncOnPremClient,
    SelfHostedClient,
    AsyncSelfHostedClient,
)


# agent
from .clients import AgentWebSocketEvents

# websocket
from .clients import (
    AgentWebSocketClient,
    AsyncAgentWebSocketClient,
)

from .clients import (
    # common websocket response
    # OpenResponse,
    # CloseResponse,
    # ErrorResponse,
    # UnhandledResponse,
    # unique
    WelcomeResponse,
    SettingsAppliedResponse,
    ConversationTextResponse,
    UserStartedSpeakingResponse,
    AgentThinkingResponse,
    FunctionCallRequest,
    AgentStartedSpeakingResponse,
    AgentAudioDoneResponse,
    InjectionRefusedResponse,
)

from .clients import (
    # top level
    SettingsOptions,
    UpdatePromptOptions,
    UpdateSpeakOptions,
    InjectAgentMessageOptions,
    InjectUserMessageOptions,
    FunctionCallResponse,
    AgentKeepAlive,
    # sub level
    Listen,
    Speak,
    Header,
    Item,
    Properties,
    Parameters,
    Function,
    Think,
    Provider,
    Agent,
    Input,
    Output,
    Audio,
    Endpoint,
)


# client errors and options
from .options import DeepgramClientOptions, ClientOptionsFromEnv
from .errors import DeepgramApiKeyError

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
        access_token (str): The Deepgram access token used for authentication.
        config_options (DeepgramClientOptions): An optional configuration object specifying client options.

    Raises:
        DeepgramApiKeyError: If both API key and access token are missing or invalid.

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
        access_token: str = "",
    ):
        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())

        # Normalize empty strings to None for consistent handling
        api_key = api_key if api_key else ""
        access_token = access_token if access_token else ""

        # Handle credential extraction from config first
        if api_key == "" and access_token == "" and config is not None:
            self._logger.info(
                "Attempting to set credentials from config object")
            api_key = config.api_key
            access_token = config.access_token

        # Fallback to environment variables if no explicit credentials provided
        # Prioritize access token over API key
        if api_key == "" and access_token == "":
            self._logger.info(
                "Attempting to get credentials from environment variables"
            )
            access_token = os.getenv("DEEPGRAM_ACCESS_TOKEN", "")
            if access_token == "":
                api_key = os.getenv("DEEPGRAM_API_KEY", "")

        # Log warnings for missing credentials
        if api_key == "" and access_token == "":
            self._logger.warning(
                "WARNING: Neither API key nor access token is provided"
            )

        if config is None:  # Use default configuration
            self._config = DeepgramClientOptions(
                api_key=api_key, access_token=access_token
            )
        else:
            # Update config with credentials only if we have valid credentials
            # This ensures empty strings don't overwrite existing config credentials
            # Prioritize API key for backward compatibility
            if api_key and api_key != "":
                config.set_apikey(api_key)
            elif access_token and access_token != "":
                config.set_access_token(access_token)
            self._config = config

        # Store credentials for backward compatibility - extract from final config
        self.api_key = self._config.api_key
        self.access_token = self._config.access_token

    @property
    def listen(self):
        """
        Returns a Listen dot-notation router for interacting with Deepgram's transcription services.
        """
        return ListenRouter(self._config)

    @property
    def read(self):
        """
        Returns a Read dot-notation router for interacting with Deepgram's read services.
        """
        return ReadRouter(self._config)

    @property
    def speak(self):
        """
        Returns a Speak dot-notation router for interacting with Deepgram's speak services.
        """
        return SpeakRouter(self._config)

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
    def auth(self):
        """
        Returns an AuthRESTClient instance for managing short-lived tokens.
        """
        return self.Version(self._config, "auth")

    @property
    def asyncauth(self):
        """
        Returns an AsyncAuthRESTClient instance for managing short-lived tokens.
        """
        return self.Version(self._config, "asyncauth")

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

    @property
    def agent(self):
        """
        Returns a Agent dot-notation router for interacting with Deepgram's speak services.
        """
        return AgentRouter(self._config)

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
                case "auth":
                    parent = "auth"
                    filename = "client"
                    classname = "AuthRESTClient"
                case "asyncauth":
                    parent = "auth"
                    filename = "async_client"
                    classname = "AsyncAuthRESTClient"
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
