# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .enums import SpeakWebSocketEvents, SpeakWebSocketMessage

# rest
from .client import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
)
from .client import (
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
from .client import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
)

# websocket
from .client import (
    SpeakWSOptions,
)
from .client import (
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)
from .client import (
    #### top level
    SpeakWSMetadataResponse,
    FlushedResponse,
    ClearedResponse,
    WarningResponse,
    #### shared
    OpenResponse,
    CloseResponse,
    UnhandledResponse,
    ErrorResponse,
)
