# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import SpeakClient as SpeakClientLatest
from .v1.async_client import AsyncSpeakClient as AsyncSpeakClientLatest
from .v1.options import SpeakOptions as SpeakOptionsLatest
from .v1.response import SpeakResponse as SpeakResponseLatest
from .source import SpeakSource, TextSource

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
