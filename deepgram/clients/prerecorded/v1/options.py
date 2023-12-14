# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Union, List, TypedDict, Optional


@dataclass_json
@dataclass
class PrerecordedOptions:
    """
    Contains all the options for the PrerecordedClient.

    Reference:
    https://developers.deepgram.com/reference/pre-recorded
    """
    alternatives: Optional[int] = None
    callback: Optional[str] = None
    detect_entities: Optional[bool] = None
    detect_language: Optional[bool] = None
    detect_topics: Optional[bool] = None
    diarize: Optional[bool] = None
    keywords: Optional[Union[list, str]] = None
    language: Optional[str] = None
    model: Optional[str] = None
    multichannel: Optional[bool] = None
    numerals: Optional[bool] = None
    paragraphs: Optional[bool] = None
    profanity_filter: Optional[bool] = None
    punctuate: Optional[bool] = None
    redact: Optional[Union[List[str], bool, str]] = None
    replace: Optional[Union[list, str]] = None
    search: Optional[Union[list, str]] = None
    smart_format: Optional[bool] = None
    summarize: Optional[Union[bool, str]] = None
    tag: Optional[list] = None
    tier: Optional[str] = None
    utt_split: Optional[int] = None
    utterances: Optional[bool] = None
    version: Optional[str] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]
