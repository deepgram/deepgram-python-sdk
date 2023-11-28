# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import OnPremClient as OnPremClientLatest

"""
The client.py points to the current supported version in the SDK.
Older versions are supported in the SDK for backwards compatibility.
"""


class OnPremClient(OnPremClientLatest):
    """
    Please see OnPremClientLatest for details
    """

    def __init__(self, config):
        super().__init__(config)
