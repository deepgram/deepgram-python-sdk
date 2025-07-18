# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import asyncio
import json
import logging
from typing import Dict, Union, Optional, cast, Any, Callable
import threading

from .....utils import verboselogs
from .....options import DeepgramClientOptions
from ...enums import AgentWebSocketEvents
from ....common import AbstractAsyncWebSocketClient
from ....common import DeepgramError

from .response import (
    OpenResponse,
    WelcomeResponse,
    SettingsAppliedResponse,
    ConversationTextResponse,
    UserStartedSpeakingResponse,
    AgentThinkingResponse,
    FunctionCallRequest,
    AgentStartedSpeakingResponse,
    AgentAudioDoneResponse,
    InjectionRefusedResponse,
    CloseResponse,
    ErrorResponse,
    UnhandledResponse,
)
from .options import (
    SettingsOptions,
    UpdatePromptOptions,
    UpdateSpeakOptions,
    InjectAgentMessageOptions,
    InjectUserMessageOptions,
    FunctionCallResponse,
    AgentKeepAlive,
)

from .....audio.speaker import (
    Speaker,
    RATE as SPEAKER_RATE,
    CHANNELS as SPEAKER_CHANNELS,
    PLAYBACK_DELTA as SPEAKER_PLAYBACK_DELTA,
)
from .....audio.microphone import (
    Microphone,
    RATE as MICROPHONE_RATE,
    CHANNELS as MICROPHONE_CHANNELS,
)

ONE_SECOND = 1
HALF_SECOND = 0.5
DEEPGRAM_INTERVAL = 5


class AsyncAgentWebSocketClient(
    AbstractAsyncWebSocketClient
):  # pylint: disable=too-many-instance-attributes
    """
    Client for interacting with Deepgram's live transcription services over WebSockets.

     This class provides methods to establish a WebSocket connection for live transcription and handle real-time transcription events.

     Args:
         config (DeepgramClientOptions): all the options for the client.
    """

    _logger: verboselogs.VerboseLogger
    _config: DeepgramClientOptions
    _endpoint: str

    _event_handlers: Dict[AgentWebSocketEvents, list]

    _keep_alive_thread: Union[asyncio.Task, None]

    _kwargs: Optional[Dict] = None
    _addons: Optional[Dict] = None
    # note the distinction here. We can't use _config because it's already used in the parent
    _settings: Optional[SettingsOptions] = None
    _headers: Optional[Dict] = None

    _speaker_created: bool = False
    _speaker: Optional[Speaker] = None
    _microphone_created: bool = False
    _microphone: Optional[Microphone] = None

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config is required")

        self._logger = verboselogs.VerboseLogger(__name__)
        self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(config.verbose)

        self._config = config

        # needs to be "wss://agent.deepgram.com/agent"
        self._endpoint = "v1/agent/converse"

        # override the endpoint since it needs to be "wss://agent.deepgram.com/agent"
        self._config.url = "agent.deepgram.com"
        self._keep_alive_thread = None

        # init handlers
        self._event_handlers = {
            event: [] for event in AgentWebSocketEvents.__members__.values()
        }

        if self._config.options.get("microphone_record") == "true":
            self._logger.info("microphone_record is enabled")
            rate = self._config.options.get("microphone_record_rate", MICROPHONE_RATE)
            channels = self._config.options.get(
                "microphone_record_channels", MICROPHONE_CHANNELS
            )
            device_index = self._config.options.get("microphone_record_device_index")

            self._logger.debug("rate: %s", rate)
            self._logger.debug("channels: %s", channels)
            if device_index is not None:
                self._logger.debug("device_index: %s", device_index)

            self._microphone_created = True

            if device_index is not None:
                self._microphone = Microphone(
                    rate=rate,
                    channels=channels,
                    verbose=self._config.verbose,
                    input_device_index=device_index,
                )
            else:
                self._microphone = Microphone(
                    rate=rate,
                    channels=channels,
                    verbose=self._config.verbose,
                )

        if self._config.options.get("speaker_playback") == "true":
            self._logger.info("speaker_playback is enabled")
            rate = self._config.options.get("speaker_playback_rate", SPEAKER_RATE)
            channels = self._config.options.get(
                "speaker_playback_channels", SPEAKER_CHANNELS
            )
            playback_delta_in_ms = self._config.options.get(
                "speaker_playback_delta_in_ms", SPEAKER_PLAYBACK_DELTA
            )
            device_index = self._config.options.get("speaker_playback_device_index")

            self._logger.debug("rate: %s", rate)
            self._logger.debug("channels: %s", channels)

            self._speaker_created = True

            if device_index is not None:
                self._logger.debug("device_index: %s", device_index)

                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    last_play_delta_in_ms=playback_delta_in_ms,
                    verbose=self._config.verbose,
                    output_device_index=device_index,
                    microphone=self._microphone,
                )
            else:
                self._speaker = Speaker(
                    rate=rate,
                    channels=channels,
                    last_play_delta_in_ms=playback_delta_in_ms,
                    verbose=self._config.verbose,
                    microphone=self._microphone,
                )
        # call the parent constructor
        super().__init__(self._config, self._endpoint)

    # pylint: disable=too-many-branches,too-many-statements
    async def start(
        self,
        options: Optional[SettingsOptions] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        members: Optional[Dict] = None,
        **kwargs,
    ) -> bool:
        """
        Starts the WebSocket connection for agent API.
        """
        self._logger.debug("AsyncAgentWebSocketClient.start ENTER")
        self._logger.info("settings: %s", options)
        self._logger.info("addons: %s", addons)
        self._logger.info("headers: %s", headers)
        self._logger.info("members: %s", members)
        self._logger.info("kwargs: %s", kwargs)

        if isinstance(options, SettingsOptions) and not options.check():
            self._logger.error("settings.check failed")
            self._logger.debug("AsyncAgentWebSocketClient.start LEAVE")
            raise DeepgramError("Fatal agent settings error")

        self._addons = addons
        self._headers = headers

        # add "members" as members of the class
        if members is not None:
            self.__dict__.update(members)

        # set kwargs as members of the class
        if kwargs is not None:
            self._kwargs = kwargs
        else:
            self._kwargs = {}

        if isinstance(options, SettingsOptions):
            self._logger.info("options is class")
            self._settings = options
        elif isinstance(options, dict):
            self._logger.info("options is dict")
            self._settings = SettingsOptions.from_dict(options)
        elif isinstance(options, str):
            self._logger.info("options is json")
            self._settings = SettingsOptions.from_json(options)
        else:
            raise DeepgramError("Invalid options type")

        try:
            # speaker substitutes the listening thread
            if self._speaker is not None:
                self._logger.notice("passing speaker to delegate_listening")
                super().delegate_listening(self._speaker)

            # call parent start
            if (
                await super().start(
                    {},
                    self._addons,
                    self._headers,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )
                is False
            ):
                self._logger.error("AsyncAgentWebSocketClient.start failed")
                self._logger.debug("AsyncAgentWebSocketClient.start LEAVE")
                return False

            if self._speaker is not None:
                self._logger.notice("speaker is delegate_listening. Starting speaker")
                self._speaker.start()

            if self._speaker is not None and self._microphone is not None:
                self._logger.notice(
                    "speaker is delegate_listening. Starting microphone"
                )
                self._microphone.set_callback(self.send)
                self._microphone.start()

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # keepalive thread
            if self._config.is_keep_alive_enabled():
                self._logger.notice("keepalive is enabled")
                self._keep_alive_thread = asyncio.create_task(self._keep_alive())
            else:
                self._logger.notice("keepalive is disabled")

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            # send the configurationsetting message
            self._logger.notice("Sending Settings...")
            ret_send_cs = await self.send(str(self._settings))
            if not ret_send_cs:
                self._logger.error("Settings failed")

                err_error: ErrorResponse = ErrorResponse(
                    "Exception in AsyncAgentWebSocketClient.start",
                    "Settings failed to send",
                    "Exception",
                )
                await self._emit(
                    AgentWebSocketEvents(AgentWebSocketEvents.Error),
                    error=err_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                self._logger.debug("AgentWebSocketClient.start LEAVE")
                return False

            self._logger.notice("start succeeded")
            self._logger.debug("AsyncAgentWebSocketClient.start LEAVE")
            return True

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "WebSocketException in AsyncAgentWebSocketClient.start: %s", e
            )
            self._logger.debug("AsyncAgentWebSocketClient.start LEAVE")
            if self._config.options.get("termination_exception_connect") is True:
                raise e
            return False

    # pylint: enable=too-many-branches,too-many-statements

    def on(self, event: AgentWebSocketEvents, handler: Callable) -> None:
        """
        Registers event handlers for specific events.
        """
        self._logger.info("event subscribed: %s", event)
        if event in AgentWebSocketEvents.__members__.values() and callable(handler):
            self._event_handlers[event].append(handler)

    async def _emit(self, event: AgentWebSocketEvents, *args, **kwargs) -> None:
        """
        Emits events to the registered event handlers.
        """
        self._logger.debug("AsyncAgentWebSocketClient._emit ENTER")
        self._logger.debug("callback handlers for: %s", event)

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.debug("callback handlers for: %s", event)
        tasks = []
        for handler in self._event_handlers[event]:
            task = asyncio.create_task(handler(self, *args, **kwargs))
            tasks.append(task)

        if tasks:
            self._logger.debug("waiting for tasks to finish...")
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks.clear()

        # debug the threads
        for thread in threading.enumerate():
            self._logger.debug("after running thread: %s", thread.name)
        self._logger.debug("number of active threads: %s", threading.active_count())

        self._logger.debug("AsyncAgentWebSocketClient._emit LEAVE")

    # pylint: disable=too-many-locals,too-many-statements
    async def _process_text(self, message: str) -> None:
        """
        Processes messages received over the WebSocket connection.
        """
        self._logger.debug("AsyncAgentWebSocketClient._process_text ENTER")

        try:
            self._logger.debug("Text data received")
            if len(message) == 0:
                self._logger.debug("message is empty")
                self._logger.debug("AsyncAgentWebSocketClient._process_text LEAVE")
                return

            data = json.loads(message)
            response_type = data.get("type")
            self._logger.debug("response_type: %s, data: %s", response_type, data)

            match response_type:
                case AgentWebSocketEvents.Open:
                    open_result: OpenResponse = OpenResponse.from_json(message)
                    self._logger.verbose("OpenResponse: %s", open_result)
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.Open),
                        open=open_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.Welcome:
                    welcome_result: WelcomeResponse = WelcomeResponse.from_json(message)
                    self._logger.verbose("WelcomeResponse: %s", welcome_result)
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.Welcome),
                        welcome=welcome_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.SettingsApplied:
                    settings_applied_result: SettingsAppliedResponse = (
                        SettingsAppliedResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "SettingsAppliedResponse: %s", settings_applied_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.SettingsApplied),
                        settings_applied=settings_applied_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.ConversationText:
                    conversation_text_result: ConversationTextResponse = (
                        ConversationTextResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "ConversationTextResponse: %s", conversation_text_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.ConversationText),
                        conversation_text=conversation_text_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.UserStartedSpeaking:
                    user_started_speaking_result: UserStartedSpeakingResponse = (
                        UserStartedSpeakingResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "UserStartedSpeakingResponse: %s", user_started_speaking_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.UserStartedSpeaking),
                        user_started_speaking=user_started_speaking_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.AgentThinking:
                    agent_thinking_result: AgentThinkingResponse = (
                        AgentThinkingResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "AgentThinkingResponse: %s", agent_thinking_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.AgentThinking),
                        agent_thinking=agent_thinking_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.FunctionCallRequest:
                    function_call_request_result: FunctionCallRequest = (
                        FunctionCallRequest.from_json(message)
                    )
                    self._logger.verbose(
                        "FunctionCallRequest: %s", function_call_request_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.FunctionCallRequest),
                        function_call_request=function_call_request_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.AgentStartedSpeaking:
                    agent_started_speaking_result: AgentStartedSpeakingResponse = (
                        AgentStartedSpeakingResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "AgentStartedSpeakingResponse: %s",
                        agent_started_speaking_result,
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.AgentStartedSpeaking),
                        agent_started_speaking=agent_started_speaking_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.AgentAudioDone:
                    agent_audio_done_result: AgentAudioDoneResponse = (
                        AgentAudioDoneResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "AgentAudioDoneResponse: %s", agent_audio_done_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.AgentAudioDone),
                        agent_audio_done=agent_audio_done_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.InjectionRefused:
                    injection_refused_result: InjectionRefusedResponse = (
                        InjectionRefusedResponse.from_json(message)
                    )
                    self._logger.verbose(
                        "InjectionRefused: %s", injection_refused_result
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.InjectionRefused),
                        injection_refused=injection_refused_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.Close:
                    close_result: CloseResponse = CloseResponse.from_json(message)
                    self._logger.verbose("CloseResponse: %s", close_result)
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.Close),
                        close=close_result,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case AgentWebSocketEvents.Error:
                    err_error: ErrorResponse = ErrorResponse.from_json(message)
                    self._logger.verbose("ErrorResponse: %s", err_error)
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.Error),
                        error=err_error,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )
                case _:
                    self._logger.warning(
                        "Unknown Message: response_type: %s, data: %s",
                        response_type,
                        data,
                    )
                    unhandled_error: UnhandledResponse = UnhandledResponse(
                        type=AgentWebSocketEvents(AgentWebSocketEvents.Unhandled),
                        raw=message,
                    )
                    await self._emit(
                        AgentWebSocketEvents(AgentWebSocketEvents.Unhandled),
                        unhandled=unhandled_error,
                        **dict(cast(Dict[Any, Any], self._kwargs)),
                    )

            self._logger.notice("_process_text Succeeded")
            self._logger.debug("AsyncAgentWebSocketClient._process_text LEAVE")

        except Exception as e:  # pylint: disable=broad-except
            self._logger.error(
                "Exception in AsyncAgentWebSocketClient._process_text: %s", e
            )
            e_error: ErrorResponse = ErrorResponse(
                "Exception in AsyncAgentWebSocketClient._process_text",
                f"{e}",
                "Exception",
            )
            await self._emit(
                AgentWebSocketEvents(AgentWebSocketEvents.Error),
                error=e_error,
                **dict(cast(Dict[Any, Any], self._kwargs)),
            )

            # signal exit and close
            await super()._signal_exit()

            self._logger.debug("AsyncAgentWebSocketClient._process_text LEAVE")

            if self._config.options.get("termination_exception") is True:
                raise
            return

    # pylint: enable=too-many-locals,too-many-statements

    async def _process_binary(self, message: bytes) -> None:
        self._logger.debug("AsyncAgentWebSocketClient._process_binary ENTER")
        self._logger.debug("Binary data received")

        await self._emit(
            AgentWebSocketEvents(AgentWebSocketEvents.AudioData),
            data=message,
            **dict(cast(Dict[Any, Any], self._kwargs)),
        )

        self._logger.notice("_process_binary Succeeded")
        self._logger.debug("AsyncAgentWebSocketClient._process_binary LEAVE")

    # pylint: disable=too-many-return-statements
    async def _keep_alive(self) -> None:
        """
        Sends keepalive messages to the WebSocket connection.
        """
        self._logger.debug("AsyncAgentWebSocketClient._keep_alive ENTER")

        counter = 0
        while True:
            try:
                counter += 1
                await asyncio.sleep(ONE_SECOND)

                if self._exit_event.is_set():
                    self._logger.notice("_keep_alive exiting gracefully")
                    self._logger.debug("AsyncAgentWebSocketClient._keep_alive LEAVE")
                    return

                # deepgram keepalive
                if counter % DEEPGRAM_INTERVAL == 0:
                    await self.keep_alive()

            except Exception as e:  # pylint: disable=broad-except
                self._logger.error(
                    "Exception in AsyncAgentWebSocketClient._keep_alive: %s", e
                )
                e_error: ErrorResponse = ErrorResponse(
                    "Exception in AsyncAgentWebSocketClient._keep_alive",
                    f"{e}",
                    "Exception",
                )
                self._logger.error(
                    "Exception in AsyncAgentWebSocketClient._keep_alive: %s", str(e)
                )
                await self._emit(
                    AgentWebSocketEvents(AgentWebSocketEvents.Error),
                    error=e_error,
                    **dict(cast(Dict[Any, Any], self._kwargs)),
                )

                # signal exit and close
                await super()._signal_exit()

                self._logger.debug("AsyncAgentWebSocketClient._keep_alive LEAVE")

                if self._config.options.get("termination_exception") is True:
                    raise
                return

    async def keep_alive(self) -> bool:
        """
        Sends a KeepAlive message
        """
        self._logger.spam("AsyncAgentWebSocketClient.keep_alive ENTER")

        self._logger.notice("Sending KeepAlive...")
        ret = await self.send(json.dumps({"type": "KeepAlive"}))

        if not ret:
            self._logger.error("keep_alive failed")
            self._logger.spam("AsyncAgentWebSocketClient.keep_alive LEAVE")
            return False

        self._logger.notice("keep_alive succeeded")
        self._logger.spam("AsyncAgentWebSocketClient.keep_alive LEAVE")

        return True

    async def inject_user_message(self, options: InjectUserMessageOptions) -> bool:
        """
        Injects a user message to trigger an agent response from text input.
        """
        self._logger.spam("AsyncAgentWebSocketClient.inject_user_message ENTER")

        if not isinstance(options, InjectUserMessageOptions):
            self._logger.error("options must be of type InjectUserMessageOptions")
            self._logger.spam("AsyncAgentWebSocketClient.inject_user_message LEAVE")
            return False

        self._logger.notice("Sending InjectUserMessage...")
        ret = await self.send(str(options))

        if not ret:
            self._logger.error("inject_user_message failed")
            self._logger.spam("AsyncAgentWebSocketClient.inject_user_message LEAVE")
            return False

        self._logger.notice("inject_user_message succeeded")
        self._logger.spam("AsyncAgentWebSocketClient.inject_user_message LEAVE")

        return True

    async def inject_agent_message(self, options: InjectAgentMessageOptions) -> bool:
        """
        Injects an agent message to immediately trigger an agent statement.
        """
        self._logger.spam("AsyncAgentWebSocketClient.inject_agent_message ENTER")

        if not isinstance(options, InjectAgentMessageOptions):
            self._logger.error("options must be of type InjectAgentMessageOptions")
            self._logger.spam("AsyncAgentWebSocketClient.inject_agent_message LEAVE")
            return False

        self._logger.notice("Sending InjectAgentMessage...")
        ret = await self.send(str(options))

        if not ret:
            self._logger.error("inject_agent_message failed")
            self._logger.spam("AsyncAgentWebSocketClient.inject_agent_message LEAVE")
            return False

        self._logger.notice("inject_agent_message succeeded")
        self._logger.spam("AsyncAgentWebSocketClient.inject_agent_message LEAVE")

        return True

    async def _close_message(self) -> bool:
        # TODO: No known API close message # pylint: disable=fixme
        # return await self.send(json.dumps({"type": "Close"}))
        return True

    async def finish(self) -> bool:
        """
        Closes the WebSocket connection gracefully.
        """
        self._logger.debug("AsyncAgentWebSocketClient.finish ENTER")

        # stop the threads
        self._logger.verbose("cancelling tasks...")
        try:
            # call parent finish
            if await super().finish() is False:
                self._logger.error("AsyncAgentWebSocketClient.finish failed")

            if self._microphone is not None and self._microphone_created:
                self._microphone.finish()
                self._microphone_created = False

            if self._speaker is not None and self._speaker_created:
                self._speaker.finish()
                self._speaker_created = False

            # Before cancelling, check if the tasks were created
            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("before running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            tasks = []
            if self._keep_alive_thread is not None:
                self._keep_alive_thread.cancel()
                tasks.append(self._keep_alive_thread)
                self._logger.notice("processing _keep_alive_thread cancel...")

            # Use asyncio.gather to wait for tasks to be cancelled
            # Prevent indefinite waiting by setting a timeout
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=10)
            self._logger.notice("threads joined")

            self._speaker = None
            self._microphone = None

            # debug the threads
            for thread in threading.enumerate():
                self._logger.debug("after running thread: %s", thread.name)
            self._logger.debug("number of active threads: %s", threading.active_count())

            self._logger.notice("finish succeeded")
            self._logger.spam("AsyncAgentWebSocketClient.finish LEAVE")
            return True

        except asyncio.CancelledError as e:
            self._logger.debug("tasks cancelled error: %s", e)
            self._logger.debug("AsyncAgentWebSocketClient.finish LEAVE")
            return False

        except asyncio.TimeoutError as e:
            self._logger.error("tasks cancellation timed out: %s", e)
            self._logger.debug("AsyncAgentWebSocketClient.finish LEAVE")
            return False
