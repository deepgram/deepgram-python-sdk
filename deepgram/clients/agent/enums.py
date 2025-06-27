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
    FunctionCallRequest: str = "FunctionCallRequest"
    AgentStartedSpeaking: str = "AgentStartedSpeaking"
    AgentAudioDone: str = "AgentAudioDone"
    Error: str = "Error"
    Unhandled: str = "Unhandled"

    # client
    Settings: str = "Settings"
    UpdatePrompt: str = "UpdatePrompt"
    UpdateSpeak: str = "UpdateSpeak"
    InjectAgentMessage: str = "InjectAgentMessage"
    InjectUserMessage: str = "InjectUserMessage"
    InjectionRefused: str = "InjectionRefused"
    AgentKeepAlive: str = "AgentKeepAlive"

