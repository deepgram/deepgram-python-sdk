# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional, Dict, Any
import io

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from ....common import (
    BaseResponse,
)


# Speak Response Types:


@dataclass
class SpeakRESTResponse(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    A class for representing a response from the speak endpoint.
    """

    content_type: str = ""
    request_id: str = ""
    model_uuid: str = ""
    model_name: str = ""
    characters: int = 0
    transfer_encoding: str = ""
    date: str = ""
    filename: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    # pylint: disable=W0511
    # TODO: stream will be deprecated in a future release. Please use stream_memory instead.
    stream: Optional[io.BytesIO] = field(
        default=None,
        metadata=dataclass_config(exclude=lambda f: True),
    )
    # pylint: enable=W0511
    stream_memory: Optional[io.BytesIO] = field(
        default=None,
        metadata=dataclass_config(exclude=lambda f: True),
    )
