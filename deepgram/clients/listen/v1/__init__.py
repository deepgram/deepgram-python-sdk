# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ....options import DeepgramClientOptions, ClientOptionsFromEnv

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
from .rest import PrerecordedOptions
from .rest import (
    UrlSource,
    FileSource,
    PreRecordedStreamSource,
    PrerecordedSource,
)
from .rest import (
    AsyncPrerecordedResponse,
    PrerecordedResponse,
    SyncPrerecordedResponse,
)

# websocket
from .websocket import ListenWebSocketClient, AsyncListenWebSocketClient
from .websocket import LiveOptions, LiveOptions as SteamingOptions
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
