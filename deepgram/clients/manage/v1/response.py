# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from typing import TypedDict, List, Optional


# Result Message


@dataclass_json
@dataclass
class Message:
    message: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Projects


@dataclass_json
@dataclass
class Project:
    project_id: str = ""
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
class ProjectsResponse:
    projects: List[Project] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "projects" in _dict:
            _dict["projects"] = [
                Project.from_dict(projects) for projects in _dict["projects"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Members


@dataclass_json
@dataclass
class Member:
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    member_id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class MembersResponse:
    members: List[Member] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "members" in _dict:
            _dict["members"] = [
                Member.from_dict(members) for members in _dict["members"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Keys


@dataclass_json
@dataclass
class Key:
    api_key_id: str = ""
    comment: Optional[str] = ""
    created: str = ""
    scopes: List[str] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "scopes" in _dict:
            _dict["scopes"] = [str(scopes) for scopes in _dict["scopes"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class KeyResponse:
    api_key: Key = None
    member: Member = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "api_key" in _dict:
            _dict["api_key"] = Key.from_dict(_dict["api_key"])
        if "member" in _dict:
            _dict["member"] = Member.from_dict(_dict["member"])
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class KeysResponse:
    api_keys: List[KeyResponse] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "api_keys" in _dict:
            _dict["api_keys"] = [
                KeyResponse.from_dict(api_keys) for api_keys in _dict["api_keys"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Scopes


@dataclass_json
@dataclass
class ScopesResponse:
    scopes: List[str] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "scopes" in _dict:
            _dict["scopes"] = [str(scopes) for scopes in _dict["scopes"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Invites


@dataclass_json
@dataclass
class Invite:
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
class InvitesResponse:
    invites: List[Invite] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "invites" in _dict:
            _dict["invites"] = [
                Invite.from_dict(invites) for invites in _dict["invites"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Usage


@dataclass_json
@dataclass
class Config:
    language: str = ""
    model: str = ""
    punctuate: Optional[bool] = False
    utterances: Optional[bool] = False
    diarize: Optional[bool] = False
    smart_format: Optional[bool] = False
    interim_results: Optional[bool] = False

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Details:
    usd: float = 0
    duration: float = 0
    total_audio: float = 0
    channels: int = 0
    streams: int = 0
    method: str = ""
    models: List[str] = None
    tags: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    features: List[str] = None
    config: Config = None
    tier: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "models" in _dict:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if "tags" in _dict:
            _dict["tags"] = [str(tags) for tags in _dict["tags"]]
        if "features" in _dict:
            _dict["features"] = [str(features) for features in _dict["features"]]
        if "config" in _dict:
            _dict["config"] = Config.from_dict(_dict["config"])
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Callback:
    attempts: int = 0
    code: int = 0
    completed: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class TokenDetail:
    feature: str = ""
    input: int = 0
    model: str = ""
    output: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Response:
    code: int = 0
    completed: str = ""
    details: Details = None
    token_details: List[TokenDetail] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "details" in _dict:
            _dict["details"] = Details.from_dict(_dict["details"])
        if "token_details" in _dict:
            _dict["token_details"] = [
                TokenDetail.from_dict(token_details)
                for token_details in _dict["token_details"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageRequest:
    project_uuid: str = ""
    request_id: str = ""
    created: str = ""
    path: str = ""
    api_key_id: str = ""
    response: Response = None
    callback: Optional[Callback] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    accessor: Optional[str] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "response" in _dict:
            _dict["response"] = Response.from_dict(_dict["response"])
        if "callback" in _dict:
            _dict["callback"] = Callback.from_dict(_dict["callback"])
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageRequestsResponse:
    page: int = 0
    limit: int = 0
    requests: List[UsageRequest] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "requests" in _dict:
            _dict["requests"] = [
                UsageRequest.from_dict(requests) for requests in _dict["requests"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Tokens:
    tokens_in: int = 0
    out: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Results:
    start: str = ""
    end: str = ""
    hours: int = 0
    total_hours: int = 0
    requests: int = 0
    tokens: Tokens = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "tokens" in _dict:
            _dict["tokens"] = [Tokens.from_dict(tokens) for tokens in _dict["tokens"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class Resolution:
    units: str = ""
    amount: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageSummaryResponse:
    start: str = ""
    end: str = ""
    resolution: Resolution = None
    results: List[Results] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "resolution" in _dict:
            _dict["resolution"] = Resolution.from_dict(_dict["resolution"])
        if "results" in _dict:
            _dict["results"] = [
                Results.from_dict(results) for results in _dict["results"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageModel:
    name: str = ""
    language: str = ""
    version: str = ""
    model_id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class UsageFieldsResponse:
    tags: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )
    models: List[UsageModel] = None
    processing_methods: List[str] = None
    features: List[str] = None
    languages: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "tags" in _dict:
            _dict["tags"] = [str(tags) for tags in _dict["tags"]]
        if "models" in _dict:
            _dict["models"] = [
                UsageModel.from_dict(models) for models in _dict["models"]
            ]
        if "processing_methods" in _dict:
            _dict["processing_methods"] = [
                str(processing_methods)
                for processing_methods in _dict["processing_methods"]
            ]
        if "features" in _dict:
            _dict["features"] = [str(features) for features in _dict["features"]]
        if "languages" in _dict:
            _dict["languages"] = [str(languages) for languages in _dict["languages"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Billing


@dataclass_json
@dataclass
class Balance:
    balance_id: str = ""
    amount: str = ""
    units: str = ""
    purchase_order_id: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass_json
@dataclass
class BalancesResponse:
    balances: List[Balance] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "balances" in _dict:
            _dict["balances"] = [
                Balance.from_dict(balances) for balances in _dict["balances"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)
