# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ..options import DeepgramClientOptions
from .prerecorded.client import PreRecordedClient # FUTURE VERSIONINING:, PreRecordedClientV1
from .live.client import LiveClient, LegacyLiveClient # FUTURE VERSIONINING:, LiveClientV1
from typing import Dict, Any, Optional

class ListenClient:
    def __init__(self, config: DeepgramClientOptions):
        self.config = config
        
    @property
    def prerecorded(self):
        return PreRecordedClient(self.config)
    
    # FUTURE VERSIONINING:
    # @property
    # def prerecorded_v1(self):
    #     return PreRecordedClientV1(self.config)
    
    @property
    def live(self):
        return LiveClient(self.config)
    
    @property
    def legacylive(self):
        return LegacyLiveClient(self.config)
    
    # FUTURE VERSIONINING:
    # @property
    # def live_v1(self):
    #     return LiveClientV1(self.config)
