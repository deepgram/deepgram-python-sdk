# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Union, Any, Tuple
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from deepgram.utils import verboselogs

from ...enums import AgentWebSocketEvents
from ....common import BaseResponse


# ConfigurationSettings


@dataclass
class Listen(BaseResponse):
    """
    This class defines any configuration settings for the Listen model.
    """

    model: Optional[str] = field(default="nova-2")


@dataclass
class Speak(BaseResponse):
    """
    This class defines any configuration settings for the Speak model.
    """

    model: Optional[str] = field(default="aura-asteria-en")


@dataclass
class Header(BaseResponse):
    """
    This class defines a single key/value pair for a header.
    """

    key: str
    value: str


@dataclass
class Item(BaseResponse):
    """
    This class defines a single item in a list of items.
    """

    type: str
    description: str


@dataclass
class Properties(BaseResponse):
    """
    This class defines the properties which is just a list of items.
    """

    item: Item

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "item" in _dict:
            _dict["item"] = [Item.from_dict(item) for item in _dict["item"]]
        return _dict[key]


@dataclass
class Parameters(BaseResponse):
    """
    This class defines the parameters for a function.
    """

    type: str
    properties: Properties
    required: List[str]

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "properties" in _dict:
            _dict["properties"] = _dict["properties"].copy()
        return _dict[key]


@dataclass
class Function(BaseResponse):
    """
    This class defines a function for the Think model.
    """

    name: str
    description: str
    url: str
    method: str
    headers: Optional[List[Header]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    parameters: Optional[Parameters] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "parameters" in _dict:
            _dict["parameters"] = [
                Parameters.from_dict(parameters) for parameters in _dict["parameters"]
            ]
        if "headers" in _dict:
            _dict["headers"] = [
                Header.from_dict(headers) for headers in _dict["headers"]
            ]
        return _dict[key]


@dataclass
class Provider(BaseResponse):
    """
    This class defines the provider for the Think model.
    """

    type: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )


@dataclass
class Think(BaseResponse):
    """
    This class defines any configuration settings for the Think model.
    """

    provider: Provider = field(default=Provider())
    model: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    instructions: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    functions: Optional[List[Function]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "provider" in _dict:
            _dict["provider"] = [
                Provider.from_dict(provider) for provider in _dict["provider"]
            ]
        if "functions" in _dict:
            _dict["functions"] = [
                Function.from_dict(functions) for functions in _dict["functions"]
            ]
        return _dict[key]


@dataclass
class Agent(BaseResponse):
    """
    This class defines any configuration settings for the Agent model.
    """

    listen: Listen = field(default=Listen())
    think: Think = field(default=Think())
    speak: Speak = field(default=Speak())

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "listen" in _dict:
            _dict["listen"] = [Listen.from_dict(listen) for listen in _dict["listen"]]
        if "think" in _dict:
            _dict["think"] = [Think.from_dict(think) for think in _dict["think"]]
        if "speak" in _dict:
            _dict["speak"] = [Speak.from_dict(speak) for speak in _dict["speak"]]
        return _dict[key]


@dataclass
class Input(BaseResponse):
    """
    This class defines any configuration settings for the input audio.
    """

    encoding: Optional[str] = field(default="linear16")
    sample_rate: int = field(default=16000)


@dataclass
class Output(BaseResponse):
    """
    This class defines any configuration settings for the output audio.
    """

    encoding: Optional[str] = field(default="linear16")
    sample_rate: Optional[int] = field(default=16000)
    bitrate: Optional[int] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    container: Optional[str] = field(default="none")


@dataclass
class Audio(BaseResponse):
    """
    This class defines any configuration settings for the audio.
    """

    input: Optional[Input] = field(default=Input())
    output: Optional[Output] = field(default=Output())

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "input" in _dict:
            _dict["input"] = [Input.from_dict(input) for input in _dict["input"]]
        if "output" in _dict:
            _dict["output"] = [Output.from_dict(output) for output in _dict["output"]]
        return _dict[key]


@dataclass
class Context(BaseResponse):
    """
    This class defines any configuration settings for the context.
    """

    messages: Optional[List[Tuple[str, str]]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    replay: Optional[bool] = field(default=False)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "messages" in _dict:
            _dict["messages"] = _dict["messages"].copy()
        return _dict[key]


@dataclass
class SettingsConfigurationOptions(BaseResponse):
    """
    The client should send a SettingsConfiguration message immediately after opening the websocket and before sending any audio.
    """

    type: str = str(AgentWebSocketEvents.SettingsConfiguration)
    audio: Audio = field(default=Audio())
    agent: Agent = field(default=Agent())
    context: Optional[Context] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "audio" in _dict:
            _dict["audio"] = [Audio.from_dict(audio) for audio in _dict["audio"]]
        if "agent" in _dict:
            _dict["agent"] = [Agent.from_dict(agent) for agent in _dict["agent"]]
        if "context" in _dict:
            _dict["context"] = [
                Context.from_dict(context) for context in _dict["context"]
            ]
        return _dict[key]

    def check(self):
        """
        Check the options for any deprecated or soon-to-be-deprecated options.
        """
        logger = verboselogs.VerboseLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        prev = logger.level
        logger.setLevel(verboselogs.ERROR)

        # do we need to check anything here?

        logger.setLevel(prev)

        return True


# UpdateInstructions


@dataclass
class UpdateInstructionsOptions(BaseResponse):
    """
    The client can send an UpdateInstructions message to give additional instructions to the Think model in the middle of a conversation.
    """

    type: str = str(AgentWebSocketEvents.UpdateInstructions)
    instructions: str = field(default="")


# UpdateSpeak


@dataclass
class UpdateSpeakOptions(BaseResponse):
    """
    The client can send an UpdateSpeak message to change the Speak model in the middle of a conversation.
    """

    type: str = str(AgentWebSocketEvents.UpdateSpeak)
    model: str = field(default="")


# InjectAgentMessage


@dataclass
class InjectAgentMessageOptions(BaseResponse):
    """
    The client can send an InjectAgentMessage to immediately trigger an agent statement. If the injection request arrives while the user is speaking, or while the server is in the middle of sending audio for an agent response, then the request will be ignored and the server will reply with an InjectionRefused.
    """

    type: str = str(AgentWebSocketEvents.InjectAgentMessage)
    message: str = field(default="")
