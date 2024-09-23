# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .enums import LiveTranscriptionEvents

# backward compat
from .client import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    LiveClient,
    AsyncLiveClient,
)

# rest
# common
from .client import (
    UrlSource,
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
)

## input
from .client import (
    ListenRESTOptions,
    PrerecordedOptions,
    PreRecordedStreamSource,
    PrerecordedSource,
    ListenRestSource,
)

## output
from .client import (
    # top level
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
    # shared
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
    # between rest and websocket
    ModelInfo,
    Alternative,
    Hit,
    Search,
    Channel,
    Word,
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
)


# websocket
## input
from .client import (
    ListenWebSocketOptions,
    LiveOptions,
)

## output
from .client import (
    # top level
    LiveResultResponse,
    ListenWSMetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    # common websocket response
    OpenResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
    # unique
    ListenWSMetadata,
)

# clients
from .client import (
    ListenRESTClient,
    AsyncListenRESTClient,
    ListenWebSocketClient,
    AsyncListenWebSocketClient,
)
