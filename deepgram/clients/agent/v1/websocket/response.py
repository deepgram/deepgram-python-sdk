# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Dict, Any

from dataclasses import dataclass

# common websocket response
from ....common import (
    BaseResponse,
    OpenResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)

# unique


@dataclass
class WelcomeResponse(BaseResponse):
    """
    The server will send a Welcome message as soon as the websocket opens.
    """

    type: str
    session_id: str


@dataclass
class SettingsAppliedResponse(BaseResponse):
    """
    The server will send a SettingsApplied message as soon as the settings are applied.
    """

    type: str


@dataclass
class ConversationTextResponse(BaseResponse):
    """
    The server will send a ConversationText message every time the agent hears the user say something, and every time the agent speaks something itself.
    """

    type: str
    role: str
    content: str


@dataclass
class UserStartedSpeakingResponse(BaseResponse):
    """
    The server will send a UserStartedSpeaking message every time the user begins a new utterance.
    """

    type: str


@dataclass
class AgentThinkingResponse(BaseResponse):
    """
    The server will send an AgentThinking message to inform the client of a non-verbalized agent thought.
    """

    type: str
    content: str


@dataclass
class FunctionCalling(BaseResponse):
    """
    The server will sometimes send FunctionCalling messages when making function calls to help the client developer debug function calling workflows.
    """

    type: str

@dataclass
class FunctionCallRequest(BaseResponse):
    """
    The FunctionCallRequest message is used to call a function from the server to the client.
    """

    type: str
    function_name: str
    function_call_id: str
    input: str

@dataclass
class AgentStartedSpeakingResponse(BaseResponse):
    """
    The server will send an AgentStartedSpeaking message when it begins streaming an agent audio response to the client for playback.
    """

    total_latency: float
    tts_latency: float
    ttt_latency: float


@dataclass
class AgentAudioDoneResponse(BaseResponse):
    """
    The server will send an AgentAudioDone message immediately after it sends the last audio message in a piece of agent speech.
    """

    type: str
