# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Union
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from deepgram.utils import verboselogs

from ....common import BaseResponse


@dataclass
class LiveOptions(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Live Transcription Options for the Deepgram Platform.

    Please see the documentation for more information on each option:
    https://developers.deepgram.com/reference/streaming
    """

    alternatives: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    callback: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    channels: Optional[int] = field(
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
    # pylint: disable=W0511
    # TODO: endpointing's current type previous was `Optional[str]` which is incorrect
    # for backward compatibility we are keeping it as `Optional[Union[str, bool, int]]`
    # since it gets translated to a string to be placed as a query parameter, will keep `str` for now
    # but will change this to `Optional[Union[bool, int]]` in a future release
    endpointing: Optional[Union[str, bool, int]] = field(
        default=None,
        metadata=dataclass_config(exclude=lambda f: f is None),
    )
    # pylint: enable=W0511
    extra: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    filler_words: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    interim_results: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    keywords: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default="nova-2", metadata=dataclass_config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    no_delay: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
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
    smart_format: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tag: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tier: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utterance_end_ms: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    vad_events: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    version: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def check(self):
        """
        Check the options for any deprecated or soon-to-be-deprecated options.
        """
        logger = verboselogs.VerboseLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(verboselogs.ERROR)

        if self.tier:
            logger.warning(
                "WARNING: Tier is deprecated. Will be removed in a future version."
            )

        if isinstance(self.endpointing, str):
            logger.warning(
                "WARNING: endpointing's current type previous was `Optional[str]` which is incorrect"
                " for backward compatibility we are keeping it as `Optional[Union[str, bool, int]]`"
                " since it gets translated to a string to be placed as a query parameter, will keep `str` for now"
                " but will change this to `Optional[Union[bool, int]]` in a future release"
            )

        logger.setLevel(prev)

        return True


ListenWebSocketOptions = LiveOptions
