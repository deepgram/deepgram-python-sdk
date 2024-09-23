# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# backward compat
from .rest import (
    ListenRESTClient as PreRecordedClient,
    AsyncListenRESTClient as AsyncPreRecordedClient,
)
from .websocket import (
    ListenWebSocketClient as LiveClient,
    AsyncListenWebSocketClient as AsyncLiveClient,
)

# shared
from ...common import (
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

# between rest and websocket
from ...common import (
    ModelInfo,
    Alternative,
    Hit,
    Search,
    Channel,
    Word,
)

# common websocket
from ...common import (
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)

# rest
from .rest import ListenRESTClient, AsyncListenRESTClient
from .rest import ListenRESTOptions, PrerecordedOptions
from .rest import (
    # common
    UrlSource,
    BufferSource,
    StreamSource,
    TextSource,
    FileSource,
    # unique
    PreRecordedStreamSource,
    PrerecordedSource,
    ListenRestSource,
)
from .rest import (
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
    #### unique
    Entity,
    Metadata as ListenRESTMetadata,
    Paragraph,
    Paragraphs,
    Results as ListenRESTResults,
    Sentence,
    Summaries,
    SummaryV1,
    SummaryV2,
    Translation,
    Utterance,
    Warning,
)

# websocket
from .websocket import ListenWebSocketClient, AsyncListenWebSocketClient
from .websocket import LiveOptions, ListenWebSocketOptions
from .websocket import (
    #### top level
    LiveResultResponse,
    MetadataResponse as ListenWSMetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    #### common websocket response
    # BaseResponse,
    # OpenResponse,
    # CloseResponse,
    # ErrorResponse,
    # UnhandledResponse,
    #### between rest and websocket
    # ModelInfo,
    # Alternative,
    # Hit,
    # Search,
    # Channel,
    # Word,
    #### unique
    Metadata as ListenWSMetadata,
)
