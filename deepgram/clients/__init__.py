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
    Sentiment,
)

# listen
from .listen_router import Listen
from .read_router import Read
from .speak_router import Speak

# live
from .live import LiveClient, AsyncLiveClient
from .live import LiveOptions
from .live import LiveTranscriptionEvents
from .live import (
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
from .prerecorded import PreRecordedClient, AsyncPreRecordedClient
from .prerecorded import PrerecordedOptions
from .prerecorded import (
    PreRecordedStreamSource,
    PrerecordedSource,
)
from .prerecorded import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# read
from .analyze import ReadClient, AsyncReadClient
from .analyze import AnalyzeClient, AsyncAnalyzeClient
from .analyze import AnalyzeOptions
from .analyze import (
    AnalyzeStreamSource,
    AnalyzeSource,
)
from .analyze import (
    AsyncAnalyzeResponse,
    AnalyzeResponse,
    SyncAnalyzeResponse,
)

# speak
from .speak import (
    SpeakOptions,
    FileSource,
    SpeakWebSocketSource,
    SpeakSource,
)

# speak REST
from .speak import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)

from .speak import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

# speak WebSocket
from .speak import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
)
from .speak import (
    SpeakWebSocketResponse,
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
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

# selfhosted
from .selfhosted import (
    OnPremClient,
    AsyncOnPremClient,
    SelfHostedClient,
    AsyncSelfHostedClient,
)
