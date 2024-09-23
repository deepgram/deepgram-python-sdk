# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# rest
from .v1 import (
    #### top level
    SpeakOptions as SpeakOptionsLatest,
    SpeakRESTOptions as SpeakRESTOptionsLatest,
    # common
    TextSource as TextSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    # unique
    SpeakSource as SpeakSourceLatest,
    SpeakRestSource as SpeakRestSourceLatest,
    SpeakRESTSource as SpeakRESTSourceLatest,
)

from .v1 import (
    SpeakRESTClient as SpeakRESTClientLatest,
    AsyncSpeakRESTClient as AsyncSpeakRESTClientLatest,
)

from .v1 import (
    SpeakRESTResponse as SpeakRESTResponseLatest,
)

# websocket
from .v1 import (
    SpeakWebSocketClient as SpeakWebSocketClientLatest,
    AsyncSpeakWebSocketClient as AsyncSpeakWebSocketClientLatest,
    SpeakWSClient as SpeakWSClientLatest,
    AsyncSpeakWSClient as AsyncSpeakWSClientLatest,
)

from .v1 import (
    SpeakWSOptions as SpeakWSOptionsLatest,
)
from .v1 import (
    OpenResponse as OpenResponseLatest,
    SpeakWSMetadataResponse as SpeakWSMetadataResponseLatest,
    FlushedResponse as FlushedResponseLatest,
    ClearedResponse as ClearedResponseLatest,
    CloseResponse as CloseResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
    WarningResponse as WarningResponseLatest,
    ErrorResponse as ErrorResponseLatest,
)

# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.

# rest
# input
SpeakOptions = SpeakOptionsLatest
SpeakRESTOptions = SpeakRESTOptionsLatest
TextSource = TextSourceLatest
BufferSource = BufferSourceLatest
StreamSource = StreamSourceLatest
FileSource = FileSourceLatest
SpeakSource = SpeakSourceLatest
SpeakRestSource = SpeakRestSourceLatest
SpeakRESTSource = SpeakRESTSourceLatest

# output
SpeakRESTResponse = SpeakRESTResponseLatest

# websocket
# input
SpeakWSOptions = SpeakWSOptionsLatest

# output
OpenResponse = OpenResponseLatest
SpeakWSMetadataResponse = SpeakWSMetadataResponseLatest
FlushedResponse = FlushedResponseLatest
ClearedResponse = ClearedResponseLatest
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
SpeakWSClient = SpeakWSClientLatest
AsyncSpeakWSClient = AsyncSpeakWSClientLatest
SpeakWebSocketClient = SpeakWebSocketClientLatest
AsyncSpeakWebSocketClient = AsyncSpeakWebSocketClientLatest
