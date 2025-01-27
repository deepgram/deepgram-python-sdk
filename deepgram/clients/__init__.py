# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# common
from .common import (
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
    UrlSource,
)
from .common import BaseResponse

# common (shared between analze and prerecorded)
from .common import (
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

# common (shared between listen rest and websocket)
from .common import (
    ModelInfo,
    Hit,
    Search,
)
from .common import (
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)
from .common import (
    DeepgramError,
    DeepgramTypeError,
    DeepgramApiError,
    DeepgramUnknownApiError,
)
from .errors import DeepgramModuleError

from .listen_router import ListenRouter
from .read_router import ReadRouter
from .speak_router import SpeakRouter
from .agent_router import AgentRouter

# listen
from .listen import LiveTranscriptionEvents

## backward compat
from .prerecorded import (
    PreRecordedClient,
    AsyncPreRecordedClient,
)
from .live import (
    LiveClient,
    AsyncLiveClient,
)

# speech-to-text rest
from .listen import ListenRESTClient, AsyncListenRESTClient

## input
from .listen import (
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

from .listen import (
    ListenRESTOptions,
    PrerecordedOptions,
)

## output
from .listen import (
    #### top level
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
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
    #### between rest and websocket
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


# speech-to-text websocket
from .listen import ListenWebSocketClient, AsyncListenWebSocketClient

## input
from .listen import (
    ListenWebSocketOptions,
    LiveOptions,
)

## output
from .listen import (
    #### top level
    LiveResultResponse,
    ListenWSMetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    #### common websocket response
    # OpenResponse,
    # CloseResponse,
    # ErrorResponse,
    # UnhandledResponse,
    #### uniqye
    ListenWSMetadata,
    ListenWSWord,
    ListenWSAlternative,
    ListenWSChannel,
)

## clients
from .listen import (
    ListenWebSocketClient,
    AsyncListenWebSocketClient,
)


# read/analyze
from .analyze import ReadClient, AsyncReadClient
from .analyze import AnalyzeClient, AsyncAnalyzeClient
from .analyze import AnalyzeOptions
from .analyze import (
    # common
    # UrlSource,
    # TextSource,
    # BufferSource,
    # StreamSource,
    # FileSource
    # unique
    AnalyzeStreamSource,
    AnalyzeSource,
)
from .analyze import (
    #### top level
    AsyncAnalyzeResponse,
    SyncAnalyzeResponse,
    AnalyzeResponse,
    #### shared between analyze and pre-recorded
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

# text-to-speech
## text-to-speech REST
from .speak import (
    #### top level
    SpeakRESTOptions,
    SpeakOptions,
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

from .speak import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)

from .speak import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

## text-to-speech WebSocket
from .speak import SpeakWebSocketEvents, SpeakWebSocketMessage

from .speak import (
    SpeakWSOptions,
)

from .speak import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)

from .speak import (
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
from .manage import ManageClient, AsyncManageClient
from .manage import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)
from .manage import (
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
from .selfhosted import (
    OnPremClient,
    AsyncOnPremClient,
    SelfHostedClient,
    AsyncSelfHostedClient,
)

# agent
from .agent import AgentWebSocketEvents

# websocket
from .agent import (
    AgentWebSocketClient,
    AsyncAgentWebSocketClient,
)

from .agent import (
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
    FunctionCalling,
    FunctionCallRequest,
    AgentStartedSpeakingResponse,
    AgentAudioDoneResponse,
)

from .agent import (
    # top level
    SettingsConfigurationOptions,
    UpdateInstructionsOptions,
    UpdateSpeakOptions,
    InjectAgentMessageOptions,
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
    Provider,
    Think,
    Agent,
    Input,
    Output,
    Audio,
    Context,
)
