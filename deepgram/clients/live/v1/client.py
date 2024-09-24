# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ...listen.v1 import ListenWebSocketClient as LiveClientLatest
from ...listen.v1 import AsyncListenWebSocketClient as AsyncLiveClientLatest
from ...listen.v1 import LiveOptions as LiveOptionsLatest
from ...listen.v1 import (
    OpenResponse as OpenResponseLatest,
    LiveResultResponse as LiveResultResponseLatest,
    ListenWSMetadataResponse as ListenWSMetadataResponseLatest,
    SpeechStartedResponse as SpeechStartedResponseLatest,
    UtteranceEndResponse as UtteranceEndResponseLatest,
    CloseResponse as CloseResponseLatest,
    ErrorResponse as ErrorResponseLatest,
    UnhandledResponse as UnhandledResponseLatest,
)

# The vX/client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
LiveOptions = LiveOptionsLatest
OpenResponse = OpenResponseLatest
LiveResultResponse = LiveResultResponseLatest
ListenWSMetadataResponse = ListenWSMetadataResponseLatest
MetadataResponse = ListenWSMetadataResponseLatest
SpeechStartedResponse = SpeechStartedResponseLatest
UtteranceEndResponse = UtteranceEndResponseLatest
CloseResponse = CloseResponseLatest
ErrorResponse = ErrorResponseLatest
UnhandledResponse = UnhandledResponseLatest


# clients
LiveClient = LiveClientLatest
AsyncLiveClient = AsyncLiveClientLatest
