# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import PreRecordedClient as PreRecordedClientLatest
from .v1.async_client import AsyncPreRecordedClient as AsyncPreRecordedClientLatest
from .v1.options import (
    PrerecordedOptions as PrerecordedOptionsLatest,
    UrlSource as UrlSourceLatest,
    FileSource as FileSourceLatest,
    PreRecordedStreamSource as PreRecordedStreamSourceLatest,
    PrerecordedSource as PrerecordedSourceLatest,
)
from .v1.response import (
    AsyncPrerecordedResponse as AsyncPrerecordedResponseLatest,
    PrerecordedResponse as PrerecordedResponseLatest,
    SyncPrerecordedResponse as SyncPrerecordedResponseLatest,
)


# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
PrerecordedOptions = PrerecordedOptionsLatest
PreRecordedStreamSource = PreRecordedStreamSourceLatest
UrlSource = UrlSourceLatest
FileSource = FileSourceLatest
PrerecordedSource = PrerecordedSourceLatest


# output
AsyncPrerecordedResponse = AsyncPrerecordedResponseLatest
PrerecordedResponse = PrerecordedResponseLatest
SyncPrerecordedResponse = SyncPrerecordedResponseLatest


# clients
PreRecordedClient = PreRecordedClientLatest
AsyncPreRecordedClient = AsyncPreRecordedClientLatest
