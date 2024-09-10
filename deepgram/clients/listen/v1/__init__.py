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

# rest
from .rest import ListenRESTClient, AsyncListenRESTClient
from .rest import ListenRESTOptions, PrerecordedOptions
from .rest import (
    UrlSource,
    FileSource,
    PreRecordedStreamSource,
    PrerecordedSource,
    ListenRestSource,
)
from .rest import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# websocket
from .websocket import ListenWebSocketClient, AsyncListenWebSocketClient
from .websocket import LiveOptions, ListenWebSocketOptions
from .websocket import (
    OpenResponse,
    LiveResultResponse,
    MetadataResponse,
    SpeechStartedResponse,
    UtteranceEndResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)
