# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT


from typing import Optional
import io

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

# Speak Response Types:


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


@dataclass
class WarningResponse(DataClassJsonMixin):
    """
    Warning Message from the Deepgram Platform
    """

    warn_code: str = ""
    warn_msg: str = ""
    type: str = ""

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
