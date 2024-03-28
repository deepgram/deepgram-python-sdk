# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import List, Optional, Union
import logging, verboselogs


@dataclass_json
@dataclass
class LiveOptions:
    """
    Live Transcription Options for the Deepgram Platform.

    Please see the documentation for more information on each option:
    https://developers.deepgram.com/reference/streaming
    """

    alternatives: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    callback: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    channels: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    diarize_version: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    encoding: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    endpointing: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    extra: Optional[Union[list, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    filler_words: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    interim_results: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    keywords: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    redact: Optional[Union[List[str], bool, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    replace: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sample_rate: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    search: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    tag: Optional[list] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    tier: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    utterance_end_ms: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    vad_events: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    version: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)

    def check(self):
        verboselogs.install()
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(logging.ERROR)

        if self.tier:
            logger.error(
                "WARNING: Tier is deprecated. Will be removed in a future version."
            )

        logger.setLevel(prev)

        return True
