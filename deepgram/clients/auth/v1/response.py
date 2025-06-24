# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from ...common import (
    BaseResponse,
)


@dataclass
class GrantTokenResponse(BaseResponse):
    """
    The response object for the authentication grant token endpoint.
    """

    access_token: str = field(
        metadata=dataclass_config(field_name="access_token"),
        default="",
    )
    expires_in: int = field(
        metadata=dataclass_config(field_name="expires_in"),
        default=30,
    )
