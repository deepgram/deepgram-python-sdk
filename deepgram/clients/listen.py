# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from ..options import DeepgramClientOptions
from .prerecorded.client import PreRecordedClient # FUTURE VERSIONINING:, PreRecordedClientV1
from .live.client import LiveClient, LegacyLiveClient # FUTURE VERSIONINING:, LiveClientV1

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

    # INTERNAL CLASSES
    class Version:
        def __init__(self, parent : str, version: int = 0):
            self.parent = parent
            self.version = version

        @property
        def latest(self):
            match self.parent:
                case "live":
                    return LiveClient(self.config)
                case "legacylive":
                    return LegacyLiveClient(self.config)
                case _:
                    raise Exception("Invalid parent") 
        
        @property
        def v(self):
            if self.version == 0:
                raise Exception("Invalid version")
            
            className = ""
            match self.parent:
                case "manage":
                    className = "ManageClient"
                case "onprem":
                    className = "OnPremClient"
                case _:
                    raise Exception("Invalid parent")
                
            myClass = __import__(f".{self.parent}.v{self.version}.client.{className}")
            return myClass
