# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from aenum import StrEnum

# Constants mapping to events from the Deepgram API


class WebSocketEvents(StrEnum):
    """
    Enumerates the possible events that can be received from the Deepgram API
    """

    Open: str = "Open"
    Close: str = "Close"
    Warning: str = "Warning"
    Error: str = "Error"
    Unhandled: str = "Unhandled"
