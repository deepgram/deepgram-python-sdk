# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .enums import SpeakWebSocketEvents
from ...options import DeepgramClientOptions, ClientOptionsFromEnv

from .client import (
    SpeakClient,  # backward compat
    SpeakRESTClient,
    AsyncSpeakRESTClient,
    SpeakWebSocketClient,
    AsyncSpeakWebSocketClient,
)
from .client import (
    SpeakOptions,
    FileSource,
    SpeakWebSocketSource,
    SpeakSource,
)
from .client import (
    SpeakResponse,  # backward compat
    SpeakRESTResponse,
    SpeakWebSocketResponse,
    OpenResponse,
    MetadataResponse,
    FlushedResponse,
    CloseResponse,
    UnhandledResponse,
    WarningResponse,
    ErrorResponse,
)
