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


# Projects


@dataclass_json
@dataclass
class Project:
    project_id: Optional[str] = ""
    name: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class ProjectsResponse:
    projects: Optional[List[Project]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["projects"] is not None:
            _dict["projects"] = [
                Project.from_dict(projects) for _, projects in _dict["projects"].items()
            ]
        return _dict[key]


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


@dataclass_json
@dataclass
class MembersResponse:
    members: Optional[List[Member]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["members"] is not None:
            _dict["members"] = [
                Member.from_dict(members) for _, members in _dict["members"].items()
            ]
        return _dict[key]


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
        if _dict["scopes"] is not None:
            _dict["scopes"] = [str(scopes) for _, scopes in _dict["scopes"].items()]
        return _dict[key]


@dataclass_json
@dataclass
class KeyResponse:
    api_key: Optional[Key] = None
    member: Optional[Member] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["api_key"] is not None:
            _dict["api_key"] = Key.from_dict(_dict["api_key"])
        if _dict["member"] is not None:
            _dict["member"] = Member.from_dict(_dict["member"])
        return _dict[key]


@dataclass_json
@dataclass
class KeysResponse:
    api_keys: Optional[List[KeyResponse]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["api_keys"] is not None:
            _dict["api_keys"] = [
                KeyResponse.from_dict(api_keys)
                for _, api_keys in _dict["api_keys"].items()
            ]
        return _dict[key]


# Scopes


@dataclass_json
@dataclass
class ScopesResponse:
    scopes: Optional[List[str]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["scopes"] is not None:
            _dict["scopes"] = [str(scopes) for _, scopes in _dict["scopes"].items()]
        return _dict[key]


# Invites


@dataclass_json
@dataclass
class Invite:
    email: Optional[str] = ""
    scope: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class InvitesResponse:
    invites: Optional[List[Invite]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["invites"] is not None:
            _dict["invites"] = [
                Invite.from_dict(invites) for _, invites in _dict["invites"].items()
            ]
        return _dict[key]


# Usage


@dataclass_json
@dataclass
class Config:
    language: Optional[str] = ""
    model: Optional[str] = ""
    punctuate: Optional[bool] = False
    utterances: Optional[bool] = False
    diarize: Optional[bool] = False

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


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

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["models"] is not None:
            _dict["models"] = [str(models) for _, models in _dict["models"].items()]
        if _dict["tags"] is not None:
            _dict["tags"] = [str(tags) for _, tags in _dict["tags"].items()]
        if _dict["features"] is not None:
            _dict["features"] = [
                str(features) for _, features in _dict["features"].items()
            ]
        if _dict["config"] is not None:
            _dict["config"] = Config.from_dict(_dict["config"])
        return _dict[key]


@dataclass_json
@dataclass
class Callback:
    attempts: Optional[int] = 0
    code: Optional[int] = 0
    completed: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Response:
    code: Optional[int] = 0
    completed: Optional[str] = ""
    details: Optional[Details] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["details"] is not None:
            _dict["details"] = Details.from_dict(_dict["details"])
        return _dict[key]


@dataclass_json
@dataclass
class UsageRequest:
    request_id: Optional[str] = ""
    created: Optional[str] = ""
    path: Optional[str] = ""
    api_key_id: Optional[str] = ""
    response: Optional[Response] = None
    callback: Optional[Callback] = None
    accessor: Optional[str] = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["response"] is not None:
            _dict["response"] = Response.from_dict(_dict["response"])
        if _dict["callback"] is not None:
            _dict["callback"] = Callback.from_dict(_dict["callback"])
        return _dict[key]


@dataclass_json
@dataclass
class UsageRequestsResponse:
    page: Optional[int] = 0
    limit: Optional[int] = 0
    requests: Optional[List[UsageRequest]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["requests"] is not None:
            _dict["requests"] = [
                UsageRequest.from_dict(requests)
                for _, requests in _dict["requests"].items()
            ]
        return _dict[key]


@dataclass_json
@dataclass
class Results:
    start: Optional[str] = ""
    end: Optional[str] = ""
    hours: Optional[int] = 0
    total_hours: Optional[int] = 0
    requests: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class Resolution:
    units: Optional[str] = ""
    amount: Optional[int] = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass_json
@dataclass
class UsageSummaryResponse:
    start: Optional[str] = ""
    end: Optional[str] = ""
    resolution: Optional[Resolution] = None
    results: Optional[List[Results]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["resolution"] is not None:
            _dict["resolution"] = Resolution.from_dict(_dict["resolution"])
        if _dict["results"] is not None:
            _dict["results"] = [
                Results.from_dict(results) for _, results in _dict["results"].items()
            ]
        return _dict[key]


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
        if _dict["tags"] is not None:
            _dict["tags"] = [str(tags) for _, tags in _dict["tags"].items()]
        if _dict["models"] is not None:
            _dict["models"] = [
                UsageModel.from_dict(models) for _, models in _dict["models"].items()
            ]
        if _dict["processing_methods"] is not None:
            _dict["processing_methods"] = [
                str(processing_methods)
                for _, processing_methods in _dict["processing_methods"].items()
            ]
        if _dict["features"] is not None:
            _dict["features"] = [
                str(features) for _, features in _dict["features"].items()
            ]
        if _dict["languages"] is not None:
            _dict["languages"] = [
                str(languages) for _, languages in _dict["languages"].items()
            ]
        return _dict[key]


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


@dataclass_json
@dataclass
class BalancesResponse:
    balances: Optional[List[Balance]] = None

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["balances"] is not None:
            _dict["balances"] = [
                Balance.from_dict(balances) for _, balances in _dict["balances"].items()
            ]
        return _dict[key]
