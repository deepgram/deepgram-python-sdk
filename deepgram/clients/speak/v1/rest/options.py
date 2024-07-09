# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from io import BufferedReader
from typing import Union

from ....common import FileSource
from ..options import SpeakOptions


SpeakRESTOptions = SpeakOptions

SpeakSource = Union[FileSource, BufferedReader]
SpeakRestSource = SpeakSource
