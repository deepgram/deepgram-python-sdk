# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from ...common import (
    BaseResponse,
)


# Result Message


@dataclass
class Message(BaseResponse):
    """
    Message from the Deepgram Platform
    """

    message: str = ""


# Projects


@dataclass
class Project(BaseResponse):
    """
    Project object
    """

    project_id: str = ""
    name: str = ""


@dataclass
class ProjectsResponse(BaseResponse):
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


# Models


@dataclass
class STTDetails(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    STTDetails class used to define the properties of the Speech-to-Text model response object.
    """

    name: str = ""
    canonical_name: str = ""
    architecture: str = ""
    languages: List[str] = field(default_factory=list)
    version: str = ""
    uuid: str = ""
    batch: bool = False
    streaming: bool = False
    formatted_output: bool = False

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "languages" in _dict:
            _dict["languages"] = [str(languages) for languages in _dict["languages"]]
        return _dict[key]


@dataclass
class TTSMetadata(BaseResponse):
    """
    TTSMetadata class used to define the properties for a given STT or TTS model.
    """

    accent: str = ""
    color: str = ""
    image: str = ""
    sample: str = ""
    tags: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )


@dataclass
class TTSDetails(BaseResponse):
    """
    TTSDetails class used to define the properties of the Text-to-Speech model response object.
    """

    name: str = ""
    canonical_name: str = ""
    architecture: str = ""
    languages: List[str] = field(default_factory=list)
    version: str = ""
    uuid: str = ""
    metadata: Optional[TTSMetadata] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "metadata" in _dict:
            _dict["metadata"] = [
                TTSMetadata.from_dict(metadata) for metadata in _dict["metadata"]
            ]
        return _dict[key]


# responses


@dataclass
class ModelResponse(BaseResponse):
    """
    ModelResponse class used to define the properties of a single model.
    """

    name: str = ""
    canonical_name: str = ""
    architecture: str = ""
    language: str = ""
    version: str = ""
    uuid: str = ""
    metadata: Optional[TTSMetadata] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "metadata" in _dict:
            _dict["metadata"] = [
                TTSMetadata.from_dict(metadata) for metadata in _dict["metadata"]
            ]
        return _dict[key]


@dataclass
class ModelsResponse(BaseResponse):
    """
    ModelsResponse class used to obtain a list of models.
    """

    stt: List[STTDetails] = field(default_factory=list)
    tts: List[TTSDetails] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "stt" in _dict:
            _dict["stt"] = [STTDetails.from_dict(stt) for stt in _dict["stt"]]
        if "tts" in _dict:
            _dict["tts"] = [TTSDetails.from_dict(tts) for tts in _dict["tts"]]
        return _dict[key]


# Members


@dataclass
class Member(BaseResponse):
    """
    Member object
    """

    email: str = ""
    first_name: str = ""
    last_name: str = ""
    member_id: str = ""


@dataclass
class MembersResponse(BaseResponse):
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


# Keys


@dataclass
class Key(BaseResponse):
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


@dataclass
class KeyResponse(BaseResponse):
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


@dataclass
class KeysResponse(BaseResponse):
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


# Scopes


@dataclass
class ScopesResponse(BaseResponse):
    """
    Scopes Response object
    """

    scopes: List[str] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "scopes" in _dict:
            _dict["scopes"] = [str(scopes) for scopes in _dict["scopes"]]
        return _dict[key]


# Invites


@dataclass
class Invite(BaseResponse):
    """
    Invite object
    """

    email: str = ""
    scope: str = ""


@dataclass
class InvitesResponse(BaseResponse):
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


# Usage


@dataclass
class Config(BaseResponse):  # pylint: disable=too-many-instance-attributes
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


@dataclass
class STTUsageDetails(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Details object
    """

    config: Config
    usd: float = 0
    duration: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    total_audio: Optional[float] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    channels: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    streams: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
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


@dataclass
class Callback(BaseResponse):
    """
    Callback object
    """

    attempts: int = 0
    code: int = 0
    completed: str = ""


@dataclass
class TokenDetail(BaseResponse):
    """
    Token Detail object
    """

    feature: str = ""
    input: int = 0
    model: str = ""
    output: int = 0


@dataclass
class SpeechSegment(BaseResponse):
    """
    Speech Segment object
    """

    characters: int = 0
    model: str = ""
    tier: str = ""


@dataclass
class TTSUsageDetails(BaseResponse):
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


@dataclass
class UsageResponse(BaseResponse):
    """
    UsageResponse object
    """

    details: Optional[STTUsageDetails] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    code: int = 0
    completed: str = ""
    message: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    tts_details: Optional[TTSUsageDetails] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    token_details: List[TokenDetail] = field(
        default_factory=list, metadata=dataclass_config(exclude=lambda f: f is list)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "details" in _dict:
            _dict["details"] = STTUsageDetails.from_dict(_dict["details"])
        if "tts_details" in _dict:
            _dict["tts_details"] = TTSUsageDetails.from_dict(_dict["tts_details"])
        if "token_details" in _dict:
            _dict["token_details"] = [
                TokenDetail.from_dict(token_details)
                for token_details in _dict["token_details"]
            ]
        return _dict[key]


@dataclass
class UsageRequest(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Usage Request object
    """

    response: UsageResponse
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
            _dict["response"] = UsageResponse.from_dict(_dict["response"])
        if "callback" in _dict:
            _dict["callback"] = Callback.from_dict(_dict["callback"])
        return _dict[key]


@dataclass
class UsageRequestsResponse(BaseResponse):
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


@dataclass
class STTTokens(BaseResponse):
    """
    STTTokens object
    """

    tokens_in: int = 0
    out: int = 0


@dataclass
class TTSTokens(BaseResponse):
    """
    TTSTokens object
    """

    characters: int = 0
    requests: int = 0


@dataclass
class UsageSummaryResults(BaseResponse):
    """
    Results object
    """

    tokens: STTTokens
    tts: TTSTokens
    start: str = ""
    end: str = ""
    hours: int = 0
    total_hours: int = 0
    requests: int = 0

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "tokens" in _dict:
            _dict["tokens"] = STTTokens.from_dict(_dict["tokens"])
        if "tts" in _dict:
            _dict["tts"] = TTSTokens.from_dict(_dict["tts"])
        return _dict[key]


@dataclass
class Resolution(BaseResponse):
    """
    Resolution object
    """

    units: str = ""
    amount: int = 0


@dataclass
class UsageSummaryResponse(BaseResponse):
    """
    Usage Summary Response object
    """

    resolution: Resolution
    start: str = ""
    end: str = ""
    results: List[UsageSummaryResults] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "resolution" in _dict:
            _dict["resolution"] = Resolution.from_dict(_dict["resolution"])
        if "results" in _dict:
            _dict["results"] = [
                UsageSummaryResults.from_dict(results) for results in _dict["results"]
            ]
        return _dict[key]


@dataclass
class UsageModel(BaseResponse):
    """
    Usage Model object
    """

    name: str = ""
    language: str = ""
    version: str = ""
    model_id: str = ""


@dataclass
class UsageFieldsResponse(BaseResponse):
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


# Billing


@dataclass
class Balance(BaseResponse):
    """
    Balance object
    """

    balance_id: str = ""
    amount: str = ""
    units: str = ""
    purchase_order_id: str = ""


@dataclass
class BalancesResponse(BaseResponse):
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
