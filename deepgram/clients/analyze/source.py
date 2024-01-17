# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Union
from io import BufferedReader
from typing_extensions import TypedDict


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
