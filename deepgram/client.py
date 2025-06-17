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

from .clients import (
    TextSource, BufferSource, StreamSource, FileSource, UrlSource,
    BaseResponse,
    Average, Intent, Intents, IntentsInfo, Segment, SentimentInfo, Sentiment, Sentiments, SummaryInfo, Topic, Topics, TopicsInfo,
    ModelInfo, Hit, Search,
    OpenResponse, CloseResponse, UnhandledResponse, ErrorResponse,
    DeepgramError, DeepgramTypeError, DeepgramModuleError, DeepgramApiError, DeepgramUnknownApiError,
    ListenRouter, ReadRouter, SpeakRouter, AgentRouter,
    LiveClient, AsyncLiveClient, ListenWebSocketClient, AsyncListenWebSocketClient, ListenWebSocketOptions, LiveOptions, LiveTranscriptionEvents,
    LiveResultResponse, ListenWSMetadataResponse, SpeechStartedResponse, UtteranceEndResponse,
    ListenWSMetadata, ListenWSAlternative, ListenWSChannel, ListenWSWord,
    PreRecordedStreamSource, PrerecordedSource, ListenRestSource,
    PreRecordedClient, AsyncPreRecordedClient, ListenRESTClient, AsyncListenRESTClient,
    ListenRESTOptions, PrerecordedOptions,
    AsyncPrerecordedResponse, PrerecordedResponse, SyncPrerecordedResponse,
    Entity, ListenRESTMetadata, Paragraph, Paragraphs, ListenRESTResults, Sentence, Summaries, SummaryV1, SummaryV2, Translation, Utterance, Warning,
    ListenRESTAlternative, ListenRESTChannel, ListenRESTWord,
    ReadClient, AsyncReadClient, AnalyzeClient, AsyncAnalyzeClient, AnalyzeOptions, AnalyzeStreamSource, AnalyzeSource,
    AsyncAnalyzeResponse, SyncAnalyzeResponse, AnalyzeResponse, AnalyzeMetadata, AnalyzeResults, AnalyzeSummary,
    SpeakRESTOptions, SpeakOptions, SpeakSource, SpeakRestSource, SpeakRESTSource,
    SpeakClient, SpeakRESTClient, AsyncSpeakRESTClient,
    SpeakResponse, SpeakRESTResponse,
    SpeakWebSocketEvents, SpeakWebSocketMessage, SpeakWSOptions,
    SpeakWebSocketClient, AsyncSpeakWebSocketClient, SpeakWSClient, AsyncSpeakWSClient,
    SpeakWSMetadataResponse, FlushedResponse, ClearedResponse, WarningResponse,
    AuthRESTClient, AsyncAuthRESTClient, GrantTokenResponse,
    ManageClient, AsyncManageClient, ProjectOptions, KeyOptions, ScopeOptions, InviteOptions, UsageRequestOptions, UsageSummaryOptions, UsageFieldsOptions,
    Message, ProjectsResponse, ModelResponse, ModelsResponse, MembersResponse, KeyResponse, KeysResponse, ScopesResponse, InvitesResponse, UsageRequest,
    UsageResponse, UsageRequestsResponse, UsageSummaryResponse, UsageFieldsResponse, BalancesResponse,
    Project, STTDetails, TTSMetadata, TTSDetails, Member, Key, Invite, Config, STTUsageDetails, Callback, TokenDetail, SpeechSegment, TTSUsageDetails,
    STTTokens, TTSTokens, UsageSummaryResults, Resolution, UsageModel, Balance,
    OnPremClient, AsyncOnPremClient, SelfHostedClient, AsyncSelfHostedClient,
    AgentWebSocketEvents, AgentWebSocketClient, AsyncAgentWebSocketClient,
    WelcomeResponse, SettingsAppliedResponse, ConversationTextResponse, UserStartedSpeakingResponse, AgentThinkingResponse, FunctionCallRequest,
    AgentStartedSpeakingResponse, AgentAudioDoneResponse, InjectionRefusedResponse,
    SettingsOptions, UpdatePromptOptions, UpdateSpeakOptions, InjectAgentMessageOptions, FunctionCallResponse, AgentKeepAlive,
    Listen, Speak, Header, Item, Properties, Parameters, Function, Think, Provider, Agent, Input, Output, Audio, Endpoint,
)

from .options import DeepgramClientOptions, ClientOptionsFromEnv
from .errors import DeepgramApiKeyError


class Deepgram:
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

        if not api_key and config is not None:
            self._logger.info("Attempting to set API key from config object")
            api_key = config.api_key
        if not api_key:
            self._logger.info("Attempting to set API key from environment variable")
            api_key = os.getenv("DEEPGRAM_API_KEY", "")
        if not api_key:
            self._logger.warning("WARNING: API key is missing")

        self.api_key = api_key
        if config is None:
            self._config = DeepgramClientOptions(self.api_key)
        else:
            config.set_apikey(self.api_key)
            self._config = config

    @property
    def listen(self):
        """Returns a Listen dot-notation router for interacting with Deepgram's transcription services."""
        return ListenRouter(self._config)

    @property
    def read(self):
        """Returns a Read dot-notation router for interacting with Deepgram's read services."""
        return ReadRouter(self._config)

    @property
    def speak(self):
        """Returns a Speak dot-notation router for interacting with Deepgram's speak services."""
        return SpeakRouter(self._config)

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.asyncspeak is deprecated. Use deepgram.speak.asyncrest instead.",
    )
    def asyncspeak(self):
        """DEPRECATED: deepgram.asyncspeak is deprecated. Use deepgram.speak.asyncrest instead."""
        return self.Version(self._config, "asyncspeak")

    @property
    def manage(self):
        """Returns a ManageClient instance for managing Deepgram resources."""
        return self.Version(self._config, "manage")

    @property
    def asyncmanage(self):
        """Returns an AsyncManageClient instance for managing Deepgram resources."""
        return self.Version(self._config, "asyncmanage")

    @property
    def auth(self):
        """Returns an AuthRESTClient instance for managing short-lived tokens."""
        return self.Version(self._config, "auth")

    @property
    def asyncauth(self):
        """Returns an AsyncAuthRESTClient instance for managing short-lived tokens."""
        return self.Version(self._config, "asyncauth")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.onprem is deprecated. Use deepgram.speak.selfhosted instead.",
    )
    def onprem(self):
        """DEPRECATED: deepgram.onprem is deprecated. Use deepgram.speak.selfhosted instead."""
        return self.Version(self._config, "selfhosted")

    @property
    def selfhosted(self):
        """Returns an SelfHostedClient instance for interacting with Deepgram's on-premises API."""
        return self.Version(self._config, "selfhosted")

    @property
    @deprecation.deprecated(
        deprecated_in="3.4.0",
        removed_in="4.0.0",
        current_version=__version__,
        details="deepgram.asynconprem is deprecated. Use deepgram.speak.asyncselfhosted instead.",
    )
    def asynconprem(self):
        """DEPRECATED: deepgram.asynconprem is deprecated. Use deepgram.speak.asyncselfhosted instead."""
        return self.Version(self._config, "asyncselfhosted")

    @property
    def asyncselfhosted(self):
        """Returns an AsyncSelfHostedClient instance for interacting with Deepgram's on-premises API."""
        return self.Version(self._config, "asyncselfhosted")

    @property
    def agent(self):
        """Returns a Agent dot-notation router for interacting with Deepgram's speak services."""
        return AgentRouter(self._config)

    def upgrade(self):
        """
        Returns the recommended upgrade instructions for the Deepgram SDK.
        """
        return (
            "To upgrade to the latest Deepgram SDK, run:\n"
            "    pip install --upgrade deepgram-sdk\n"
            "For more information, see the README or visit https://github.com/deepgram/deepgram-python-sdk"
        )

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

        def v(self, version: str = ""):
            """
            Returns a client for the specified version of the API.
            """
            self._logger.debug("Version.v ENTER")
            self._logger.info(f"version: {version}")
            if not version:
                self._logger.error("version is empty")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Invalid module version")

            match self._parent:
                case "manage":
                    parent, filename, classname = "manage", "client", "ManageClient"
                case "asyncmanage":
                    parent, filename, classname = "manage", "async_client", "AsyncManageClient"
                case "asyncspeak":
                    return AsyncSpeakRESTClient(self._config)
                case "selfhosted":
                    parent, filename, classname = "selfhosted", "client", "SelfHostedClient"
                case "asyncselfhosted":
                    parent, filename, classname = "selfhosted", "async_client", "AsyncSelfHostedClient"
                case "auth":
                    parent, filename, classname = "auth", "client", "AuthRESTClient"
                case "asyncauth":
                    parent, filename, classname = "auth", "async_client", "AsyncAuthRESTClient"
                case _:
                    self._logger.error(f"parent unknown: {self._parent}")
                    self._logger.debug("Version.v LEAVE")
                    raise DeepgramModuleError("Invalid parent type")

            path = f"deepgram.clients.{parent}.v{version}.{filename}"
            self._logger.info(f"path: {path}")
            self._logger.info(f"classname: {classname}")

            mod = import_module(path)
            if mod is None:
                self._logger.error("module path is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find package")

            my_class = getattr(mod, classname, None)
            if my_class is None:
                self._logger.error("my_class is None")
                self._logger.debug("Version.v LEAVE")
                raise DeepgramModuleError("Unable to find class")

            my_class_instance = my_class(self._config)
            self._logger.notice("Version.v succeeded")
            self._logger.debug("Version.v LEAVE")
            return my_class_instance
