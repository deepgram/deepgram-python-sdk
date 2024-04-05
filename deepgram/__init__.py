# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# version
__version__ = "0.0.0"

# entry point for the deepgram python sdk
from .client import Deepgram, DeepgramClient
from .options import DeepgramClientOptions, ClientOptionsFromEnv
import logging, verboselogs

# listen client
from .client import Listen, Read

# live
from .client import LiveTranscriptionEvents
from .client import LiveClient, AsyncLiveClient
from .client import LiveOptions
from .client import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)

# prerecorded
from .client import PreRecordedClient, AsyncPreRecordedClient
from .client import (
    FileSource,
    PrerecordedSource,
    UrlSource,
    BufferSource,
    ReadStreamSource,
    PrerecordedOptions,
    Sentiment,
)
from .client import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# read
from .client import ReadClient, AsyncReadClient
from .client import AnalyzeClient, AsyncAnalyzeClient
from .client import (
    AnalyzeSource,
    TextSource,
    UrlSource,
    BufferSource,
    AnalyzeStreamSource,
    AnalyzeOptions,
    Sentiment,
)
from .client import (
    AsyncAnalyzeResponse,
    AnalyzeResponse,
    SyncAnalyzeResponse,
)

# speak
from .client import SpeakClient, AsyncSpeakClient
from .client import SpeakSource, TextSource, SpeakStreamSource, SpeakOptions
from .client import SpeakResponse

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

# onprem
from .client import (
    OnPremClient,
    AsyncOnPremClient,
)

# utilities
from .audio import Microphone
from .audio import (
    LOGGING,
    CHANNELS,
    RATE,
    CHUNK,
)
