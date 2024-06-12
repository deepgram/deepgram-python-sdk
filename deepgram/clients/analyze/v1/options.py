# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import logging
from typing import List, Union, Optional

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

from ....utils import verboselogs
from ...common import FileSource, StreamSource, UrlSource


@dataclass
class AnalyzeOptions(
    DataClassJsonMixin
):  # pylint: disable=too-many-instance-attributes
    """
    Contains all the options for the AnalyzeOptions.

    Reference:
    https://developers.deepgram.com/reference/text-intelligence-apis
    """

    callback: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    callback_method: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_intent: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_intent_mode: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_topic: Optional[Union[List[str], str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    custom_topic_mode: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    language: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summarize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics: Optional[bool] = field(
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
        Check the options for the AnalyzeOptions.
        """
        logger = verboselogs.VerboseLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(verboselogs.ERROR)

        # no op at the moment

        logger.setLevel(prev)

        return True


AnalyzeStreamSource = StreamSource

# FileSource = FileSource
# UrlSource = UrlSource
AnalyzeSource = Union[FileSource, UrlSource, AnalyzeStreamSource]
