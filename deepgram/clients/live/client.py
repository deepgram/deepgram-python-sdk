# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import LiveClient as LiveClientLatest
from .v1.async_client import AsyncLiveClient as AsyncLiveClientLatest
from .v1.options import LiveOptions as LiveOptionsLatest
from .v1.response import (
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


# input
LiveOptions = LiveOptionsLatest
OpenResponse = OpenResponseLatest
LiveResultResponse = LiveResultResponseLatest
MetadataResponse = MetadataResponseLatest
SpeechStartedResponse = SpeechStartedResponseLatest
UtteranceEndResponse = UtteranceEndResponseLatest
CloseResponse = CloseResponseLatest
ErrorResponse = ErrorResponseLatest
UnhandledResponse = UnhandledResponseLatest


# clients
LiveClient = LiveClientLatest
AsyncLiveClient = AsyncLiveClientLatest
