# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import SpeakClient as SpeakClientLatest
from .v1.async_client import AsyncSpeakClient as AsyncSpeakClientLatest
from .v1.options import (
    SpeakOptions as SpeakOptionsLatest,
    FileSource as FileSourceLatest,
    SpeakStreamSource as SpeakStreamSourceLatest,
    SpeakSource as SpeakSourceLatest,
)
from .v1.response import SpeakResponse as SpeakResponseLatest

# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
SpeakOptions = SpeakOptionsLatest
SpeakStreamSource = SpeakStreamSourceLatest


FileSource = FileSourceLatest
SpeakSource = SpeakSourceLatest


# output
SpeakResponse = SpeakResponseLatest
SpeakClient = SpeakClientLatest
AsyncSpeakClient = AsyncSpeakClientLatest
