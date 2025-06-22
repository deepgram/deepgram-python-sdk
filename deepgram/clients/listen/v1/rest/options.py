# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Union, List, Optional
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from deepgram.utils import verboselogs
from ....common import (
    TextSource,
    StreamSource,
    BufferSource,
    FileSource,
    UrlSource,
    BaseResponse,
)


@dataclass
class PrerecordedOptions(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Contains all the options for the PrerecordedClient.

    Reference:
    https://developers.deepgram.com/reference/pre-recorded
    """

    alternatives: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    channels: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    callback: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_intent: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_intent_mode: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_topic: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_topic_mode: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    detect_entities: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    detect_language: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    detect_topics: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    diarize_version: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    dictation: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    encoding: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    extra: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    filler_words: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    keyterm: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    keywords: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    measurements: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    paragraphs: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    redact: Optional[Union[List[str], bool, str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    replace: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sample_rate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    search: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summarize: Optional[Union[bool, str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tag: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tier: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utt_split: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utterances: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    version: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def check(self):
        """
        Check the options for any deprecated fields or values.
        """
        logger = verboselogs.VerboseLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(verboselogs.ERROR)

        if self.tier:
            logger.error(
                "WARNING: Tier is deprecated. Will be removed in a future version."
            )

        logger.setLevel(prev)

        return True


ListenRESTOptions = PrerecordedOptions

# unique
PrerecordedSource = Union[UrlSource, FileSource]
ListenRestSource = PrerecordedSource

# PrerecordedSource for backwards compatibility
PreRecordedStreamSource = StreamSource
