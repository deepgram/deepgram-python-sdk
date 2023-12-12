# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# version
__version__ = "0.0.0"

# entry point for the deepgram python sdk
from .client import DeepgramClient
from .options import DeepgramClientOptions

# live
from .clients import LiveTranscriptionEvents
from .clients import LiveClient, AsyncLiveClient, LiveOptions

# onprem
from .clients import (
    OnPremClient,
    AsyncOnPremClient,
)

# prerecorded
from .clients import (
    PreRecordedClient,
    AsyncPreRecordedClient,
    PrerecordedOptions,
    PrerecordedSource,
    FileSource,
    UrlSource,
    BufferSource,
    ReadStreamSource,
)

# manage
from .clients import (
    ManageClient,
    AsyncManageClient,
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)

# utilities
from .audio import Microphone
from .audio import (
    LOGGING,
    CHANNELS,
    RATE,
    CHUNK,
)
