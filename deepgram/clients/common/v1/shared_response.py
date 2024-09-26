# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any


from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config, DataClassJsonMixin


# base class


@dataclass
class BaseResponse(DataClassJsonMixin):
    """
    BaseResponse class used to define the common methods and properties for all response classes.
    """

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self) -> str:
        return self.to_json(indent=4)

    def eval(self, key: str) -> str:
        """
        This method is used to evaluate a key in the response object using a dot notation style method.
        """
        keys = key.split(".")
        result: Dict[Any, Any] = self.to_dict()
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            elif isinstance(result, list) and k.isdigit() and int(k) < len(result):
                result = result[int(k)]
            else:
                return ""
        return str(result)


# shared classes


@dataclass
class ModelInfo(BaseResponse):
    """
    ModelInfo object
    """

    name: str = ""
    version: str = ""
    arch: str = ""


@dataclass
class Hit(BaseResponse):
    """
    The hit information for the response.
    """

    confidence: float = 0
    start: float = 0
    end: float = 0
    snippet: Optional[str] = ""


@dataclass
class Search(BaseResponse):
    """
    The search information for the response.
    """

    query: str = ""
    hits: List[Hit] = field(default_factory=list)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "hits" in _dict:
            _dict["hits"] = [Hit.from_dict(hits) for hits in _dict["hits"]]
        return _dict[key]
