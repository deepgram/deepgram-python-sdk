from datetime import datetime
from typing import TypedDict, List, Optional, Dict

class Message(TypedDict):
   message: str

# Projects

class Project(TypedDict):
    project_id: str
    name: str

class ProjectsResponse(TypedDict):
    projects: List[Project]

class ProjectOptions(TypedDict, total=False):
    name: Optional[str]
    company: Optional[str]

# Members

class Member(TypedDict):
    email: str
    first_name: str
    last_name: str
    member_id: str
    scopes: List[str]

class MembersResponse(TypedDict):
    projects: List[Member]

# Keys

class ApiKey(TypedDict):
    api_key_id: str
    comment: Optional[str]
    created: datetime
    scopes: List[str]
    tags: Optional[List[str]]

class Key(TypedDict):
    api_key: ApiKey
    member: Member

class KeysResponse(TypedDict):
    api_keys: List[Key]

class CreateKeyResponse(TypedDict):
    api_key_id: str
    key: str
    comment: Optional[str]
    created: datetime
    scopes: List[str]
    tags: Optional[List[str]]

class KeyOptions(TypedDict):
    comment: str
    scopes: List[str]
    tags: Optional[List[str]]
    time_to_live_in_seconds: Optional[int]
    expiration_date: Optional[datetime]

# Scopes

class ScopesResponse(TypedDict):
    scopes: List[str]

class ScopeOptions(TypedDict):
    scope: str

# Invites

class Invite(TypedDict):
    email: str
    scope: str

class InvitesResponse(TypedDict):
    projects: List[Invite]

class InviteOptions(TypedDict):
    email: str
    scope: str

# Usage

class Config(TypedDict, total=False):
    alternatives: Optional[int]
    callback: Optional[str]
    diarize: Optional[bool]
    keywords: Optional[List[str]]
    language: Optional[str]
    model: Optional[str]
    multichannel: Optional[bool]
    ner: Optional[bool]
    numerals: Optional[bool]
    profanity_filter: Optional[bool]
    punctuate: Optional[bool]
    redact: Optional[List[str]]
    search: Optional[List[str]]
    utterances: Optional[bool]

class Details(TypedDict, total=False):
    usd: Optional[float]
    duration: Optional[float]
    total_audio: Optional[float]
    channels: Optional[float]
    streams: Optional[float]
    models: List[str]
    method: Optional[str]
    tags: Optional[List[str]]
    features: Optional[List[str]]
    config: Config

class Callback(TypedDict):
    attempts: Optional[int]
    code: Optional[int]
    completed: Optional[str]

class Response(TypedDict, total=False):
    details: Details
    code: Optional[int]
    completed: Optional[str]

class UsageRequest(TypedDict):
    request_id: str
    created: str
    path: str
    api_key_id: str
    response: Response
    callback: Optional[Callback]

class UsageRequestsResponse(TypedDict):
    page: int
    limit: int
    requests: List[UsageRequest]

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

class UsageSummary(TypedDict):
    start: str
    end: str
    hours: int
    total_hours: int
    requests: int

class Resolution(TypedDict):
    units: str
    amount: int

class UsageSummaryResponse(TypedDict):
    start: str
    end: str
    resolution: Resolution
    results: List[UsageSummary]

class UsageModel(TypedDict):
    name: str
    language: str
    version: str
    model_id: str

class UsageFieldsResponse(TypedDict):
    tags: List[str]
    models: List[UsageModel]
    processing_methods: List[str]
    languages: List[str]
    features: List[str]

class UsageFieldsOptions(TypedDict):
    start: Optional[str]
    end: Optional[str]

# Billing

class Balance(TypedDict):
    balance_id: str
    amount: int
    units: str
    purchase: str

class BalancesResponse(TypedDict):
    balances: List[Balance]