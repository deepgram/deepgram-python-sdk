# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from enum import Enum

"""
Constants mapping to events from the Deepgram API
"""


class LiveTranscriptionEvents(Enum):
    Open = "Open"
    Close = "Close"
    Transcript = "Results"
    Metadata = "Metadata"
    UtteranceEnd = "UtteranceEnd"
    Error = "Error"
    Warning = "Warning"
