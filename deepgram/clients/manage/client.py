# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import ManageClient as ManageClientLatest
from .v1.async_client import AsyncManageClient as AsyncManageClientLatest

# input
from .v1.options import (
    ProjectOptions as ProjectOptionsLatest,
    KeyOptions as KeyOptionsLatest,
    ScopeOptions as ScopeOptionsLatest,
    InviteOptions as InviteOptionsLatest,
    UsageRequestOptions as UsageRequestOptionsLatest,
    UsageSummaryOptions as UsageSummaryOptionsLatest,
    UsageFieldsOptions as UsageFieldsOptionsLatest,
)

# responses
from .v1.response import (
    Message as MessageLatest,
    Project as ProjectLatest,
    ProjectsResponse as ProjectsResponseLatest,
    MembersResponse as MembersResponseLatest,
    Key as KeyLatest,
    KeyResponse as KeyResponseLatest,
    KeysResponse as KeysResponseLatest,
    ScopesResponse as ScopesResponseLatest,
    InvitesResponse as InvitesResponseLatest,
    UsageRequest as UsageRequestLatest,
    UsageRequestsResponse as UsageRequestsResponseLatest,
    UsageSummaryResponse as UsageSummaryResponseLatest,
    UsageFieldsResponse as UsageFieldsResponseLatest,
    Balance as BalanceLatest,
    BalancesResponse as BalancesResponseLatest,
    ModelResponse as ModelResponseLatest,
    ModelsResponse as ModelsResponseLatest,
)


# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.


# input
ProjectOptions = ProjectOptionsLatest
KeyOptions = KeyOptionsLatest
ScopeOptions = ScopeOptionsLatest
InviteOptions = InviteOptionsLatest
UsageRequestOptions = UsageRequestOptionsLatest
UsageSummaryOptions = UsageSummaryOptionsLatest
UsageFieldsOptions = UsageFieldsOptionsLatest


# responses
Message = MessageLatest
Project = ProjectLatest
ProjectsResponse = ProjectsResponseLatest
MembersResponse = MembersResponseLatest
Key = KeyLatest
KeyResponse = KeyResponseLatest
KeysResponse = KeysResponseLatest
ScopesResponse = ScopesResponseLatest
InvitesResponse = InvitesResponseLatest
UsageRequest = UsageRequestLatest
UsageRequestsResponse = UsageRequestsResponseLatest
UsageSummaryResponse = UsageSummaryResponseLatest
UsageFieldsResponse = UsageFieldsResponseLatest
Balance = BalanceLatest
BalancesResponse = BalancesResponseLatest
ModelResponse = ModelResponseLatest
ModelsResponse = ModelsResponseLatest

# clients
ManageClient = ManageClientLatest
AsyncManageClient = AsyncManageClientLatest
