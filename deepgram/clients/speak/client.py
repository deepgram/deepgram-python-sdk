# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import SpeakClient as SpeakClientLatest
from .v1.async_client import AsyncSpeakClient as AsyncSpeakClientLatest
from .v1.options import (
    SpeakOptions as SpeakOptionsLatest,
    SpeakSource as SpeakSourceLatest,
    TextSource as TextSourceLatest,
    SpeakStreamSource as SpeakStreamSourceLatest,
)
from .v1.response import SpeakResponse as SpeakResponseLatest

"""
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


# input
class SpeakOptions(SpeakOptionsLatest):
    """
    Please see SpeakOptionsLatest for details
    """

    pass


class TextSource(TextSourceLatest):
    """
    Please see TextSourceLatest for details
    """

    pass


class SpeakStreamSource(SpeakStreamSourceLatest):
    """
    Please see SpeakStreamSourceLatest for details
    """

    pass


SpeakSource = SpeakSourceLatest


# output
class SpeakResponse(SpeakResponseLatest):
    """
    Please see SpeakResponseLatest for details
    """

    pass


# clients
class SpeakClient(SpeakClientLatest):
    """
    Please see SpeakClientLatest for details
    """

    def __init__(self, config):
        self.config = config
        super().__init__(config)


class AsyncSpeakClient(AsyncSpeakClientLatest):
    """
    Please see AsyncSpeakClientLatest for details
    """

    def __init__(self, config):
        super().__init__(config)
