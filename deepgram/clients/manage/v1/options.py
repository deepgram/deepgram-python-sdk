# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import TypedDict, List, Optional

# Input


@dataclass_json
@dataclass
class ProjectOptions:
    name: Optional[str] = ""

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
    time_to_live_in_seconds: Optional[int] = 0
    expiration_date: Optional[str] = ""
    scopes: Optional[List[str]] = None
    tags: Optional[List[str]] = None

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
    scope: Optional[str] = ""

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
    email: Optional[str] = ""
    scope: Optional[str] = ""

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
    start: Optional[str] = ""
    end: Optional[str] = ""
    limit: Optional[int] = 0
    status: Optional[str] = ""

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
    start: Optional[str] = ""
    end: Optional[str] = ""
    accessor: Optional[str] = ""
    tag: Optional[str] = ""
    method: Optional[str] = ""
    model: Optional[str] = ""
    multichannel: Optional[bool] = False
    interim_results: Optional[bool] = False
    punctuate: Optional[bool] = False
    ner: Optional[bool] = False
    utterances: Optional[bool] = False
    replace: Optional[bool] = False
    profanity_filter: Optional[bool] = False
    keywords: Optional[bool] = False
    detect_topics: Optional[bool] = False
    diarize: Optional[bool] = False
    search: Optional[bool] = False
    redact: Optional[bool] = False
    alternatives: Optional[bool] = False
    numerals: Optional[bool] = False
    smart_format: Optional[bool] = False

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
