# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .options import (
    SpeakOptions,
)
from .rest import (
    SpeakRESTOptions,
    SpeakRestSource,
    SpeakSource,
    FileSource,
)
from .websocket import (
    SpeakWebSocketOptions,
)
from ....options import DeepgramClientOptions, ClientOptionsFromEnv

# rest
from .rest import SpeakRESTClient, AsyncSpeakRESTClient

from .rest import SpeakRESTResponse

# websocket
from .websocket import SpeakWebSocketClient, AsyncSpeakWebSocketClient
from .websocket import (
    SpeakWebSocketResponse,
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
)
