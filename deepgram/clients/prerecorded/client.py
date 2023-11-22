# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .source import UrlSource, FileSource

from .v1_client import PreRecordedClientV1
from .v1_options import PrerecordedOptionsV1
from .source import PrerecordedSource, FileSource, UrlSource

'''
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
'''
class PrerecordedOptions(PrerecordedOptionsV1):
    pass

class PreRecordedClient(PreRecordedClientV1):
    """
    Please see PreRecordedClientV1 for details
    """
    def __init__(self, config):
        self.config = config
        super().__init__(config)
