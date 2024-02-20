# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from io import BufferedReader
from typing import Union, List, TypedDict, Optional
import logging, verboselogs


@dataclass_json
@dataclass
class SpeakOptions:
    """
    Contains all the options for the SpeakOptions.

    Reference:
    https://developers.deepgram.com/reference/text-to-speech-preview-api
    """

    model: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    encoding: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    container: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    sample_rate: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    bit_rate: Optional[int] = field(
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


class SpeakStreamSource(TypedDict):
    """
    Represents a data source for reading binary data from a stream-like source.

    This class is used to specify a source of binary data that can be read from
    a stream, such as an audio file in .wav format.

    Attributes:
        stream (BufferedReader): A BufferedReader object for reading binary data.
    """

    stream: BufferedReader


class TextSource(TypedDict):
    """
    Represents a data source for reading binary data from a text-like source.

    This class is used to specify a source of text data that can be read from.

    Attributes:
        text (str): A string for reading text data.
    """

    text: str


SpeakSource = Union[TextSource, SpeakStreamSource]
