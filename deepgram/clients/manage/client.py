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
    ProjectsResponse as ProjectsResponseLatest,
    ModelResponse as ModelResponseLatest,
    ModelsResponse as ModelsResponseLatest,
    MembersResponse as MembersResponseLatest,
    KeyResponse as KeyResponseLatest,
    KeysResponse as KeysResponseLatest,
    ScopesResponse as ScopesResponseLatest,
    InvitesResponse as InvitesResponseLatest,
    UsageRequest as UsageRequestLatest,
    UsageResponse as UsageResponseLatest,
    UsageRequestsResponse as UsageRequestsResponseLatest,
    UsageSummaryResponse as UsageSummaryResponseLatest,
    UsageFieldsResponse as UsageFieldsResponseLatest,
    BalancesResponse as BalancesResponseLatest,
    Project as ProjectLatest,
    STTDetails as STTDetailsLatest,
    TTSMetadata as TTSMetadataLatest,
    TTSDetails as TTSDetailsLatest,
    Member as MemberLatest,
    Key as KeyLatest,
    Invite as InviteLatest,
    Config as ConfigLatest,
    STTUsageDetails as STTUsageDetailsLatest,
    Callback as CallbackLatest,
    TokenDetail as TokenDetailLatest,
    SpeechSegment as SpeechSegmentLatest,
    TTSUsageDetails as TTSUsageDetailsLatest,
    STTTokens as STTTokensLatest,
    TTSTokens as TTSTokensLatest,
    UsageSummaryResults as UsageSummaryResultsLatest,
    Resolution as ResolutionLatest,
    UsageModel as UsageModelLatest,
    Balance as BalanceLatest,
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
ProjectsResponse = ProjectsResponseLatest
ModelResponse = ModelResponseLatest
ModelsResponse = ModelsResponseLatest
MembersResponse = MembersResponseLatest
KeyResponse = KeyResponseLatest
KeysResponse = KeysResponseLatest
ScopesResponse = ScopesResponseLatest
InvitesResponse = InvitesResponseLatest
UsageRequest = UsageRequestLatest
UsageResponse = UsageResponseLatest
UsageRequestsResponse = UsageRequestsResponseLatest
UsageSummaryResponse = UsageSummaryResponseLatest
UsageFieldsResponse = UsageFieldsResponseLatest
BalancesResponse = BalancesResponseLatest
Project = ProjectLatest
STTDetails = STTDetailsLatest
TTSMetadata = TTSMetadataLatest
TTSDetails = TTSDetailsLatest
Member = MemberLatest
Key = KeyLatest
Invite = InviteLatest
Config = ConfigLatest
STTUsageDetails = STTUsageDetailsLatest
Callback = CallbackLatest
TokenDetail = TokenDetailLatest
SpeechSegment = SpeechSegmentLatest
TTSUsageDetails = TTSUsageDetailsLatest
STTTokens = STTTokensLatest
TTSTokens = TTSTokensLatest
UsageSummaryResults = UsageSummaryResultsLatest
Resolution = ResolutionLatest
UsageModel = UsageModelLatest
Balance = BalanceLatest

# clients
ManageClient = ManageClientLatest
AsyncManageClient = AsyncManageClientLatest
