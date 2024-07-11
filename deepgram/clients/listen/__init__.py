# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .enums import LiveTranscriptionEvents
from ...options import DeepgramClientOptions, ClientOptionsFromEnv

# backward compat
from .client import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    LiveClient,
    AsyncLiveClient,
)

# rest
## input
from .client import (
    ListenRESTOptions,
    PrerecordedOptions,
    PreRecordedStreamSource,
    UrlSource,
    FileSource,
    PrerecordedSource,
    ListenRestSource,
)

## output
from .client import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)


# websocket
## input
from .client import (
    ListenWebSocketOptions,
    LiveOptions,
)

## output
from .client import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)

# clients
from .client import (
    ListenRESTClient,
    AsyncListenRESTClient,
    ListenWebSocketClient,
    AsyncListenWebSocketClient,
)
