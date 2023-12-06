# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional


@dataclass_json
@dataclass
class LiveOptions:
    callback: Optional[str] = None
    channels: Optional[int] = None
    diarize: Optional[bool] = None
    encoding: Optional[str] = None
    endpointing: Optional[str] = None
    interim_results: Optional[bool] = None
    keywords: Optional[str] = None
    language: Optional[str] = None
    model: Optional[str] = None
    multichannel: Optional[bool] = None
    numerals: Optional[bool] = None
    punctuate: Optional[bool] = None
    profanity_filter: Optional[bool] = None
    redact: Optional[bool] = None
    replace: Optional[str] = None
    sample_rate: Optional[int] = None
    search: Optional[str] = None
    smart_format: Optional[bool] = None
    tag: Optional[list] = None
    tier: Optional[str] = None
    version: Optional[str] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]
