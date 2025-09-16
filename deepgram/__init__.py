# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# version
__version__ = "0.0.0"

# entry point for the deepgram python sdk
import logging
from .utils import VerboseLogger
from .utils import (
    NOTICE,
    SPAM,
    SUCCESS,
    VERBOSE,
    WARNING,
    ERROR,
    FATAL,
    CRITICAL,
    INFO,
    DEBUG,
    NOTSET,
)

from .client import Deepgram, DeepgramClient
from .client import DeepgramClientOptions, ClientOptionsFromEnv
from .client import (
    DeepgramError,
    DeepgramTypeError,
    DeepgramModuleError,
    DeepgramApiError,
    DeepgramUnknownApiError,
)
from .errors import DeepgramApiKeyError

# listen/read client
from .client import ListenRouter, ReadRouter, SpeakRouter, AgentRouter

# common
from .client import (
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
    UrlSource,
)
from .client import BaseResponse
from .client import (
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
from .client import (
    ModelInfo,
    Hit,
    Search,
)
from .client import (
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)

# speect-to-text WS
from .client import LiveClient, AsyncLiveClient  # backward compat
from .client import ListenWebSocketClient, AsyncListenWebSocketClient
from .client import LiveTranscriptionEvents
from .client import LiveOptions, ListenWebSocketOptions
from .client import (
    #### top level
    LiveResultResponse,
    ListenWSMetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    #### common websocket response
    # OpenResponse,
    # CloseResponse,
    # UnhandledResponse,
    # ErrorResponse,
    #### unique
    ListenWSMetadata,
    ListenWSAlternative,
    ListenWSChannel,
    ListenWSWord,
)

# prerecorded
from .client import PreRecordedClient, AsyncPreRecordedClient  # backward compat
from .client import ListenRESTClient, AsyncListenRESTClient
from .client import (
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
    SpeakRESTSource,
)
from .client import (
    ListenRESTOptions,
    PrerecordedOptions,
)
from .client import (
    #### top level
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
    #### shared
    # Average,
    # Alternative,
    # Channel,
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
    # Word,
    #### unique
    Entity,
    Hit,
    ListenRESTMetadata,
    ModelInfo,
    Paragraph,
    Paragraphs,
    ListenRESTResults,
    Search,
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
from .client import ReadClient, AsyncReadClient
from .client import AnalyzeClient, AsyncAnalyzeClient
from .client import (
    AnalyzeOptions,
    AnalyzeStreamSource,
    AnalyzeSource,
)
from .client import (
    #### top level
    AsyncAnalyzeResponse,
    SyncAnalyzeResponse,
    AnalyzeResponse,
    #### shared
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
    #### unique
    AnalyzeMetadata,
    AnalyzeResults,
    AnalyzeSummary,
)

# speak
## speak REST
from .client import (
    #### top level
    SpeakRESTOptions,
    SpeakOptions,  # backward compat
    #### common
    # TextSource,
    # BufferSource,
    # StreamSource,
    # FileSource,
    #### unique
    SpeakSource,
    SpeakRestSource,
)

from .client import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)

from .client import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

## speak WebSocket
from .client import SpeakWebSocketEvents, SpeakWebSocketMessage

from .client import (
    SpeakWSOptions,
)

from .client import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)

from .client import (
    #### top level
    SpeakWSMetadataResponse,
    FlushedResponse,
    ClearedResponse,
    WarningResponse,
    #### common websocket response
    # OpenResponse,
    # CloseResponse,
    # UnhandledResponse,
    # ErrorResponse,
)

# manage
from .client import ManageClient, AsyncManageClient
from .client import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)

# manage client responses
from .client import (
    #### top level
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
    #### shared
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

# selfhosted
from .client import (
    OnPremClient,
    AsyncOnPremClient,
    SelfHostedClient,
    AsyncSelfHostedClient,
)


# agent
from .client import AgentWebSocketEvents

# websocket
from .client import (
    AgentWebSocketClient,
    AsyncAgentWebSocketClient,
)

from .client import (
    #### common websocket response
    # OpenResponse,
    # CloseResponse,
    # ErrorResponse,
    # UnhandledResponse,
    #### unique
    WelcomeResponse,
    SettingsAppliedResponse,
    ConversationTextResponse,
    UserStartedSpeakingResponse,
    AgentThinkingResponse,
    FunctionCall,
    FunctionCallRequest,
    AgentStartedSpeakingResponse,
    AgentAudioDoneResponse,
    InjectionRefusedResponse,
)

from .client import (
    # top level
    SettingsOptions,
    UpdatePromptOptions,
    UpdateSpeakOptions,
    InjectAgentMessageOptions,
    InjectUserMessageOptions,
    FunctionCallResponse,
    AgentKeepAlive,
    Flags,
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
    Context,
    HistoryConversationMessage,
    HistoryFunctionCallsMessage,
    FunctionCallHistory,
)

# utilities
# pylint: disable=wrong-import-position
from .audio import Microphone, DeepgramMicrophoneError
from .audio import (
    INPUT_LOGGING,
    INPUT_CHANNELS,
    INPUT_RATE,
    INPUT_CHUNK,
)

LOGGING = INPUT_LOGGING
CHANNELS = INPUT_CHANNELS
RATE = INPUT_RATE
CHUNK = INPUT_CHUNK

from .audio import Speaker
from .audio import (
    OUTPUT_LOGGING,
    OUTPUT_CHANNELS,
    OUTPUT_RATE,
    OUTPUT_CHUNK,
)

# pylint: enable=wrong-import-position
