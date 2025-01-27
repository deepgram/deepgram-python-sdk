# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# websocket
from .v1 import (
    AgentWebSocketClient as LatestAgentWebSocketClient,
    AsyncAgentWebSocketClient as LatestAsyncAgentWebSocketClient,
)

from .v1 import (
    #### common websocket response
    BaseResponse as LatestBaseResponse,
    OpenResponse as LatestOpenResponse,
    CloseResponse as LatestCloseResponse,
    ErrorResponse as LatestErrorResponse,
    UnhandledResponse as LatestUnhandledResponse,
    #### unique
    WelcomeResponse as LatestWelcomeResponse,
    SettingsAppliedResponse as LatestSettingsAppliedResponse,
    ConversationTextResponse as LatestConversationTextResponse,
    UserStartedSpeakingResponse as LatestUserStartedSpeakingResponse,
    AgentThinkingResponse as LatestAgentThinkingResponse,
    FunctionCalling as LatestFunctionCalling,
    FunctionCallRequest as LatestFunctionCallRequest,
    AgentStartedSpeakingResponse as LatestAgentStartedSpeakingResponse,
    AgentAudioDoneResponse as LatestAgentAudioDoneResponse,
)

from .v1 import (
    # top level
    SettingsConfigurationOptions as LatestSettingsConfigurationOptions,
    UpdateInstructionsOptions as LatestUpdateInstructionsOptions,
    UpdateSpeakOptions as LatestUpdateSpeakOptions,
    InjectAgentMessageOptions as LatestInjectAgentMessageOptions,
    FunctionCallResponse as LatestFunctionCallResponse,
    AgentKeepAlive as LatestAgentKeepAlive,
    # sub level
    Listen as LatestListen,
    Speak as LatestSpeak,
    Header as LatestHeader,
    Item as LatestItem,
    Properties as LatestProperties,
    Parameters as LatestParameters,
    Function as LatestFunction,
    Provider as LatestProvider,
    Think as LatestThink,
    Agent as LatestAgent,
    Input as LatestInput,
    Output as LatestOutput,
    Audio as LatestAudio,
    Context as LatestContext,
)


# The vX/client.py points to the current supported version in the SDK.
# Older versions are supported in the SDK for backwards compatibility.

AgentWebSocketClient = LatestAgentWebSocketClient
AsyncAgentWebSocketClient = LatestAsyncAgentWebSocketClient

OpenResponse = LatestOpenResponse
CloseResponse = LatestCloseResponse
ErrorResponse = LatestErrorResponse
UnhandledResponse = LatestUnhandledResponse

WelcomeResponse = LatestWelcomeResponse
SettingsAppliedResponse = LatestSettingsAppliedResponse
ConversationTextResponse = LatestConversationTextResponse
UserStartedSpeakingResponse = LatestUserStartedSpeakingResponse
AgentThinkingResponse = LatestAgentThinkingResponse
FunctionCalling = LatestFunctionCalling
FunctionCallRequest = LatestFunctionCallRequest
AgentStartedSpeakingResponse = LatestAgentStartedSpeakingResponse
AgentAudioDoneResponse = LatestAgentAudioDoneResponse


SettingsConfigurationOptions = LatestSettingsConfigurationOptions
UpdateInstructionsOptions = LatestUpdateInstructionsOptions
UpdateSpeakOptions = LatestUpdateSpeakOptions
InjectAgentMessageOptions = LatestInjectAgentMessageOptions
FunctionCallResponse = LatestFunctionCallResponse
AgentKeepAlive = LatestAgentKeepAlive

Listen = LatestListen
Speak = LatestSpeak
Header = LatestHeader
Item = LatestItem
Properties = LatestProperties
Parameters = LatestParameters
Function = LatestFunction
Provider = LatestProvider
Think = LatestThink
Agent = LatestAgent
Input = LatestInput
Output = LatestOutput
Audio = LatestAudio
Context = LatestContext
