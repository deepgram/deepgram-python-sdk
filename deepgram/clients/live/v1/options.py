# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional
import logging, verboselogs


@dataclass_json
@dataclass
class LiveOptions:
    """
    Live Transcription Options for the Deepgram Platform.

    Please see the documentation for more information on each option:
    https://developers.deepgram.com/reference/streaming
    """

    alternatives: Optional[int] = None
    callback: Optional[str] = None
    callback_method: Optional[str] = None
    channels: Optional[int] = None
    diarize: Optional[bool] = None
    diarize_version: Optional[str] = None
    encoding: Optional[str] = None
    endpointing: Optional[str] = None
    extra: Optional[str] = None
    filler_words: Optional[bool] = None
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
    utterance_end_ms: Optional[str] = None
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
