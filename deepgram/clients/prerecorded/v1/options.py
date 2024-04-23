# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from io import BufferedReader
from typing import Union, List, Optional
from typing_extensions import TypedDict
import logging, verboselogs


@dataclass_json
@dataclass
class PrerecordedOptions:
    """
    Contains all the options for the PrerecordedClient.

    Reference:
    https://developers.deepgram.com/reference/pre-recorded
    """

    alternatives: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    channels: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    callback: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_intent: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_intent_mode: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_topics: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_topic_mode: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    detect_entities: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    detect_language: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    detect_topics: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    diarize_version: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    dictation: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    encoding: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    extra: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    filler_words: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    intents: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    keywords: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    measurements: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default="nova-2", metadata=config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    paragraphs: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    redact: Optional[Union[List[str], bool, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    replace: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sample_rate: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    search: Optional[Union[List[str], str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    summarize: Optional[Union[bool, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    tag: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    tier: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    utt_split: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    utterances: Optional[bool] = field(
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


class ReadStreamSource(TypedDict):
    """
    Represents a data source for reading binary data from a stream-like source.

    This class is used to specify a source of binary data that can be read from
    a stream, such as an audio file in .wav format.

    Attributes:
        stream (BufferedReader): A BufferedReader object for reading binary data.
    """

    stream: BufferedReader


class UrlSource(TypedDict):
    """
    Represents a data source for specifying the location of a file via a URL.

    This class is used to specify a hosted file URL, typically pointing to an
    externally hosted file, such as an audio file hosted on a server or the internet.

    Attributes:
        url (str): The URL pointing to the hosted file.
    """

    url: str


class BufferSource(TypedDict):
    """
    Represents a data source for handling raw binary data.

    This class is used to specify raw binary data, such as audio data in its
    binary form, which can be captured from a microphone or generated synthetically.

    Attributes:
        buffer (bytes): The binary data.
    """

    buffer: bytes


PrerecordedSource = Union[UrlSource, BufferSource, ReadStreamSource]
FileSource = Union[BufferSource, ReadStreamSource]
