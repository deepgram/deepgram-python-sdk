# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import PreRecordedClient as PreRecordedClientV1
from .v1.options import PrerecordedOptions as PrerecordedOptionsV1
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
