# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import LiveClient
from .v1.async_client import AsyncLiveClient
from .v1.options import LiveOptions
from ...options import DeepgramClientOptions


def live_options():
    return LiveOptions()


def live(config: DeepgramClientOptions):
    return LiveClient(config)


def asynclive(config: DeepgramClientOptions):
    return AsyncLiveClient(config)
