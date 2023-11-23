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
    message: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

# Projects

@dataclass_json
@dataclass
class Project:
    project_id: Optional[str]
    name: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class ProjectsResponse:
    projects: Optional[List[Project]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["projects"] is not None:
            _dict["projects"] = [Project.from_dict(project) for project in _dict["projects"]]
        return _dict[key]

class ProjectOptions(TypedDict, total=False):
    name: Optional[str]

# Members

@dataclass_json
@dataclass
class Member:
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    member_id: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class MembersResponse:
    members: Optional[List[Member]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["members"] is not None:
            _dict["members"] = [Member.from_dict(member) for member in _dict["members"]]
        return _dict[key]

# Keys
@dataclass_json
@dataclass
class Key:
    api_key_id: Optional[str]
    comment: Optional[str]
    created: Optional[str]
    scopes: Optional[List[str]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class KeyResponse:
    api_key: Optional[Key]
    member: Optional[Member]

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
    api_keys: Optional[List[KeyResponse]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["api_keys"] is not None:
            _dict["api_keys"] = [KeyResponse.from_dict(key) for key in _dict["api_keys"]]
        return _dict[key]

class KeyOptions(TypedDict):
    comment: Optional[str]
    scopes: Optional[List[str]]
    tags: Optional[List[str]]
    time_to_live_in_seconds: Optional[int]
    expiration_date: Optional[datetime]

# Scopes
@dataclass_json
@dataclass
class ScopesResponse:
    scopes: List[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

class ScopeOptions(TypedDict):
    scope: str

# Invites

@dataclass_json
@dataclass
class Invite:
    email: Optional[str]
    scope: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class InvitesResponse:
    invites: List[Invite]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["invites"] is not None:
            _dict["invites"] = [Invite.from_dict(invite) for invite in _dict["invites"]]
        return _dict[key]

class InviteOptions:
    email: Optional[str]
    scope: Optional[str]
    
# Usage
@dataclass_json
@dataclass
class Config:
    # diarize: Optional[bool]
    # language: Optional[str]
    # model: Optional[str]
    # punctuate: Optional[bool]
    # utterances: Optional[bool]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class Details:
    usd: Optional[float]
    duration: Optional[float]
    total_audio: Optional[float]
    channels: Optional[int]
    streams: Optional[int]
    models: List[str]
    method: Optional[str]
    tags: Optional[List[str]]
    features: Optional[List[str]]
    config: Optional[Config]

    def __getitem__(self, key):
        _dict = self.to_dict()
        # if _dict["config"] is not None:
        #     _dict["config"] = Config.from_dict(_dict["config"])
        return _dict[key]

@dataclass_json
@dataclass
class Callback:
    attempts: Optional[int]
    code: Optional[int]
    completed: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class Response:
    details: Optional[Details]
    code: Optional[int]
    completed: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["details"] is not None:
            _dict["details"] = Details.from_dict(_dict["details"])
        return _dict[key]

@dataclass_json
@dataclass
class UsageRequest:
    request_id: Optional[str]
    created: Optional[str]
    path: Optional[str]
    # accessor: Optional[str]
    api_key_id: Optional[str]
    response: Optional[Response]
    # callback: Optional[Callback]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["response"] is not None:
            _dict["response"] = Response.from_dict(_dict["response"])
        # if _dict["callback"] is not None:
        #     _dict["callback"] = Callback.from_dict(_dict["callback"])
        return _dict[key]

@dataclass_json
@dataclass
class UsageRequestsResponse:
    page: Optional[int]
    limit: Optional[int]
    requests: List[UsageRequest]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["requests"] is not None:
            _dict["requests"] = [UsageRequest.from_dict(request) for request in _dict["requests"]]
        return _dict[key]

class UsageRequestOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]
    limit: Optional[int]
    status: Optional[str]

class UsageSummaryOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]
    accessor: Optional[str]
    tag: Optional[str]
    method: Optional[str]
    model: Optional[str]
    multichannel: Optional[bool]
    interim_results: Optional[bool]
    punctuate: Optional[bool]
    ner: Optional[bool]
    utterances: Optional[bool]
    replace: Optional[bool]
    profanity_filter: Optional[bool]
    keywords: Optional[bool]
    detect_topics: Optional[bool]
    diarize: Optional[bool]
    search: Optional[bool]
    redact: Optional[bool]
    alternatives: Optional[bool]
    numerals: Optional[bool]
    smart_format: Optional[bool]

@dataclass_json
@dataclass
class Results:
    start: Optional[str]
    end: Optional[str]
    hours: Optional[int]
    total_hours: Optional[int]
    requests: Optional[int]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class Resolution:
    units: Optional[str]
    amount: Optional[int]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class UsageSummaryResponse:
    start: Optional[str]
    end: Optional[str]
    resolution: Optional[Resolution]
    results: Optional[List[Results]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["resolution"] is not None:
            _dict["resolution"] = Resolution.from_dict(_dict["resolution"])
        if _dict["results"] is not None:
            _dict["results"] = [Results.from_dict(result) for result in _dict["results"]]
        return _dict[key]

@dataclass_json
@dataclass
class UsageModel:
    name: Optional[str]
    language: Optional[str]
    version: Optional[str]
    model_id: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class UsageFieldsResponse:
    tags: Optional[List[str]]
    models: Optional[List[UsageModel]]
    processing_methods: Optional[List[str]]
    # languages: Optional[List[str]]
    features: Optional[List[str]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["models"] is not None:
            _dict["models"] = [UsageModel.from_dict(model) for model in _dict["models"]]
        return _dict[key]

class UsageFieldsOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]

# Billing

@dataclass_json
@dataclass
class Balance:
    balance_id: Optional[str]
    amount: Optional[str]
    units: Optional[str]
    purchase_order_id: Optional[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

@dataclass_json
@dataclass
class BalancesResponse:
    balances: Optional[List[Balance]]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if _dict["balances"] is not None:
            _dict["balances"] = [Balance.from_dict(balance) for balance in _dict["balances"]]
        return _dict[key]