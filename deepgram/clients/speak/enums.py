# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from aenum import StrEnum

# Constants mapping to events from the Deepgram API


class SpeakWebSocketMessage(StrEnum):
    """
    Enumerates the possible message types that can be received from the Deepgram API
    """

    Speak: str = "Speak"
    Flush: str = "Flush"
    Clear: str = "Clear"
    Close: str = "Close"


class SpeakWebSocketEvents(StrEnum):
    """
    Enumerates the possible events that can be received from the Deepgram API
    """

    Open: str = "Open"
    Close: str = "Close"
    AudioData: str = "AudioData"
    Metadata: str = "Metadata"
    Flushed: str = "Flushed"
    Cleared: str = "Cleared"
    Unhandled: str = "Unhandled"
    Error: str = "Error"
    Warning: str = "Warning"
