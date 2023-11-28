# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from enum import Enum


class LiveTranscriptionEvents(Enum):
    Open = "open"
    Close = "close"
    Transcript = "Results"
    Metadata = "Metadata"
    Error = "error"
    Warning = "warning"
