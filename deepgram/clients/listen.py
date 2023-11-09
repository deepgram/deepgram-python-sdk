# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .prerecorded.client import PreRecordedClient # FUTURE VERSIONINING:, PreRecordedClientV1
from .live.client import LiveClient # FUTURE VERSIONINING:, LiveClientV1
from typing import Dict, Any, Optional


class ListenClient:
    def __init__(self, url: str, api_key: str, headers: Optional[Dict[str, Any]]):
        self.url = url
        self.api_key = api_key
        self.headers = headers

    @property
    def prerecorded(self):
        return PreRecordedClient(self.url, self.headers)
    
    # FUTURE VERSIONINING:
    # @property
    # def prerecorded_v1(self):
    #     return PreRecordedClientV1(self.url, self.headers)
    
    @property
    def live(self):
        return LiveClient(self.url, self.api_key, self.headers)
    
    # FUTURE VERSIONINING:
    # @property
    # def live_v1(self):
    #     return LiveClientV1(self.url, self.api_key, self.headers)
