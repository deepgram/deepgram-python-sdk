# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from .v1.client import AnalyzeClient as AnalyzeClientLatest
from .v1.async_client import AsyncAnalyzeClient as AsyncAnalyzeClientLatest
from .v1.options import (
    # common
    AnalyzeOptions as AnalyzeOptionsLatest,
    UrlSource as UrlSourceLatest,
    TextSource as TextSourceLatest,
    BufferSource as BufferSourceLatest,
    StreamSource as StreamSourceLatest,
    FileSource as FileSourceLatest,
    # unique
    AnalyzeStreamSource as AnalyzeStreamSourceLatest,
    AnalyzeSource as AnalyzeSourceLatest,
)
from .v1.response import (
    SyncAnalyzeResponse as SyncAnalyzeResponseLatest,
    AnalyzeResponse as AnalyzeResponseLatest,
    AsyncAnalyzeResponse as AsyncAnalyzeResponseLatest,
    # shared
    Average as AverageLatest,
    Intent as IntentLatest,
    Intents as IntentsLatest,
    IntentsInfo as IntentsInfoLatest,
    Segment as SegmentLatest,
    SentimentInfo as SentimentInfoLatest,
    Sentiment as SentimentLatest,
    Sentiments as SentimentsLatest,
    SummaryInfo as SummaryInfoLatest,
    Topic as TopicLatest,
    Topics as TopicsLatest,
    TopicsInfo as TopicsInfoLatest,
    # unique
    Results as ResultsLatest,
    Metadata as MetadataLatest,
    Summary as SummaryLatest,
)

# The client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.

# common
UrlSource = UrlSourceLatest
TextSource = TextSourceLatest
BufferSource = BufferSourceLatest
StreamSource = StreamSourceLatest
FileSource = FileSourceLatest

AnalyzeStreamSource = AnalyzeStreamSourceLatest
AnalyzeSource = AnalyzeSourceLatest

# input
AnalyzeOptions = AnalyzeOptionsLatest

# responses
SyncAnalyzeResponse = SyncAnalyzeResponseLatest
AnalyzeResponse = AnalyzeResponseLatest
AsyncAnalyzeResponse = AsyncAnalyzeResponseLatest
# shared
Average = AverageLatest
Intent = IntentLatest
Intents = IntentsLatest
IntentsInfo = IntentsInfoLatest
Segment = SegmentLatest
SentimentInfo = SentimentInfoLatest
Sentiment = SentimentLatest
Sentiments = SentimentsLatest
SummaryInfo = SummaryInfoLatest
Topic = TopicLatest
Topics = TopicsLatest
TopicsInfo = TopicsInfoLatest
# unique
AnalyzeResults = ResultsLatest
AnalyzeMetadata = MetadataLatest
AnalyzeSummary = SummaryLatest

# clients
AnalyzeClient = AnalyzeClientLatest
AsyncAnalyzeClient = AsyncAnalyzeClientLatest


# aliases
ReadClient = AnalyzeClientLatest
AsyncReadClient = AsyncAnalyzeClientLatest
