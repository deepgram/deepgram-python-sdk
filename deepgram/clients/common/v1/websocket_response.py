# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from .shared_response import BaseResponse


# Result Message


@dataclass
class OpenResponse(BaseResponse):
    """
    Open Message from the Deepgram Platform
    """

    type: str = ""


# Close Message


@dataclass
class CloseResponse(BaseResponse):
    """
    Close Message from the Deepgram Platform
    """

    type: str = ""


# Error Message


@dataclass
class ErrorResponse(BaseResponse):
    """
    Error Message from the Deepgram Platform
    """

    description: str = ""
    message: str = ""
    type: str = ""
    variant: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )


# Unhandled Message


@dataclass
class UnhandledResponse(BaseResponse):
    """
    Unhandled Message from the Deepgram Platform
    """

    type: str = ""
    raw: str = ""
