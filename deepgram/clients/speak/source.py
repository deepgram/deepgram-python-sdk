# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Union
from io import BufferedReader
from typing_extensions import TypedDict


class TextSource(TypedDict):
    """
    Represents a data source for reading binary data from a text-like source.

    This class is used to specify a source of text data that can be read from.

    Attributes:
        text (str): A string for reading text data.
    """

    text: str


SpeakSource = Union[TextSource]
