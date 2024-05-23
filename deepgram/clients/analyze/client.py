# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import AnalyzeClient as AnalyzeClientLatest
from .v1.async_client import AsyncAnalyzeClient as AsyncAnalyzeClientLatest
from .v1.options import (
    AnalyzeOptions as AnalyzeOptionsLatest,
    UrlSource as UrlSourceLatest,
    FileSource as FileSourceLatest,
    AnalyzeStreamSource as AnalyzeStreamSourceLatest,
    AnalyzeSource as AnalyzeSourceLatest,
)
from .v1.response import (
    SyncAnalyzeResponse as SyncAnalyzeResponseLatest,
    AnalyzeResponse as AnalyzeResponseLatest,
    AsyncAnalyzeResponse as AsyncAnalyzeResponseLatest,
)

# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
AnalyzeOptions = AnalyzeOptionsLatest
AnalyzeStreamSource = AnalyzeStreamSourceLatest
FileSource = FileSourceLatest
UrlSource = UrlSourceLatest
AnalyzeSource = AnalyzeSourceLatest


# responses
AsyncAnalyzeResponse = AsyncAnalyzeResponseLatest
AnalyzeResponse = AnalyzeResponseLatest
SyncAnalyzeResponse = SyncAnalyzeResponseLatest


# clients
AnalyzeClient = AnalyzeClientLatest
AsyncAnalyzeClient = AsyncAnalyzeClientLatest


# aliases
ReadClient = AnalyzeClientLatest
AsyncReadClient = AsyncAnalyzeClientLatest
