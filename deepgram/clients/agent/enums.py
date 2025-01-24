# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from aenum import StrEnum

# Constants mapping to events from the Deepgram API


class AgentWebSocketEvents(StrEnum):
    """
    Enumerates the possible Agent API events that can be received from the Deepgram API
    """

    # server
    Open: str = "Open"
    Close: str = "Close"
    AudioData: str = "AudioData"
    Welcome: str = "Welcome"
    SettingsApplied: str = "SettingsApplied"
    ConversationText: str = "ConversationText"
    UserStartedSpeaking: str = "UserStartedSpeaking"
    AgentThinking: str = "AgentThinking"
    FunctionCallingMessage: str = "FunctionCallingMessage"
    FunctionCallRequest: str = "FunctionCallRequest"
    AgentStartedSpeaking: str = "AgentStartedSpeaking"
    AgentAudioDone: str = "AgentAudioDone"
    EndOfThought: str = "EndOfThought"
    Error: str = "Error"
    Unhandled: str = "Unhandled"

    # client
    SettingsConfiguration: str = "SettingsConfiguration"
    UpdateInstructions: str = "UpdateInstructions"
    UpdateSpeak: str = "UpdateSpeak"
    InjectAgentMessage: str = "InjectAgentMessage"
    AgentKeepAlive: str = "AgentKeepAlive"
