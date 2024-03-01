# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from io import BufferedReader
from typing import Union, Optional
from typing_extensions import TypedDict
import logging, verboselogs


@dataclass_json
@dataclass
class AnalyzeOptions:
    """
    Contains all the options for the AnalyzeOptions.

    Reference:
    https://developers.deepgram.com/reference/text-intelligence-apis
    """

    callback: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_intent: Optional[Union[list, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_intent_mode: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_topic: Optional[Union[list, str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    custom_topic_mode: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    intents: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sentiment: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    summarize: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    topics: Optional[bool] = field(
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

        # no op at the moment

        logger.setLevel(prev)

        return True


class AnalyzeStreamSource(TypedDict):
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


AnalyzeSource = Union[UrlSource, BufferSource, AnalyzeStreamSource]
TextSource = Union[BufferSource, AnalyzeStreamSource]
