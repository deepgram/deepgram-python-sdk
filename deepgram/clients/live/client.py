# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import LiveClient as LiveClientLatest
from .v1.async_client import AsyncLiveClient as AsyncLiveClientLatest
from .v1.options import LiveOptions as LiveOptionsLatest
from .enums import LiveTranscriptionEvents
from .v1.response import LiveResultResponse, MetadataResponse, ErrorResponse

"""
The vX/client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""

class LiveOptions(LiveOptionsLatest):
    """
    pass through for LiveOptions based on API version
    """
    pass

class LiveClient(LiveClientLatest):
    """
    Please see LiveClientLatest for details
    """
    def __init__(self, config):
        super().__init__(config)

class AsyncLiveClient(AsyncLiveClientLatest):
    """
    Please see LiveClientLatest for details
    """
    def __init__(self, config):
        super().__init__(config)
