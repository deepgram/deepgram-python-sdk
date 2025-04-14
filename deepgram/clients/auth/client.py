# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import AuthRESTClient as AuthRESTClientLatest
from .v1.async_client import AsyncAuthRESTClient as AsyncAuthRESTClientLatest
from .v1.response import GrantTokenResponse as GrantTokenResponseLatest

AuthRESTClient = AuthRESTClientLatest
AsyncAuthRESTClient = AsyncAuthRESTClientLatest
GrantTokenResponse = GrantTokenResponseLatest
