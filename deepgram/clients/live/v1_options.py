# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Union, List, TypedDict

class LiveOptionsV1(TypedDict, total=False):
    callback: str
    channels: int
    diarize: bool
    encoding: str
    endpointing: int
    interim_results: bool
    keywords: str
    language: str
    model: str
    multichannel: bool
    numerals: bool
    punctuate: bool
    profanity_filter: bool
    redact: bool
    replace: str
    sample_rate: int
    search: str
    smart_format: bool
    tag: list
    tier: str
    version: str

