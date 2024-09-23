# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT


from dataclasses import dataclass

from ....common import (
    BaseResponse,
    OpenResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)


# Speak Response Types:


@dataclass
class MetadataResponse(BaseResponse):
    """
    Metadata object
    """

    type: str = ""
    request_id: str = ""


@dataclass
class FlushedResponse(BaseResponse):
    """
    Flushed Message from the Deepgram Platform
    """

    type: str = ""
    sequence_id: int = 0


@dataclass
class ClearedResponse(BaseResponse):
    """
    Cleared object
    """

    type: str = ""
    sequence_id: int = 0


@dataclass
class WarningResponse(BaseResponse):
    """
    Warning Message from the Deepgram Platform
    """

    warn_code: str = ""
    warn_msg: str = ""
    type: str = ""
