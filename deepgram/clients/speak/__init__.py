# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .enums import SpeakWebSocketEvents, SpeakWebSocketMessage
from ...options import DeepgramClientOptions, ClientOptionsFromEnv

from .client import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
    SpeakWSClient,
    AsyncSpeakWSClient,
)
from .client import (
    SpeakOptions,
    SpeakRESTOptions,
    SpeakWSOptions,
    FileSource,
    SpeakRestSource,
    SpeakSource,
)
from .client import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    ClearedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
)
