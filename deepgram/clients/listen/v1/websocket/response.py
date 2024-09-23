# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

# common websocket response
from ....common import (
    BaseResponse,
    OpenResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)

# between rest and websocket
from ....common import (
    ModelInfo,
    Alternative,
    Hit,
    Search,
    Channel,
    Word,
)

# shared

ModelInfo = ModelInfo
Word = Word
Alternative = Alternative
Hit = Hit
Search = Search
Channel = Channel

# unique


@dataclass
class Metadata(BaseResponse):
    """
    Metadata object
    """

    model_info: ModelInfo
    request_id: str = ""
    model_uuid: str = ""
    extra: Optional[Dict[str, str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info) for model_info in _dict["model_info"]
            ]
        if "extra" in _dict:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
        return _dict[key]


# shared result messages
OpenResponse = OpenResponse
CloseResponse = CloseResponse
ErrorResponse = ErrorResponse
UnhandledResponse = UnhandledResponse


# live result messages


@dataclass
class LiveResultResponse(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Result Message from the Deepgram Platform
    """

    channel: Channel
    metadata: Metadata
    type: str = ""
    channel_index: List[int] = field(default_factory=list)
    duration: float = 0
    start: float = 0
    is_final: bool = False
    from_finalize: Optional[bool] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    speech_final: bool = False

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "channel" in _dict:
            _dict["channel"] = [
                Channel.from_dict(channel) for channel in _dict["channel"]
            ]
        if "metadata" in _dict:
            _dict["metadata"] = [
                Metadata.from_dict(metadata) for metadata in _dict["metadata"]
            ]
        return _dict[key]


# Metadata Message


@dataclass
class MetadataResponse(BaseResponse):  # pylint: disable=too-many-instance-attributes
    """
    Metadata Message from the Deepgram Platform
    """

    type: str = ""
    transaction_key: str = ""
    request_id: str = ""
    sha256: str = ""
    created: str = ""
    duration: float = 0
    channels: int = 0
    models: Optional[List[str]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    model_info: Optional[Dict[str, ModelInfo]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    extra: Optional[Dict] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "models" in _dict:
            _dict["models"] = [str(models) for models in _dict["models"]]
        if "model_info" in _dict:
            _dict["model_info"] = [
                ModelInfo.from_dict(model_info)
                for _, model_info in _dict["model_info"].items()
            ]
        if "extra" in _dict:
            _dict["extra"] = [str(extra) for _, extra in _dict["extra"].items()]
        return _dict[key]


# Speech Started Message


@dataclass
class SpeechStartedResponse(BaseResponse):
    """
    SpeechStartedResponse Message from the Deepgram Platform
    """

    type: str = ""
    channel: List[int] = field(default_factory=list)
    timestamp: float = 0


# Utterance End Message


@dataclass
class UtteranceEndResponse(BaseResponse):
    """
    UtteranceEnd Message from the Deepgram Platform
    """

    type: str = ""
    channel: List[int] = field(default_factory=list)
    last_word_end: float = 0
