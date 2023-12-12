# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import ManageClient
from .v1.async_client import AsyncManageClient
from .v1.options import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)
from ...options import DeepgramClientOptions


def project_options():
    return ProjectOptions()


def key_options():
    return KeyOptions()


def scope_options():
    return ScopeOptions()


def invite_options():
    return InviteOptions()


def usage_request_options():
    return UsageRequestOptions()


def usage_summary_options():
    return UsageSummaryOptions()


def usage_fields_options():
    return UsageFieldsOptions()


def manage(config: DeepgramClientOptions):
    return ManageClient(config)


def asyncmanage(config: DeepgramClientOptions):
    return AsyncManageClient(config)
