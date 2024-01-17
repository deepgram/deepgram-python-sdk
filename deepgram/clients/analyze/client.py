# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import AnalyzeClient as AnalyzeClientLatest
from .v1.async_client import AsyncAnalyzeClient as AsyncAnalyzeClientLatest
from .v1.options import AnalyzeOptions as AnalyzeOptionsLatest
from .source import AnalyzeSource, TextSource, UrlSource
from .v1.response import (
    SyncAnalyzeResponse as SyncAnalyzeResponseLatest,
    AnalyzeResponse as AnalyzeResponseLatest,
    AsyncAnalyzeResponse as AsyncAnalyzeResponseLatest,
)
from .enums import Sentiment

"""
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


# input
class AnalyzeOptions(AnalyzeOptionsLatest):
    """
    Please see AnalyzeOptionsLatest for details
    """

    pass


class AsyncAnalyzeResponse(AsyncAnalyzeResponseLatest):
    """
    Please see AnalyzeResponseLatest for details
    """

    pass


class AnalyzeResponse(AnalyzeResponseLatest):
    """
    Please see AnalyzeResponseLatest for details
    """

    pass


class SyncAnalyzeResponse(SyncAnalyzeResponseLatest):
    """
    Please see AnalyzeResponseLatest for details
    """

    pass


# clients
class AnalyzeClient(AnalyzeClientLatest):
    """
    Please see AnalyzeClientLatest for details
    """

    def __init__(self, config):
        self.config = config
        super().__init__(config)


class AsyncAnalyzeClient(AsyncAnalyzeClientLatest):
    """
    Please see AsyncAnalyzeClientLatest for details
    """

    def __init__(self, config):
        super().__init__(config)
