# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin


# Result Message


@dataclass
class Message(DataClassJsonMixin):
    """
    Message from the Deepgram Platform
    """

    message: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


# Projects


@dataclass
class Project(DataClassJsonMixin):
    """
    Project object
    """

    project_id: str = ""
    name: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class ProjectsResponse(DataClassJsonMixin):
    """
    Projects Response object
    """

    projects: List[Project] = field(default_factory=list)

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


@dataclass
class Member(DataClassJsonMixin):
    """
    Member object
    """

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


@dataclass
class MembersResponse(DataClassJsonMixin):
    """
    Members Response object
    """

    members: List[Member] = field(default_factory=list)

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


@dataclass
class Key(DataClassJsonMixin):
    """
    Key object
    """

    api_key_id: str = ""
    key: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    comment: Optional[str] = ""
    created: str = ""
    scopes: List[str] = field(default_factory=list)
    expiration_date: str = field(
        default="", metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "scopes" in _dict:
            _dict["scopes"] = [str(scopes) for scopes in _dict["scopes"]]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class KeyResponse(DataClassJsonMixin):
    """
    Key Response object
    """

    api_key: Key
    member: Member

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


@dataclass
class KeysResponse(DataClassJsonMixin):
    """
    Keys Response object
    """

    api_keys: List[KeyResponse] = field(default_factory=list)

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


@dataclass
class ScopesResponse(DataClassJsonMixin):
    """
    Scopes Response object
    """

    scopes: List[str] = field(default_factory=list)

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


@dataclass
class Invite(DataClassJsonMixin):
    """
    Invite object
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
class InvitesResponse(DataClassJsonMixin):
    """
    Invites Response object
    """

    invites: List[Invite] = field(default_factory=list)

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


@dataclass
class Config(DataClassJsonMixin):  # pylint: disable=too-many-instance-attributes
    """
    Config object
    """

    language: str = ""
    model: str = ""
    punctuate: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    utterances: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    diarize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    smart_format: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    interim_results: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    topics: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    intents: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    sentiment: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    summarize: Optional[bool] = field(
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
class Details(DataClassJsonMixin):  # pylint: disable=too-many-instance-attributes
    """
    Details object
    """

    config: Config
    usd: float = 0
    duration: float = 0
    total_audio: float = 0
    channels: int = 0
    streams: int = 0
    method: str = ""
    tier: Optional[str] = ""
    models: List[str] = field(default_factory=list)
    tags: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    features: List[str] = field(default_factory=list)

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


@dataclass
class Callback(DataClassJsonMixin):
    """
    Callback object
    """

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


@dataclass
class TokenDetail(DataClassJsonMixin):
    """
    Token Detail object
    """

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


@dataclass
class SpeechSegment(DataClassJsonMixin):
    """
    Speech Segment object
    """

    characters: int = 0
    model: str = ""
    tier: str = ""

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class TTSDetails(DataClassJsonMixin):
    """
    TTS Details object
    """

    duration: float = 0
    speech_segments: List[SpeechSegment] = field(default_factory=list)
    # pylint: disable=fixme
    # TODO: audio_metadata: None
    # pylint: enable=fixme

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "speech_segments" in _dict:
            _dict["speech_segments"] = [
                SpeechSegment.from_dict(speech_segments)
                for speech_segments in _dict["speech_segments"]
            ]
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class Response(DataClassJsonMixin):
    """
    Response object
    """

    details: Details
    code: int = 0
    completed: str = ""
    tts_details: Optional[TTSDetails] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    token_details: List[TokenDetail] = field(
        default_factory=list, metadata=dataclass_config(exclude=lambda f: f is list)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "details" in _dict:
            _dict["details"] = Details.from_dict(_dict["details"])
        if "tts_details" in _dict:
            _dict["tts_details"] = TTSDetails.from_dict(_dict["tts_details"])
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


@dataclass
class UsageRequest(DataClassJsonMixin):  # pylint: disable=too-many-instance-attributes
    """
    Usage Request object
    """

    response: Response
    project_uuid: str = ""
    request_id: str = ""
    created: str = ""
    path: str = ""
    api_key_id: str = ""
    callback: Optional[Callback] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    accessor: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class UsageRequestsResponse(DataClassJsonMixin):
    """
    Usage Requests Response object
    """

    page: int = 0
    limit: int = 0
    requests: List[UsageRequest] = field(default_factory=list)

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


@dataclass
class Tokens(DataClassJsonMixin):
    """
    Tokens object
    """

    tokens_in: int = 0
    out: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class TTS(DataClassJsonMixin):
    """
    TTS object
    """

    characters: int = 0
    requests: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class Results(DataClassJsonMixin):
    """
    Results object
    """

    tokens: Tokens
    tts: TTS
    start: str = ""
    end: str = ""
    hours: int = 0
    total_hours: int = 0
    requests: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "tokens" in _dict:
            _dict["tokens"] = Tokens.from_dict(_dict["tokens"])
        if "tts" in _dict:
            _dict["tts"] = TTS.from_dict(_dict["tts"])
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class Resolution(DataClassJsonMixin):
    """
    Resolution object
    """

    units: str = ""
    amount: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)


@dataclass
class UsageSummaryResponse(DataClassJsonMixin):
    """
    Usage Summary Response object
    """

    resolution: Resolution
    start: str = ""
    end: str = ""
    results: List[Results] = field(default_factory=list)

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


@dataclass
class UsageModel(DataClassJsonMixin):
    """
    Usage Model object
    """

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


@dataclass
class UsageFieldsResponse(DataClassJsonMixin):
    """
    Usage Fields Response object
    """

    tags: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    models: List[UsageModel] = field(default_factory=list)
    processing_methods: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    languages: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
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


@dataclass
class Balance(DataClassJsonMixin):
    """
    Balance object
    """

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


@dataclass
class BalancesResponse(DataClassJsonMixin):
    """
    Balances Response object
    """

    balances: List[Balance] = field(default_factory=list)

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
