# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1_client import ManageClientV1
from .v1_response import ProjectOptionsV1, KeyOptionsV1, ScopeOptionsV1, InviteOptionsV1, UsageRequestOptionsV1, UsageSummaryOptionsV1, UsageFieldsOptionsV1

'''
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
'''
class ProjectOptions(ProjectOptionsV1):
   pass

class KeyOptions(KeyOptionsV1):
   pass

class ScopeOptions(ScopeOptionsV1):
   pass

class InviteOptions(InviteOptionsV1):
   pass

class UsageRequestOptions(UsageRequestOptionsV1):
   pass

class UsageSummaryOptions(UsageSummaryOptionsV1):
   pass

class UsageFieldsOptions(UsageFieldsOptionsV1):
   pass

class ManageClient(ManageClientV1):
    """
    Please see ManageClientV1 for details
    """
    def __init__(self, config):
      super().__init__(config)
