# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import PreRecordedClient as PreRecordedClientLatest
from .v1.async_client import AsyncPreRecordedClient as AsyncPreRecordedClientLatest
from .v1.options import (
    PrerecordedOptions as PrerecordedOptionsLatest,
    UrlSource as UrlSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    PrerecordedSource as PrerecordedSourceLatest,
)
from .v1.response import (
    AsyncPrerecordedResponse as AsyncPrerecordedResponseLatest,
    PrerecordedResponse as PrerecordedResponseLatest,
    SyncPrerecordedResponse as SyncPrerecordedResponseLatest,
)
from .enums import Sentiment

"""
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


# input
class PrerecordedOptions(PrerecordedOptionsLatest):
    """
    Please see PrerecordedOptionsLatest for details
    """

    pass


class UrlSource(UrlSourceLatest):
    """
    Please see UrlSourceLatest for details
    """

    pass


class BufferSource(BufferSourceLatest):
    """
    Please see BufferSourceLatest for details
    """

    pass


class StreamSource(StreamSourceLatest):
    """
    Please see StreamSourceLatest for details
    """

    pass


FileSource = FileSourceLatest
PrerecordedSource = PrerecordedSourceLatest


# output
class AsyncPrerecordedResponse(AsyncPrerecordedResponseLatest):
    """
    Please see AsyncPrerecordedResponseLatest for details
    """

    pass


class PrerecordedResponse(PrerecordedResponseLatest):
    """
    Please see PrerecordedResponseLatest for details
    """

    pass


class SyncPrerecordedResponse(PrerecordedResponseLatest):
    """
    Please see PrerecordedResponseLatest for details
    """

    pass


# clients
class PreRecordedClient(PreRecordedClientLatest):
    """
    Please see PreRecordedClientLatest for details
    """

    def __init__(self, config):
        self.config = config
        super().__init__(config)


class AsyncPreRecordedClient(AsyncPreRecordedClientLatest):
    """
    Please see AsyncPreRecordedClientLatest for details
    """

    def __init__(self, config):
        super().__init__(config)
