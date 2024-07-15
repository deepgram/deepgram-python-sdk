# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .rest import (
    SpeakRESTOptions,
    SpeakOptions,
    SpeakRestSource,
    SpeakSource,
    FileSource,
)
from .websocket import (
    SpeakWSOptions,
)
from ....options import DeepgramClientOptions, ClientOptionsFromEnv

# rest
from .rest import SpeakRESTClient, AsyncSpeakRESTClient

from .rest import SpeakRESTResponse

# websocket
from .websocket import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)
from .websocket import (
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
)
