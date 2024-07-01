# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ...listen import PreRecordedClient as PreRecordedClientLatest
from ...listen import AsyncPreRecordedClient as AsyncPreRecordedClientLatest
from ...listen import (
    PrerecordedOptions as PrerecordedOptionsLatest,
    UrlSource as UrlSourceLatest,
    FileSource as FileSourceLatest,
    PreRecordedStreamSource as PreRecordedStreamSourceLatest,
    PrerecordedSource as PrerecordedSourceLatest,
)
from ...listen import (
    AsyncPrerecordedResponse as AsyncPrerecordedResponseLatest,
    PrerecordedResponse as PrerecordedResponseLatest,
    SyncPrerecordedResponse as SyncPrerecordedResponseLatest,
)


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
