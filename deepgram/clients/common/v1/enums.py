# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from aenum import StrEnum

# Constants mapping to events from the Deepgram API


class Sentiment(StrEnum):
    """
    Sentiment values.
    """

    UNKNOWN: str = ""
    NEGATIVE: str = "negative"
    NEUTRAL: str = "neutral"
    POSITIVE: str = "positive"
