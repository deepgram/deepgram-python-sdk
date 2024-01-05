# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Union, List, TypedDict, Optional
import logging, verboselogs


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
    callback_method: Optional[str] = None
    detect_entities: Optional[bool] = None
    detect_language: Optional[bool] = None
    detect_topics: Optional[bool] = None
    diarize: Optional[bool] = None
    diarize_version: Optional[str] = None
    dictation: Optional[bool] = None
    extra: Optional[str] = None
    filler_words: Optional[bool] = None
    keywords: Optional[Union[list, str]] = None
    language: Optional[str] = None
    measurements: Optional[bool] = None
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

    def check(self):
        verboselogs.install()
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(logging.ERROR)

        if self.numerals:
            logger.error(
                "WARNING: Numerals is deprecated. Will be removed in a future version. Please use smart_format instead."
            )
        if self.tier:
            logger.error(
                "WARNING: Tier is deprecated. Will be removed in a future version."
            )

        logger.setLevel(prev)

        return True
