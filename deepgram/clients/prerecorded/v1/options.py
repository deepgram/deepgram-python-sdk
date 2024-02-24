# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from io import BufferedReader
from typing import Union, List, Optional
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
    custom_intent: Optional[Union[list, str]] = None
    custom_intent_mode: Optional[str] = None
    custom_topics: Optional[Union[list, str]] = None
    custom_topic_mode: Optional[str] = None
    detect_entities: Optional[bool] = None
    detect_language: Optional[bool] = None
    detect_topics: Optional[bool] = None
    diarize: Optional[bool] = None
    diarize_version: Optional[str] = None
    dictation: Optional[bool] = None
    extra: Optional[Union[list, str]] = None
    filler_words: Optional[bool] = None
    intents: Optional[bool] = None
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
    sentiment: Optional[bool] = None
    smart_format: Optional[bool] = None
    summarize: Optional[Union[bool, str]] = None
    tag: Optional[list] = None
    tier: Optional[str] = None
    topics: Optional[bool] = None
    utt_split: Optional[int] = None
    utterances: Optional[bool] = None
    version: Optional[str] = None

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


@dataclass_json
@dataclass
class StreamSource:
    """
    Represents a data source for reading binary data from a stream-like source.

    This class is used to specify a source of binary data that can be read from
    a stream, such as an audio file in .wav format.

    Attributes:
        stream (BufferedReader): A BufferedReader object for reading binary data.
    """

    stream: BufferedReader

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UrlSource:
    """
    Represents a data source for specifying the location of a file via a URL.

    This class is used to specify a hosted file URL, typically pointing to an
    externally hosted file, such as an audio file hosted on a server or the internet.

    Attributes:
        url (str): The URL pointing to the hosted file.
    """

    url: str

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class BufferSource:
    """
    Represents a data source for handling raw binary data.

    This class is used to specify raw binary data, such as audio data in its
    binary form, which can be captured from a microphone or generated synthetically.

    Attributes:
        buffer (bytes): The binary data.
    """

    buffer: bytes

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


PrerecordedSource = Union[UrlSource, BufferSource, StreamSource]
FileSource = Union[BufferSource, StreamSource]
