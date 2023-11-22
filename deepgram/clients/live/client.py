# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1_client import LiveClientV1
from .v1_legacy_client import LegacyLiveClientV1
from .v1_options import LiveOptionsV1

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
  