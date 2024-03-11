# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import List, Optional, TypedDict, Dict

import io

# Speak Response Types:


@dataclass_json
@dataclass
class SpeakResponse:
    content_type: str = ""
    request_id: str = ""
    model_uuid: str = ""
    model_name: str = ""
    characters: str = 0
    transfer_encoding: str = ""
    date: str = ""
    stream: Optional[io.BytesIO] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    filename: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    # this is a hack to make the response look like a dict because of the io.BytesIO object
    # otherwise it will throw an exception on printing
    def __str__(self) -> str:
        myDict = self.to_dict()
        return myDict.__str__()
