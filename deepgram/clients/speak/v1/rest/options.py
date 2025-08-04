# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from io import BufferedReader
from typing import Union, Optional
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from .....utils import verboselogs
from ....common import TextSource, BufferSource, StreamSource, FileSource, BaseResponse


@dataclass
class SpeakRESTOptions(BaseResponse):
    """
    Contains all the options for the SpeakOptions.

    Reference:
    https://developers.deepgram.com/reference/text-to-speech-api
    """

    model: Optional[str] = field(
        default="aura-2-thalia-en",
        metadata=dataclass_config(exclude=lambda f: f is None),
    )
    encoding: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    container: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sample_rate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    bit_rate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    mip_opt_out: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def check(self):
        """
        Check the SpeakOptions for any missing or invalid values.
        """
        logger = verboselogs.VerboseLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(verboselogs.ERROR)

        # no op at the moment

        logger.setLevel(prev)

        return True


SpeakOptions = SpeakRESTOptions


# unqiue
SpeakSource = Union[FileSource, BufferedReader]
SpeakRestSource = SpeakSource
SpeakRESTSource = SpeakSource  # pylint: disable=invalid-name
