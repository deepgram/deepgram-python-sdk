# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from io import BufferedReader
from typing import Union, Optional
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from .....utils import verboselogs
from ....common import BaseResponse


@dataclass
class SpeakWSOptions(BaseResponse):
    """
    Contains all the options for the SpeakOptions.

    Reference:
    https://developers.deepgram.com/reference/transform-text-to-speech-websocket
    """

    model: Optional[str] = field(
        default="aura-asteria-en",
        metadata=dataclass_config(exclude=lambda f: f is None),
    )
    encoding: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    # container: Optional[str] = field(
    #     default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    # )
    sample_rate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    bit_rate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)

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
