# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Optional, Dict, Any
import io

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin


# Base Classes:


@dataclass
class BaseResponse(DataClassJsonMixin):
    """
    BaseResponse class used to define the common methods and properties for all response classes.
    """

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)

    def eval(self, key: str) -> str:
        """
        This method is used to evaluate a key in the response object using a dot notation style method.
        """
        keys = key.split(".")
        result: Dict[Any, Any] = self.to_dict()
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            elif isinstance(result, list) and k.isdigit() and int(k) < len(result):
                result = result[int(k)]
            else:
                return ""
        return str(result)


# Speak Response Types:


@dataclass
class SpeakRESTResponse(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    A class for representing a response from the speak endpoint.
    """

    content_type: str = ""
    request_id: str = ""
    model_uuid: str = ""
    model_name: str = ""
    characters: int = 0
    transfer_encoding: str = ""
    date: str = ""
    filename: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    # pylint: disable=W0511
    # TODO: stream will be deprecated in a future release. Please use stream_memory instead.
    stream: Optional[io.BytesIO] = field(
        default=None,
        metadata=dataclass_config(exclude=lambda f: True),
    )
    # pylint: enable=W0511
    stream_memory: Optional[io.BytesIO] = field(
        default=None,
        metadata=dataclass_config(exclude=lambda f: True),
    )


@dataclass
class OpenResponse(BaseResponse):
    """
    Open Message from the Deepgram Platform
    """

    type: str = ""


@dataclass
class MetadataResponse(BaseResponse):
    """
    Metadata object
    """

    request_id: str = ""


@dataclass
class FlushedResponse(BaseResponse):
    """
    Flushed Message from the Deepgram Platform
    """

    type: str = ""


@dataclass
class CloseResponse(BaseResponse):
    """
    Close Message from the Deepgram Platform
    """

    type: str = ""


@dataclass
class ErrorResponse(BaseResponse):
    """
    Error Message from the Deepgram Platform
    """

    description: str = ""
    message: str = ""
    type: str = ""
    variant: Optional[str] = ""


# Unhandled Message


@dataclass
class UnhandledResponse(BaseResponse):
    """
    Unhandled Message from the Deepgram Platform
    """

    type: str = ""
    raw: str = ""
