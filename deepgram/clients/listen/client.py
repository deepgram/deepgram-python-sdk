# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT


from ...options import DeepgramClientOptions, ClientOptionsFromEnv

# rest
from .v1 import (
    ListenRESTClient as ListenRESTClientLatest,
    AsyncListenRESTClient as AsyncListenRESTClientLatest,
)
from .v1 import PrerecordedOptions as PrerecordedOptionsLatest

from .v1 import (
    UrlSource as UrlSourceLatest,
    FileSource as FileSourceLatest,
    PreRecordedStreamSource as PreRecordedStreamSourceLatest,
    PrerecordedSource as PrerecordedSourceLatest,
)
from .v1 import (
    AsyncPrerecordedResponse as AsyncPrerecordedResponseLatest,
    PrerecordedResponse as PrerecordedResponseLatest,
    SyncPrerecordedResponse as SyncPrerecordedResponseLatest,
)

# websocket
from .v1 import (
    ListenWebSocketClient as ListenWebSocketClientLatest,
    AsyncListenWebSocketClient as AsyncListenWebSocketClientLatest,
)
from .v1 import LiveOptions as LiveOptionsLatest, LiveOptions as SteamingOptionsLatest
from .v1 import (
    OpenResponse as OpenResponseLatest,
    LiveResultResponse as LiveResultResponseLatest,
    MetadataResponse as MetadataResponseLatest,
    SpeechStartedResponse as SpeechStartedResponseLatest,
    UtteranceEndResponse as UtteranceEndResponseLatest,
    CloseResponse as CloseResponseLatest,
    ErrorResponse as ErrorResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
)

# The vX/client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# backward compat
PreRecordedClient = ListenRESTClientLatest
AsyncPreRecordedClient = AsyncListenRESTClientLatest
LiveClient = ListenWebSocketClientLatest
AsyncLiveClient = ListenWebSocketClientLatest

# rest
## input
PrerecordedOptions = PrerecordedOptionsLatest
PreRecordedStreamSource = PreRecordedStreamSourceLatest
UrlSource = UrlSourceLatest
FileSource = FileSourceLatest
PrerecordedSource = PrerecordedSourceLatest

## output
AsyncPrerecordedResponse = AsyncPrerecordedResponseLatest
PrerecordedResponse = PrerecordedResponseLatest
SyncPrerecordedResponse = SyncPrerecordedResponseLatest


# websocket
## input
LiveOptions = LiveOptionsLatest

## output
OpenResponse = OpenResponseLatest
LiveResultResponse = LiveResultResponseLatest
MetadataResponse = MetadataResponseLatest
SpeechStartedResponse = SpeechStartedResponseLatest
UtteranceEndResponse = UtteranceEndResponseLatest
CloseResponse = CloseResponseLatest
ErrorResponse = ErrorResponseLatest
UnhandledResponse = UnhandledResponseLatest


# clients
ListenWebSocketClient = ListenWebSocketClientLatest
AsyncListenWebSocketClient = AsyncListenWebSocketClientLatest
