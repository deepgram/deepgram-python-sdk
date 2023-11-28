# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import LiveClient as LiveClientV1
from .v1.legacy_client import LegacyLiveClient as LegacyLiveClientV1
from .v1.options import LiveOptions as LiveOptionsV1

'''
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
'''
class LiveOptions(LiveOptionsV1):
  pass

class LiveClient(LiveClientV1):
  """
    Please see LiveClientV1 for details
    """
  def __init__(self, config):
      super().__init__(config)

class LegacyLiveClient(LegacyLiveClientV1):
  """
    Please see LiveClientV1 for details
    """
  def __init__(self, config):
      super().__init__(config)
  