# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import List, Optional, Union, Any, Tuple, Dict, Literal
import logging

from dataclasses import dataclass, field
from dataclasses_json import config as dataclass_config

from deepgram.utils import verboselogs

from ...enums import AgentWebSocketEvents
from ....common import BaseResponse


# ConfigurationSettings


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


class Provider(dict):
    """
    Generic attribute class for provider objects.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            # pylint: disable=raise-missing-from
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


@dataclass
class Endpoint(BaseResponse):
    """
    Define a custom endpoint for the agent.
    """

    method: Optional[str] = field(default="POST")
    url: str = field(default="")
    headers: Optional[List[Header]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "headers" in _dict:
            _dict["headers"] = [
                Header.from_dict(headers) for headers in _dict["headers"]
            ]
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
    endpoint: Optional[Endpoint] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "parameters" in _dict and isinstance(_dict["parameters"], dict):
            _dict["parameters"] = Parameters.from_dict(_dict["parameters"])
        if "headers" in _dict and isinstance(_dict["headers"], list):
            _dict["headers"] = [Header.from_dict(header) for header in _dict["headers"]]
        if "endpoint" in _dict and isinstance(_dict["endpoint"], dict):
            _dict["endpoint"] = Endpoint.from_dict(_dict["endpoint"])
        return _dict[key]


@dataclass
class Think(BaseResponse):
    """
    This class defines any configuration settings for the Think model.
    """

    provider: Provider = field(
        default_factory=Provider,
        metadata=dataclass_config(
            exclude=lambda f: (
                f is None
                or (isinstance(f, dict) and not f)
                or (isinstance(f, Provider) and not f)
            )
        ),
    )
    functions: Optional[List[Function]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    endpoint: Optional[Endpoint] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    prompt: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )
    context_length: Optional[Union[int, Literal["max"]]] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __post_init__(self):
        if (
            not isinstance(self.provider, Provider)
            and self.provider is not None
            and not (isinstance(self.provider, dict) and not self.provider)
        ):
            self.provider = Provider(self.provider)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "functions" in _dict and isinstance(_dict["functions"], list):
            _dict["functions"] = [
                Function.from_dict(function) for function in _dict["functions"]
            ]
        if "endpoint" in _dict and isinstance(_dict["endpoint"], dict):
            _dict["endpoint"] = Endpoint.from_dict(_dict["endpoint"])
        return _dict[key]


@dataclass
class Listen(BaseResponse):
    """
    This class defines any configuration settings for the Listen model.
    """

    provider: Provider = field(
        default_factory=Provider,
        metadata=dataclass_config(
            exclude=lambda f: (
                f is None
                or (isinstance(f, dict) and not f)
                or (isinstance(f, Provider) and not f)
            )
        ),
    )

    def __post_init__(self):
        if (
            not isinstance(self.provider, Provider)
            and self.provider is not None
            and not (isinstance(self.provider, dict) and not self.provider)
        ):
            self.provider = Provider(self.provider)

    def __getitem__(self, key):
        _dict = self.to_dict()
        return _dict[key]


@dataclass
class Speak(BaseResponse):
    """
    This class defines any configuration settings for the Speak model.
    """

    provider: Provider = field(
        default_factory=Provider,
        metadata=dataclass_config(
            exclude=lambda f: (
                f is None
                or (isinstance(f, dict) and not f)
                or (isinstance(f, Provider) and not f)
            )
        ),
    )
    endpoint: Optional[Endpoint] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __post_init__(self):
        if (
            not isinstance(self.provider, Provider)
            and self.provider is not None
            and not (isinstance(self.provider, dict) and not self.provider)
        ):
            self.provider = Provider(self.provider)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "endpoint" in _dict and isinstance(_dict["endpoint"], dict):
            _dict["endpoint"] = Endpoint.from_dict(_dict["endpoint"])
        return _dict[key]


@dataclass
class Agent(BaseResponse):
    """
    This class defines any configuration settings for the Agent model.
    """

    language: str = field(default="en")
    listen: Listen = field(
        default_factory=Listen,
        metadata=dataclass_config(
            exclude=lambda f: f is None
            or (isinstance(f, dict) and not f)
            or (isinstance(f, Listen) and not f)
        ),
    )
    think: Think = field(
        default_factory=Think,
        metadata=dataclass_config(
            exclude=lambda f: f is None
            or (isinstance(f, dict) and not f)
            or (isinstance(f, Think) and not f)
        ),
    )
    speak: Union[Speak, List[Speak]] = field(default_factory=Speak)
    greeting: Optional[str] = field(
        default=None, metadata=dataclass_config(exclude=lambda f: f is None)
    )

    def __post_init__(self):
        """Handle conversion of dict/list data to proper Speak objects"""
        # Handle speak conversion (OneOf pattern)
        if isinstance(self.speak, list):
            self.speak = [
                Speak.from_dict(item) if isinstance(item, dict) else item
                for item in self.speak
            ]
        elif isinstance(self.speak, dict):
            self.speak = Speak.from_dict(self.speak)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "listen" in _dict and isinstance(_dict["listen"], dict):
            _dict["listen"] = Listen.from_dict(_dict["listen"])
        if "think" in _dict and isinstance(_dict["think"], dict):
            _dict["think"] = Think.from_dict(_dict["think"])
        if "speak" in _dict:
            if isinstance(_dict["speak"], list):
                _dict["speak"] = [Speak.from_dict(item) for item in _dict["speak"]]
            elif isinstance(_dict["speak"], dict):
                _dict["speak"] = Speak.from_dict(_dict["speak"])
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

    input: Optional[Input] = field(default_factory=Input)
    output: Optional[Output] = field(default_factory=Output)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "input" in _dict and isinstance(_dict["input"], dict):
            _dict["input"] = Input.from_dict(_dict["input"])
        if "output" in _dict and isinstance(_dict["output"], dict):
            _dict["output"] = Output.from_dict(_dict["output"])
        return _dict[key]


@dataclass
class SettingsOptions(BaseResponse):
    """
    The client should send a Settings message immediately after opening the websocket and before sending any audio.
    """

    experimental: Optional[bool] = field(default=False)
    type: str = str(AgentWebSocketEvents.Settings)
    audio: Audio = field(default_factory=Audio)
    agent: Agent = field(default_factory=Agent)

    def __getitem__(self, key):
        _dict = self.to_dict()
        if "audio" in _dict and isinstance(_dict["audio"], dict):
            _dict["audio"] = Audio.from_dict(_dict["audio"])
        if "agent" in _dict and isinstance(_dict["agent"], dict):
            _dict["agent"] = Agent.from_dict(_dict["agent"])

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


# UpdatePrompt


@dataclass
class UpdatePromptOptions(BaseResponse):
    """
    The client can send an UpdatePrompt message to provide a new prompt to the Think model in the middle of a conversation.
    """

    type: str = str(AgentWebSocketEvents.UpdatePrompt)
    prompt: str = field(default="")


# UpdateSpeak


@dataclass
class UpdateSpeakOptions(BaseResponse):
    """
    The client can send an UpdateSpeak message to change the Speak model in the middle of a conversation.
    """

    type: str = str(AgentWebSocketEvents.UpdateSpeak)
    speak: Union[Speak, List[Speak]] = field(default_factory=Speak)

    def __post_init__(self):
        """Handle conversion of dict/list data to proper Speak objects"""
        if isinstance(self.speak, list):
            # Convert list of dicts to list of Speak objects
            self.speak = [
                Speak.from_dict(item) if isinstance(item, dict) else item
                for item in self.speak
            ]
        elif isinstance(self.speak, dict):
            # Convert single dict to Speak object
            self.speak = Speak.from_dict(self.speak)


# InjectAgentMessage


@dataclass
class InjectAgentMessageOptions(BaseResponse):
    """
    The client can send an InjectAgentMessage to immediately trigger an agent statement. If the injection request arrives while the user is speaking, or while the server is in the middle of sending audio for an agent response, then the request will be ignored and the server will reply with an InjectionRefused.
    """

    type: str = str(AgentWebSocketEvents.InjectAgentMessage)
    message: str = field(default="")


# InjectUserMessage


@dataclass
class InjectUserMessageOptions(BaseResponse):
    """
    The client can send an InjectUserMessage to interact with the agent using text input.
    This is useful when you need to trigger an agent response from text input.
    """

    type: str = str(AgentWebSocketEvents.InjectUserMessage)
    content: str = field(default="")


# Function Call Response


@dataclass
class FunctionCallResponse(BaseResponse):
    """
    TheFunctionCallResponse message is a JSON command that the client should reply with every time there is a FunctionCallRequest received.
    """

    type: str = "FunctionCallResponse"
    function_call_id: str = field(default="")
    output: str = field(default="")


# Agent Keep Alive


@dataclass
class AgentKeepAlive(BaseResponse):
    """
    The KeepAlive message is a JSON command that you can use to ensure that the server does not close the connection.
    """

    type: str = "KeepAlive"
