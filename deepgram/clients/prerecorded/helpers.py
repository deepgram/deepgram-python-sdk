# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .source import PrerecordedSource


def is_buffer_source(provided_source: PrerecordedSource) -> bool:
    return "buffer" in provided_source


def is_readstream_source(provided_source: PrerecordedSource) -> bool:
    return "stream" in provided_source


def is_url_source(provided_source: PrerecordedSource) -> bool:
    return "url" in provided_source
