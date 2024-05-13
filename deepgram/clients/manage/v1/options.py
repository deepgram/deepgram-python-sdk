# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from typing import TypedDict, List, Optional

# Input


@dataclass_json
@dataclass
class ProjectOptions:
    name: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class KeyOptions:
    comment: Optional[str] = ""
    expiration_date: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    time_to_live_in_seconds: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    expiration_date: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    scopes: List[str] = None
    tags: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
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


@dataclass_json
@dataclass
class ScopeOptions:
    scope: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class InviteOptions:
    email: str = ""
    scope: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageRequestOptions:
    start: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    end: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    limit: Optional[int] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    status: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageSummaryOptions:
    start: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    end: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    accessor: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    tag: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    method: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    model: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    multichannel: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    interim_results: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    punctuate: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    ner: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    utterances: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    replace: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    profanity_filter: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    keywords: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    detect_topics: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    search: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    redact: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    alternatives: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    numerals: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageFieldsOptions:
    start: Optional[str] = ""
    end: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
