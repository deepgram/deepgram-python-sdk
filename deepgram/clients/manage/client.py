# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import ManageClient as ManageClientLatest
from .v1.async_client import AsyncManageClient as AsyncManageClientLatest
from .v1.options import (
    ProjectOptions as ProjectOptionsLatest,
    KeyOptions as KeyOptionsLatest,
    ScopeOptions as ScopeOptionsLatest,
    InviteOptions as InviteOptionsLatest,
    UsageRequestOptions as UsageRequestOptionsLatest,
    UsageSummaryOptions as UsageSummaryOptionsLatest,
    UsageFieldsOptions as UsageFieldsOptionsLatest,
)

"""
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


class ProjectOptions(ProjectOptionsLatest):
    """
    pass through for ProjectOptions based on API version
    """
    pass


class KeyOptions(KeyOptionsLatest):
    """
    pass through for KeyOptions based on API version
    """
    pass


class ScopeOptions(ScopeOptionsLatest):
    """
    pass through for ScopeOptions based on API version
    """
    pass


class InviteOptions(InviteOptionsLatest):
    """
    pass through for InviteOptions based on API version
    """
    pass


class UsageRequestOptions(UsageRequestOptionsLatest):
    """
    pass through for UsageRequestOptions based on API version
    """
    pass


class UsageSummaryOptions(UsageSummaryOptionsLatest):
    """
    pass through for UsageSummaryOptions based on API version
    """
    pass


class UsageFieldsOptions(UsageFieldsOptionsLatest):
    """
    pass through for UsageFieldsOptions based on API version
    """
    pass


class ManageClient(ManageClientLatest):
    """
    Please see ManageClientLatest for details
    """
    def __init__(self, config):
        super().__init__(config)


class AsyncManageClient(AsyncManageClientLatest):
    """
    Please see AsyncManageClientLatest for details
    """
    def __init__(self, config):
        super().__init__(config)
