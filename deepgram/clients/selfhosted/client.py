# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import SelfHostedClient as SelfHostedClientLatest
from .v1.async_client import AsyncSelfHostedClient as AsyncSelfHostedClientLatest


# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.

SelfHostedClient = SelfHostedClientLatest
AsyncSelfHostedClient = AsyncSelfHostedClientLatest
OnPremClient = SelfHostedClientLatest
AsyncOnPremClient = AsyncSelfHostedClientLatest
