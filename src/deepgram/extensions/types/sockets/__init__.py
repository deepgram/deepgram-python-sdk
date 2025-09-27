# Socket message types - protected from auto-generation

# isort: skip_file

import typing
from importlib import import_module

if typing.TYPE_CHECKING:
    # Speak socket types
    from .speak_v1_text_message import SpeakV1TextMessage
    from .speak_v1_control_message import SpeakV1ControlMessage
    from .speak_v1_audio_chunk_event import SpeakV1AudioChunkEvent
    from .speak_v1_metadata_event import SpeakV1MetadataEvent
    from .speak_v1_control_event import SpeakV1ControlEvent
    from .speak_v1_warning_event import SpeakV1WarningEvent
    
    # Listen socket types
    from .listen_v1_media_message import ListenV1MediaMessage
    from .listen_v1_control_message import ListenV1ControlMessage
    from .listen_v1_results_event import ListenV1ResultsEvent
    from .listen_v1_metadata_event import ListenV1MetadataEvent
    from .listen_v1_utterance_end_event import ListenV1UtteranceEndEvent
    from .listen_v1_speech_started_event import ListenV1SpeechStartedEvent
    
    # Listen V2 socket types
    from .listen_v2_media_message import ListenV2MediaMessage
    from .listen_v2_control_message import ListenV2ControlMessage
    from .listen_v2_connected_event import ListenV2ConnectedEvent
    from .listen_v2_turn_info_event import ListenV2TurnInfoEvent
    from .listen_v2_fatal_error_event import ListenV2FatalErrorEvent
    
    # Agent socket types - Main message types
    from .agent_v1_settings_message import AgentV1SettingsMessage
    from .agent_v1_update_speak_message import AgentV1UpdateSpeakMessage
    from .agent_v1_update_prompt_message import AgentV1UpdatePromptMessage
    from .agent_v1_inject_user_message_message import AgentV1InjectUserMessageMessage
    from .agent_v1_inject_agent_message_message import AgentV1InjectAgentMessageMessage
    from .agent_v1_function_call_response_message import AgentV1FunctionCallResponseMessage
    from .agent_v1_control_message import AgentV1ControlMessage
    from .agent_v1_media_message import AgentV1MediaMessage
    from .agent_v1_welcome_message import AgentV1WelcomeMessage
    from .agent_v1_settings_applied_event import AgentV1SettingsAppliedEvent
    from .agent_v1_conversation_text_event import AgentV1ConversationTextEvent
    from .agent_v1_user_started_speaking_event import AgentV1UserStartedSpeakingEvent
    from .agent_v1_agent_thinking_event import AgentV1AgentThinkingEvent
    from .agent_v1_function_call_request_event import AgentV1FunctionCallRequestEvent
    from .agent_v1_agent_started_speaking_event import AgentV1AgentStartedSpeakingEvent
    from .agent_v1_agent_audio_done_event import AgentV1AgentAudioDoneEvent
    from .agent_v1_prompt_updated_event import AgentV1PromptUpdatedEvent
    from .agent_v1_speak_updated_event import AgentV1SpeakUpdatedEvent
    from .agent_v1_injection_refused_event import AgentV1InjectionRefusedEvent
    from .agent_v1_error_event import AgentV1ErrorEvent
    from .agent_v1_warning_event import AgentV1WarningEvent
    from .agent_v1_audio_chunk_event import AgentV1AudioChunkEvent
    
    # Agent socket types - Nested configuration types
    from .agent_v1_settings_message import (
        AgentV1AudioInput,
        AgentV1AudioOutput,
        AgentV1AudioConfig,
        AgentV1HistoryMessage,
        AgentV1FunctionCall,
        AgentV1HistoryFunctionCalls,
        AgentV1Flags,
        AgentV1Context,
        AgentV1ListenProvider,
        AgentV1Listen,
        AgentV1Endpoint,
        AgentV1AwsCredentials,
        AgentV1Function,
        AgentV1OpenAiThinkProvider,
        AgentV1AwsBedrockThinkProvider,
        AgentV1AnthropicThinkProvider,
        AgentV1GoogleThinkProvider,
        AgentV1GroqThinkProvider,
        AgentV1Think,
        AgentV1DeepgramSpeakProvider,
        AgentV1ElevenLabsSpeakProvider,
        AgentV1CartesiaVoice,
        AgentV1CartesiaSpeakProvider,
        AgentV1OpenAiSpeakProvider,
        AgentV1AwsPollySpeakProvider,
        AgentV1SpeakProviderConfig,
        AgentV1Agent,
    )
    
    # Union types for socket clients
    from .socket_client_responses import (
        SpeakV1SocketClientResponse,
        ListenV1SocketClientResponse,
        ListenV2SocketClientResponse,
        AgentV1SocketClientResponse,
        # Backward compatibility aliases
        SpeakSocketClientResponse,
        ListenSocketClientResponse,
        AgentSocketClientResponse,
    )

__all__ = [
    # Speak socket types
    "SpeakV1TextMessage",
    "SpeakV1ControlMessage", 
    "SpeakV1AudioChunkEvent",
    "SpeakV1MetadataEvent",
    "SpeakV1ControlEvent",
    "SpeakV1WarningEvent",
    
    # Listen socket types
    "ListenV1MediaMessage",
    "ListenV1ControlMessage",
    "ListenV1ResultsEvent", 
    "ListenV1MetadataEvent",
    "ListenV1UtteranceEndEvent",
    "ListenV1SpeechStartedEvent",
    
    # Listen V2 socket types
    "ListenV2MediaMessage",
    "ListenV2ControlMessage", 
    "ListenV2ConnectedEvent",
    "ListenV2TurnInfoEvent",
    "ListenV2FatalErrorEvent",
    
    # Agent socket types - Main message types
    "AgentV1SettingsMessage",
    "AgentV1UpdateSpeakMessage",
    "AgentV1UpdatePromptMessage",
    "AgentV1InjectUserMessageMessage",
    "AgentV1InjectAgentMessageMessage",
    "AgentV1FunctionCallResponseMessage",
    "AgentV1ControlMessage",
    "AgentV1MediaMessage",
    "AgentV1WelcomeMessage",
    "AgentV1SettingsAppliedEvent",
    "AgentV1ConversationTextEvent",
    "AgentV1UserStartedSpeakingEvent",
    "AgentV1AgentThinkingEvent",
    "AgentV1FunctionCallRequestEvent",
    "AgentV1AgentStartedSpeakingEvent",
    "AgentV1AgentAudioDoneEvent",
    "AgentV1PromptUpdatedEvent",
    "AgentV1SpeakUpdatedEvent",
    "AgentV1InjectionRefusedEvent",
    "AgentV1ErrorEvent",
    "AgentV1WarningEvent",
    "AgentV1AudioChunkEvent",
    
    # Agent socket types - Nested configuration types
    "AgentV1AudioInput",
    "AgentV1AudioOutput",
    "AgentV1AudioConfig",
    "AgentV1HistoryMessage",
    "AgentV1FunctionCall",
    "AgentV1HistoryFunctionCalls",
    "AgentV1Flags",
    "AgentV1Context",
    "AgentV1ListenProvider",
    "AgentV1Listen",
    "AgentV1Endpoint",
    "AgentV1AwsCredentials",
    "AgentV1Function",
    "AgentV1OpenAiThinkProvider",
    "AgentV1AwsBedrockThinkProvider",
    "AgentV1AnthropicThinkProvider",
    "AgentV1GoogleThinkProvider",
    "AgentV1GroqThinkProvider",
    "AgentV1Think",
    "AgentV1DeepgramSpeakProvider",
    "AgentV1ElevenLabsSpeakProvider",
    "AgentV1CartesiaVoice",
    "AgentV1CartesiaSpeakProvider",
    "AgentV1OpenAiSpeakProvider",
    "AgentV1AwsPollySpeakProvider",
    "AgentV1SpeakProviderConfig",
    "AgentV1Agent",
    
    # Union types
    "SpeakV1SocketClientResponse",
    "ListenV1SocketClientResponse", 
    "ListenV2SocketClientResponse",
    "AgentV1SocketClientResponse",
    
    # Backward compatibility aliases
    "SpeakSocketClientResponse",
    "ListenSocketClientResponse",
    "AgentSocketClientResponse",
]


def __getattr__(name: str) -> typing.Any:
    if name in __all__:
        # Handle special case for union types
        if name.endswith("SocketClientResponse"):
            return getattr(import_module(".socket_client_responses", package=__name__), name)
        
        # Handle nested types from agent_v1_settings_message
        nested_agent_types = {
            "AgentV1AudioInput", "AgentV1AudioOutput", "AgentV1AudioConfig",
            "AgentV1HistoryMessage", "AgentV1FunctionCall", "AgentV1HistoryFunctionCalls",
            "AgentV1Flags", "AgentV1Context", "AgentV1ListenProvider", "AgentV1Listen",
            "AgentV1Endpoint", "AgentV1AwsCredentials", "AgentV1Function",
            "AgentV1OpenAiThinkProvider", "AgentV1AwsBedrockThinkProvider",
            "AgentV1AnthropicThinkProvider", "AgentV1GoogleThinkProvider",
            "AgentV1GroqThinkProvider", "AgentV1Think", "AgentV1DeepgramSpeakProvider",
            "AgentV1ElevenLabsSpeakProvider", "AgentV1CartesiaVoice",
            "AgentV1CartesiaSpeakProvider", "AgentV1OpenAiSpeakProvider",
            "AgentV1AwsPollySpeakProvider", "AgentV1SpeakProviderConfig",
            "AgentV1Agent"
        }
        
        if name in nested_agent_types:
            return getattr(import_module(".agent_v1_settings_message", package=__name__), name)
        
        # Convert CamelCase to snake_case for other types
        import re
        module_name = re.sub('([A-Z]+)', r'_\1', name).lower().lstrip('_')
        return getattr(import_module(f".{module_name}", package=__name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
