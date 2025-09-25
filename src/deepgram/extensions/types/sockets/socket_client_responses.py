# Socket client response union types - protected from auto-generation

import typing

# Import all event types for union definitions
if typing.TYPE_CHECKING:
    from .agent_v1_agent_audio_done_event import AgentV1AgentAudioDoneEvent
    from .agent_v1_agent_started_speaking_event import AgentV1AgentStartedSpeakingEvent
    from .agent_v1_agent_thinking_event import AgentV1AgentThinkingEvent
    from .agent_v1_audio_chunk_event import AgentV1AudioChunkEvent
    from .agent_v1_conversation_text_event import AgentV1ConversationTextEvent
    from .agent_v1_error_event import AgentV1ErrorEvent
    from .agent_v1_function_call_request_event import AgentV1FunctionCallRequestEvent
    from .agent_v1_function_call_response_message import AgentV1FunctionCallResponseMessage
    from .agent_v1_injection_refused_event import AgentV1InjectionRefusedEvent
    from .agent_v1_prompt_updated_event import AgentV1PromptUpdatedEvent
    from .agent_v1_settings_applied_event import AgentV1SettingsAppliedEvent

    # History messages may also be emitted by the server
    from .agent_v1_settings_message import AgentV1HistoryFunctionCalls, AgentV1HistoryMessage
    from .agent_v1_speak_updated_event import AgentV1SpeakUpdatedEvent
    from .agent_v1_user_started_speaking_event import AgentV1UserStartedSpeakingEvent
    from .agent_v1_warning_event import AgentV1WarningEvent
    from .agent_v1_welcome_message import AgentV1WelcomeMessage
    from .listen_v1_metadata_event import ListenV1MetadataEvent
    from .listen_v1_results_event import ListenV1ResultsEvent
    from .listen_v1_speech_started_event import ListenV1SpeechStartedEvent
    from .listen_v1_utterance_end_event import ListenV1UtteranceEndEvent
    from .listen_v2_connected_event import ListenV2ConnectedEvent
    from .listen_v2_fatal_error_event import ListenV2FatalErrorEvent
    from .listen_v2_turn_info_event import ListenV2TurnInfoEvent
    from .speak_v1_audio_chunk_event import SpeakV1AudioChunkEvent
    from .speak_v1_control_event import SpeakV1ControlEvent
    from .speak_v1_metadata_event import SpeakV1MetadataEvent
    from .speak_v1_warning_event import SpeakV1WarningEvent

# Speak socket client can receive these message types (including binary audio)
# Import the actual types for proper resolution
from .speak_v1_audio_chunk_event import SpeakV1AudioChunkEvent
from .speak_v1_control_event import SpeakV1ControlEvent
from .speak_v1_metadata_event import SpeakV1MetadataEvent
from .speak_v1_warning_event import SpeakV1WarningEvent

SpeakV1SocketClientResponse = typing.Union[
    SpeakV1AudioChunkEvent,  # Binary audio data
    SpeakV1MetadataEvent,    # JSON metadata
    SpeakV1ControlEvent,     # JSON control responses (Flushed, Cleared)
    SpeakV1WarningEvent,     # JSON warnings
    bytes,  # Raw binary audio chunks
]

# Listen socket client only receives JSON events
# Import the actual types for proper resolution
from .listen_v1_metadata_event import ListenV1MetadataEvent
from .listen_v1_results_event import ListenV1ResultsEvent
from .listen_v1_speech_started_event import ListenV1SpeechStartedEvent
from .listen_v1_utterance_end_event import ListenV1UtteranceEndEvent

ListenV1SocketClientResponse = typing.Union[
    ListenV1ResultsEvent,
    ListenV1MetadataEvent, 
    ListenV1UtteranceEndEvent,
    ListenV1SpeechStartedEvent,
]

# Listen V2 socket client receives JSON events
# Import the actual types for proper resolution
from .listen_v2_connected_event import ListenV2ConnectedEvent
from .listen_v2_fatal_error_event import ListenV2FatalErrorEvent
from .listen_v2_turn_info_event import ListenV2TurnInfoEvent

ListenV2SocketClientResponse = typing.Union[
    ListenV2ConnectedEvent,
    ListenV2TurnInfoEvent,
    ListenV2FatalErrorEvent,
]

# Agent socket client can receive both JSON events and binary audio
# Import the actual types for proper resolution
from .agent_v1_agent_audio_done_event import AgentV1AgentAudioDoneEvent
from .agent_v1_agent_started_speaking_event import AgentV1AgentStartedSpeakingEvent
from .agent_v1_agent_thinking_event import AgentV1AgentThinkingEvent
from .agent_v1_audio_chunk_event import AgentV1AudioChunkEvent
from .agent_v1_conversation_text_event import AgentV1ConversationTextEvent
from .agent_v1_error_event import AgentV1ErrorEvent
from .agent_v1_function_call_request_event import AgentV1FunctionCallRequestEvent
from .agent_v1_function_call_response_message import AgentV1FunctionCallResponseMessage
from .agent_v1_injection_refused_event import AgentV1InjectionRefusedEvent
from .agent_v1_prompt_updated_event import AgentV1PromptUpdatedEvent
from .agent_v1_settings_applied_event import AgentV1SettingsAppliedEvent
from .agent_v1_settings_message import AgentV1HistoryFunctionCalls, AgentV1HistoryMessage
from .agent_v1_speak_updated_event import AgentV1SpeakUpdatedEvent
from .agent_v1_user_started_speaking_event import AgentV1UserStartedSpeakingEvent
from .agent_v1_warning_event import AgentV1WarningEvent
from .agent_v1_welcome_message import AgentV1WelcomeMessage

AgentV1SocketClientResponse = typing.Union[
    AgentV1WelcomeMessage,
    AgentV1SettingsAppliedEvent,
    AgentV1HistoryMessage,
    AgentV1HistoryFunctionCalls,
    AgentV1ConversationTextEvent,
    AgentV1UserStartedSpeakingEvent,
    AgentV1AgentThinkingEvent,
    AgentV1FunctionCallRequestEvent,
    AgentV1FunctionCallResponseMessage,  # Bidirectional: Server → Client function responses
    AgentV1AgentStartedSpeakingEvent,
    AgentV1AgentAudioDoneEvent,
    AgentV1PromptUpdatedEvent,
    AgentV1SpeakUpdatedEvent,
    AgentV1InjectionRefusedEvent,
    AgentV1ErrorEvent,
    AgentV1WarningEvent,
    AgentV1AudioChunkEvent,  # Binary audio data
    bytes,  # Raw binary audio chunks
]

# Backward compatibility aliases
SpeakSocketClientResponse = SpeakV1SocketClientResponse
ListenSocketClientResponse = ListenV1SocketClientResponse  
AgentSocketClientResponse = AgentV1SocketClientResponse
