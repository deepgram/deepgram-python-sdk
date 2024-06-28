# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1 import (
    SpeakRESTClient as SpeakRESTClientLatest,
    AsyncSpeakRESTClient as AsyncSpeakRESTClientLatest,
    SpeakWebSocketClient as SpeakWebSocketClientLatest,
    AsyncSpeakWebSocketClient as AsyncSpeakWebSocketClientLatest,
)
from .v1 import (
    SpeakOptions as SpeakOptionsLatest,
    FileSource as FileSourceLatest,
    SpeakWebSocketSource as SpeakWebSocketSourceLatest,
    SpeakSource as SpeakSourceLatest,
)
from .v1 import (
    SpeakRESTResponse as SpeakRESTResponseLatest,
    SpeakWebSocketResponse as SpeakWebSocketResponseLatest,
    OpenResponse as OpenResponseLatest,
    MetadataResponse as MetadataResponseLatest,
    FlushedResponse as MetadataResponseLatest,
    CloseResponse as CloseResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
    WarningResponse as WarningResponseLatest,
    ErrorResponse as ErrorResponseLatest,
)

# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
SpeakOptions = SpeakOptionsLatest
SpeakWebSocketSource = SpeakWebSocketSourceLatest
FileSource = FileSourceLatest
SpeakSource = SpeakSourceLatest

# output
SpeakRESTResponse = SpeakRESTResponseLatest
SpeakWebSocketResponse = SpeakWebSocketResponseLatest
OpenResponse = OpenResponseLatest
MetadataResponse = MetadataResponseLatest
FlushedResponse = MetadataResponseLatest
CloseResponse = CloseResponseLatest
UnhandledResponse = UnhandledResponseLatest
WarningResponse = WarningResponseLatest
ErrorResponse = ErrorResponseLatest


# backward compatibility
SpeakResponse = SpeakRESTResponseLatest
SpeakClient = SpeakRESTClientLatest

# clients
SpeakRESTClient = SpeakRESTClientLatest
AsyncSpeakRESTClient = AsyncSpeakRESTClientLatest
SpeakWebSocketClient = SpeakWebSocketClientLatest
AsyncSpeakWebSocketClient = AsyncSpeakWebSocketClientLatest
