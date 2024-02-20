# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, Optional, TypedDict, Dict

# Speak Response Types:


@dataclass_json
@dataclass
class SpeakResponse:
    content_type: Optional[str] = ""
    request_id: Optional[str] = ""
    model_uuid: Optional[str] = ""
    model_name: Optional[str] = ""
    characters: Optional[int] = 0
    transfer_encoding: Optional[str] = ""
    date: Optional[str] = ""
    stream: Optional[bytes] = None
    filename: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __str__(self) -> str:
        return self.to_json(indent=4)
