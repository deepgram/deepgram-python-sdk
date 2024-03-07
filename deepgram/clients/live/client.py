# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import LiveClient as LiveClientLatest
from .v1.async_client import AsyncLiveClient as AsyncLiveClientLatest
from .v1.options import LiveOptions as LiveOptionsLatest
from .enums import LiveTranscriptionEvents
from .v1.response import (
    OpenResponse as OpenResponseLatest,
    LiveResultResponse as LiveResultResponseLatest,
    MetadataResponse as MetadataResponseLatest,
    SpeechStartedResponse as SpeechStartedResponseLatest,
    UtteranceEndResponse as UtteranceEndResponseLatest,
    ErrorResponse as ErrorResponseLatest,
    CloseResponse as CloseResponseLatest,
)

"""
The vX/client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


# input
class LiveOptions(LiveOptionsLatest):
    """
    pass through for LiveOptions based on API version
    """

    pass


# responses
class OpenResponse(OpenResponseLatest):
    """
    pass through for OpenResponse based on API version
    """

    pass


class LiveResultResponse(LiveResultResponseLatest):
    """
    pass through for LiveResultResponse based on API version
    """

    pass


class MetadataResponse(MetadataResponseLatest):
    """
    pass through for MetadataResponse based on API version
    """

    pass


class SpeechStartedResponse(SpeechStartedResponseLatest):
    """
    pass through for SpeechStartedResponse based on API version
    """

    pass


class UtteranceEndResponse(UtteranceEndResponseLatest):
    """
    pass through for UtteranceEndResponse based on API version
    """

    pass


class ErrorResponse(ErrorResponseLatest):
    """
    pass through for ErrorResponse based on API version
    """

    pass


class CloseResponse(CloseResponseLatest):
    """
    pass through for CloseResponse based on API version
    """

    pass


# clients
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
