# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import TypedDict, List, Optional


# Result Message


@dataclass_json
@dataclass
class Message:
    message: Optional[str] = ""

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
    project_id: Optional[str] = ""
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
class ProjectsResponse:
    projects: Optional[List[Project]] = None

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
    email: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    member_id: Optional[str] = ""

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
    members: Optional[List[Member]] = None

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
    api_key_id: Optional[str] = ""
    comment: Optional[str] = ""
    created: Optional[str] = ""
    scopes: Optional[List[str]] = None

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
    api_key: Optional[Key] = None
    member: Optional[Member] = None

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
    api_keys: Optional[List[KeyResponse]] = None

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
    scopes: Optional[List[str]] = None

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
class InvitesResponse:
    invites: Optional[List[Invite]] = None

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
    language: Optional[str] = ""
    model: Optional[str] = ""
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
    usd: Optional[float] = 0
    duration: Optional[float] = 0
    total_audio: Optional[float] = 0
    channels: Optional[int] = 0
    streams: Optional[int] = 0
    method: Optional[str] = ""
    models: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    features: Optional[List[str]] = None
    config: Optional[Config] = None
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
    attempts: Optional[int] = 0
    code: Optional[int] = 0
    completed: Optional[str] = ""

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
    feature: Optional[str] = ""
    input: Optional[int] = 0
    model: Optional[str] = ""
    output: Optional[int] = 0

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
    code: Optional[int] = 0
    completed: Optional[str] = ""
    details: Optional[Details] = None
    token_details: Optional[List[TokenDetail]] = None

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
    project_uuid: Optional[str] = ""
    request_id: Optional[str] = ""
    created: Optional[str] = ""
    path: Optional[str] = ""
    api_key_id: Optional[str] = ""
    response: Optional[Response] = None
    callback: Optional[Callback] = None
    accessor: Optional[str] = ""

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
    page: Optional[int] = 0
    limit: Optional[int] = 0
    requests: Optional[List[UsageRequest]] = None

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
    tokens_in: Optional[int] = 0
    out: Optional[int] = 0

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
    start: Optional[str] = ""
    end: Optional[str] = ""
    hours: Optional[int] = 0
    total_hours: Optional[int] = 0
    requests: Optional[int] = 0
    tokens: Optional[Tokens] = None

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
    units: Optional[str] = ""
    amount: Optional[int] = 0

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
    start: Optional[str] = ""
    end: Optional[str] = ""
    resolution: Optional[Resolution] = None
    results: Optional[List[Results]] = None

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
    name: Optional[str] = ""
    language: Optional[str] = ""
    version: Optional[str] = ""
    model_id: Optional[str] = ""

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
    tags: Optional[List[str]] = None
    models: Optional[List[UsageModel]] = None
    processing_methods: Optional[List[str]] = None
    features: Optional[List[str]] = None
    languages: Optional[List[str]] = None

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
    balance_id: Optional[str] = ""
    amount: Optional[str] = ""
    units: Optional[str] = ""
    purchase_order_id: Optional[str] = ""

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
    balances: Optional[List[Balance]] = None

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
