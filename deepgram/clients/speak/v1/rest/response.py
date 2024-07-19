# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT


from typing import Optional
import io

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

# Speak Response Types:


@dataclass
class SpeakRESTResponse(
    DataClassJsonMixin
):  # pylint: disable=too-many-instance-attributes
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

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    # this is a hack to make the response look like a dict because of the io.BytesIO object
    # otherwise it will throw an exception on printing
    def __str__(self) -> str:
        my_dict = self.to_dict()
        return my_dict.__str__()


@dataclass
class OpenResponse(DataClassJsonMixin):
    """
    Open Message from the Deepgram Platform
    """

    type: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class MetadataResponse(DataClassJsonMixin):
    """
    Metadata object
    """

    request_id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class FlushedResponse(DataClassJsonMixin):
    """
    Flushed Message from the Deepgram Platform
    """

    type: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class CloseResponse(DataClassJsonMixin):
    """
    Close Message from the Deepgram Platform
    """

    type: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class ErrorResponse(DataClassJsonMixin):
    """
    Error Message from the Deepgram Platform
    """

    description: str = ""
    message: str = ""
    type: str = ""
    variant: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Unhandled Message


@dataclass
class UnhandledResponse(DataClassJsonMixin):
    """
    Unhandled Message from the Deepgram Platform
    """

    type: str = ""
    raw: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
