# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import ManageClient as ManageClientLatest
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
    pass


class KeyOptions(KeyOptionsLatest):
    pass


class ScopeOptions(ScopeOptionsLatest):
    pass


class InviteOptions(InviteOptionsLatest):
    pass


class UsageRequestOptions(UsageRequestOptionsLatest):
    pass


class UsageSummaryOptions(UsageSummaryOptionsLatest):
    pass


class UsageFieldsOptions(UsageFieldsOptionsLatest):
    pass


class ManageClient(ManageClientLatest):
    """
    Please see ManageClientLatest for details
    """

    def __init__(self, config):
        super().__init__(config)
