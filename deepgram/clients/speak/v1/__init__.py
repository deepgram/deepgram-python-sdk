# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# rest
from .rest import (
    #### top level
    SpeakRESTOptions,
    SpeakOptions,
    # common
    TextSource,
    BufferSource,
    StreamSource,
    FileSource,
    # unique
    SpeakSource,
    SpeakRestSource,
    SpeakRESTSource,
)
from .rest import (
    SpeakRESTOptions,
    SpeakOptions,
)
from .rest import SpeakRESTClient, AsyncSpeakRESTClient
from .rest import SpeakRESTResponse

# websocket
from .websocket import (
    SpeakWSOptions,
)
from .websocket import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)
from .websocket import (
    #### top level
    MetadataResponse as SpeakWSMetadataResponse,
    FlushedResponse,
    ClearedResponse,
    WarningResponse,
    #### shared
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)
