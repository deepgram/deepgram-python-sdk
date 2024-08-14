# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin

# Input


@dataclass
class ProjectOptions(DataClassJsonMixin):
    """
    Project Options
    """

    name: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class ModelOptions(DataClassJsonMixin):
    """
    Model Options
    """

    include_outdated: bool = False

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class KeyOptions(DataClassJsonMixin):
    """
    Key Options
    """

    comment: Optional[str] = ""
    expiration_date: Optional[str] = field(
        default="", metadata=dataclass_config(exclude=lambda f: f == "")
    )
    time_to_live_in_seconds: Optional[int] = field(
        default=-1, metadata=dataclass_config(exclude=lambda f: f == -1)
    )
    scopes: List[str] = field(default_factory=list)
    tags: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["scopes"] is not None:
            _dict["scopes"] = [str(scopes) for scopes in _dict["scopes"]]
        if _dict["tags"] is not None:
            _dict["tags"] = [str(tags) for tags in _dict["tags"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class ScopeOptions(DataClassJsonMixin):
    """
    Scope Options
    """

    scope: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class InviteOptions(DataClassJsonMixin):
    """
    Invite Options
    """

    email: str = ""
    scope: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class UsageRequestOptions(DataClassJsonMixin):
    """
    Usage Request Options
    """

    start: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    end: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    limit: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    status: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class UsageSummaryOptions(
    DataClassJsonMixin
):  # pylint: disable=too-many-instance-attributes
    """
    Usage Summary Options
    """

    start: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    end: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    accessor: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tag: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    method: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    interim_results: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    ner: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utterances: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    replace: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    keywords: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    detect_topics: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    search: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    redact: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    alternatives: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class UsageFieldsOptions(DataClassJsonMixin):
    """
    Usage Fields Options
    """

    start: Optional[str] = ""
    end: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
