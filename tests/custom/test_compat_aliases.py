from deepgram import CreateKeyV1Request as RootCreateKeyV1Request
from deepgram import CreateKeyV1RequestOne
from deepgram.agent import AgentV1HistoryContent as AgentHistoryContentFromAgent
from deepgram.agent import AgentV1HistoryContentParams as AgentHistoryContentParamsFromAgent
from deepgram.agent import AgentV1HistoryFunctionCalls as AgentHistoryFunctionCallsFromAgent
from deepgram.agent import AgentV1HistoryFunctionCallsParams as AgentHistoryFunctionCallsParamsFromAgent
from deepgram.agent import AgentV1SettingsAgentContextMessagesItemContent as AgentContextContentFromAgent
from deepgram.agent import AgentV1SettingsAgentContextMessagesItemContentParams as AgentContextContentParamsFromAgent
from deepgram.agent import AgentV1SettingsAgentContextMessagesItemFunctionCalls as AgentContextFunctionCallsFromAgent
from deepgram.agent import (
    AgentV1SettingsAgentContextMessagesItemFunctionCallsParams as AgentContextFunctionCallsParamsFromAgent,
)
from deepgram.agent.v1 import AgentV1HistoryContent as AgentHistoryContentFromV1
from deepgram.agent.v1 import AgentV1HistoryContentParams as AgentHistoryContentParamsFromV1
from deepgram.agent.v1 import AgentV1HistoryFunctionCalls as AgentHistoryFunctionCallsFromV1
from deepgram.agent.v1 import AgentV1HistoryFunctionCallsParams as AgentHistoryFunctionCallsParamsFromV1
from deepgram.agent.v1 import AgentV1SettingsAgentContextMessagesItemContent as AgentContextContentFromV1
from deepgram.agent.v1 import AgentV1SettingsAgentContextMessagesItemContentParams as AgentContextContentParamsFromV1
from deepgram.agent.v1 import AgentV1SettingsAgentContextMessagesItemFunctionCalls as AgentContextFunctionCallsFromV1
from deepgram.agent.v1 import (
    AgentV1SettingsAgentContextMessagesItemFunctionCallsParams as AgentContextFunctionCallsParamsFromV1,
)
from deepgram.agent.v1.requests import (
    AgentV1HistoryContentParams,
    AgentV1HistoryFunctionCallsParams,
    AgentV1SettingsAgentContextMessagesItemContentParams,
    AgentV1SettingsAgentContextMessagesItemFunctionCallsParams,
    ConversationHistoryMessageParams,
    FunctionCallHistoryMessageParams,
)
from deepgram.agent.v1.requests.agent_v1history_content import AgentV1HistoryContentParams as ModuleHistoryContentParams
from deepgram.agent.v1.requests.agent_v1history_function_calls import (
    AgentV1HistoryFunctionCallsParams as ModuleHistoryFunctionCallsParams,
)
from deepgram.agent.v1.requests.agent_v1settings_agent_context_messages_item_content import (
    AgentV1SettingsAgentContextMessagesItemContentParams as ModuleContextContentParams,
)
from deepgram.agent.v1.requests.agent_v1settings_agent_context_messages_item_function_calls import (
    AgentV1SettingsAgentContextMessagesItemFunctionCallsParams as ModuleContextFunctionCallsParams,
)
from deepgram.agent.v1.types import (
    AgentV1HistoryContent,
    AgentV1HistoryFunctionCalls,
    AgentV1SettingsAgentContextMessagesItemContent,
    AgentV1SettingsAgentContextMessagesItemFunctionCalls,
    ConversationHistoryMessage,
    FunctionCallHistoryMessage,
)
from deepgram.agent.v1.types.agent_v1history_content import AgentV1HistoryContent as ModuleHistoryContent
from deepgram.agent.v1.types.agent_v1history_function_calls import (
    AgentV1HistoryFunctionCalls as ModuleHistoryFunctionCalls,
)
from deepgram.agent.v1.types.agent_v1settings_agent_context_messages_item_content import (
    AgentV1SettingsAgentContextMessagesItemContent as ModuleContextContent,
)
from deepgram.agent.v1.types.agent_v1settings_agent_context_messages_item_function_calls import (
    AgentV1SettingsAgentContextMessagesItemFunctionCalls as ModuleContextFunctionCalls,
)
from deepgram.requests import CreateKeyV1RequestOneParams, CreateKeyV1RequestParams
from deepgram.requests.create_key_v1request_one import CreateKeyV1RequestOneParams as ModuleCreateKeyV1RequestOneParams
from deepgram.types import CreateKeyV1Request
from deepgram.types import CreateKeyV1RequestOne as CreateKeyV1RequestOneType
from deepgram.types.create_key_v1request_one import CreateKeyV1RequestOne as ModuleCreateKeyV1RequestOne


def test_old_agent_history_type_aliases_resolve_to_new_models() -> None:
    assert AgentV1HistoryContent is ConversationHistoryMessage
    assert ModuleHistoryContent is ConversationHistoryMessage
    assert AgentHistoryContentFromV1 is ConversationHistoryMessage
    assert AgentHistoryContentFromAgent is ConversationHistoryMessage

    assert AgentV1HistoryFunctionCalls is FunctionCallHistoryMessage
    assert ModuleHistoryFunctionCalls is FunctionCallHistoryMessage
    assert AgentHistoryFunctionCallsFromV1 is FunctionCallHistoryMessage
    assert AgentHistoryFunctionCallsFromAgent is FunctionCallHistoryMessage

    assert AgentV1SettingsAgentContextMessagesItemContent is ConversationHistoryMessage
    assert ModuleContextContent is ConversationHistoryMessage
    assert AgentContextContentFromV1 is ConversationHistoryMessage
    assert AgentContextContentFromAgent is ConversationHistoryMessage

    assert AgentV1SettingsAgentContextMessagesItemFunctionCalls is FunctionCallHistoryMessage
    assert ModuleContextFunctionCalls is FunctionCallHistoryMessage
    assert AgentContextFunctionCallsFromV1 is FunctionCallHistoryMessage
    assert AgentContextFunctionCallsFromAgent is FunctionCallHistoryMessage


def test_old_agent_history_request_aliases_resolve_to_new_params() -> None:
    assert AgentV1HistoryContentParams is ConversationHistoryMessageParams
    assert ModuleHistoryContentParams is ConversationHistoryMessageParams
    assert AgentHistoryContentParamsFromV1 is ConversationHistoryMessageParams
    assert AgentHistoryContentParamsFromAgent is ConversationHistoryMessageParams

    assert AgentV1HistoryFunctionCallsParams is FunctionCallHistoryMessageParams
    assert ModuleHistoryFunctionCallsParams is FunctionCallHistoryMessageParams
    assert AgentHistoryFunctionCallsParamsFromV1 is FunctionCallHistoryMessageParams
    assert AgentHistoryFunctionCallsParamsFromAgent is FunctionCallHistoryMessageParams

    assert AgentV1SettingsAgentContextMessagesItemContentParams is ConversationHistoryMessageParams
    assert ModuleContextContentParams is ConversationHistoryMessageParams
    assert AgentContextContentParamsFromV1 is ConversationHistoryMessageParams
    assert AgentContextContentParamsFromAgent is ConversationHistoryMessageParams

    assert AgentV1SettingsAgentContextMessagesItemFunctionCallsParams is FunctionCallHistoryMessageParams
    assert ModuleContextFunctionCallsParams is FunctionCallHistoryMessageParams
    assert AgentContextFunctionCallsParamsFromV1 is FunctionCallHistoryMessageParams
    assert AgentContextFunctionCallsParamsFromAgent is FunctionCallHistoryMessageParams


def test_old_key_request_aliases_resolve_to_new_request_type() -> None:
    assert CreateKeyV1RequestOneType is CreateKeyV1Request
    assert ModuleCreateKeyV1RequestOne is CreateKeyV1Request
    assert CreateKeyV1RequestOne is RootCreateKeyV1Request

    assert CreateKeyV1RequestOneParams is CreateKeyV1RequestParams
    assert ModuleCreateKeyV1RequestOneParams is CreateKeyV1RequestParams


def test_old_agent_history_type_aliases_can_be_instantiated() -> None:
    history_content = AgentV1HistoryContent(type="History", role="user", content="hello")
    assert isinstance(history_content, ConversationHistoryMessage)
    assert history_content.role == "user"
    assert history_content.content == "hello"

    context_content = AgentV1SettingsAgentContextMessagesItemContent(type="History", role="assistant", content="hi")
    assert isinstance(context_content, ConversationHistoryMessage)
    assert context_content.role == "assistant"
    assert context_content.content == "hi"

    function_call = {
        "id": "fc_123",
        "name": "lookup_weather",
        "client_side": True,
        "arguments": '{"city":"London"}',
        "response": "sunny",
    }
    history_function_calls = AgentV1HistoryFunctionCalls(type="History", function_calls=[function_call])
    assert isinstance(history_function_calls, FunctionCallHistoryMessage)
    assert history_function_calls.function_calls[0].name == "lookup_weather"

    context_function_calls = AgentV1SettingsAgentContextMessagesItemFunctionCalls(
        type="History", function_calls=[function_call]
    )
    assert isinstance(context_function_calls, FunctionCallHistoryMessage)
    assert context_function_calls.function_calls[0].response == "sunny"


def test_legacy_settings_agent_context_messages_kwarg_remaps_to_context() -> None:
    from deepgram.agent.v1.types import (
        AgentV1SettingsAgentContext,
        AgentV1SettingsAgentContextContext,
    )

    msg = ConversationHistoryMessage(type="History", role="user", content="hi")

    legacy = AgentV1SettingsAgentContext(messages=[msg])
    canonical = AgentV1SettingsAgentContext(context=AgentV1SettingsAgentContextContext(messages=[msg]))

    assert legacy.dict() == canonical.dict()
    assert legacy.context is not None
    assert legacy.context.messages == [msg]


def test_legacy_settings_agent_context_messages_kwarg_does_not_clobber_explicit_context() -> None:
    from deepgram.agent.v1.types import (
        AgentV1SettingsAgentContext,
        AgentV1SettingsAgentContextContext,
    )

    msg_a = ConversationHistoryMessage(type="History", role="user", content="a")
    msg_b = ConversationHistoryMessage(type="History", role="user", content="b")

    explicit_context_wins = AgentV1SettingsAgentContext(
        context=AgentV1SettingsAgentContextContext(messages=[msg_a]),
        messages=[msg_b],
    )
    assert explicit_context_wins.context is not None
    assert explicit_context_wins.context.messages == [msg_a]


def test_legacy_settings_agent_context_messages_property_reads_nested_context() -> None:
    from deepgram.agent.v1.types import (
        AgentV1SettingsAgentContext,
        AgentV1SettingsAgentContextContext,
    )

    msg = ConversationHistoryMessage(type="History", role="user", content="hi")

    legacy = AgentV1SettingsAgentContext(messages=[msg])
    canonical = AgentV1SettingsAgentContext(context=AgentV1SettingsAgentContextContext(messages=[msg]))

    assert legacy.messages == [msg]
    assert canonical.messages == [msg]


def test_renamed_settings_context_type_aliases_resolve() -> None:
    from deepgram.agent.v1.types import (
        AgentV1SettingsAgentContextContextMessagesItem,
        AgentV1SettingsAgentContextContextMessagesItemContentRole,
        AgentV1SettingsAgentContextContextMessagesItemFunctionCallsFunctionCallsItem,
        AgentV1SettingsAgentContextMessagesItem,
        AgentV1SettingsAgentContextMessagesItemContentRole,
        AgentV1SettingsAgentContextMessagesItemFunctionCallsFunctionCallsItem,
    )

    assert AgentV1SettingsAgentContextMessagesItem is AgentV1SettingsAgentContextContextMessagesItem
    assert AgentV1SettingsAgentContextMessagesItemContentRole is AgentV1SettingsAgentContextContextMessagesItemContentRole
    assert (
        AgentV1SettingsAgentContextMessagesItemFunctionCallsFunctionCallsItem
        is AgentV1SettingsAgentContextContextMessagesItemFunctionCallsFunctionCallsItem
    )


def test_renamed_settings_context_request_aliases_resolve() -> None:
    from deepgram.agent.v1.requests import (
        AgentV1SettingsAgentContextContextMessagesItemFunctionCallsFunctionCallsItemParams,
        AgentV1SettingsAgentContextContextMessagesItemParams,
        AgentV1SettingsAgentContextMessagesItemFunctionCallsFunctionCallsItemParams,
        AgentV1SettingsAgentContextMessagesItemParams,
    )

    assert AgentV1SettingsAgentContextMessagesItemParams is AgentV1SettingsAgentContextContextMessagesItemParams
    assert (
        AgentV1SettingsAgentContextMessagesItemFunctionCallsFunctionCallsItemParams
        is AgentV1SettingsAgentContextContextMessagesItemFunctionCallsFunctionCallsItemParams
    )


def test_legacy_settings_agent_wrapper_preserves_old_wire_shape() -> None:
    from deepgram.agent.v1.types import (
        AgentV1Settings,
        AgentV1SettingsAgent,
        AgentV1SettingsAgentContext,
        AgentV1SettingsAgentContextContext,
        AgentV1SettingsAgentContextListen,
        AgentV1SettingsAgentContextListenProvider_V1,
        AgentV1SettingsAgentListen,
        AgentV1SettingsAgentListenProvider_V1,
        AgentV1SettingsAudio,
        AgentV1SettingsAudioInput,
    )
    from deepgram.types.speak_settings_v1 import SpeakSettingsV1
    from deepgram.types.speak_settings_v1provider import SpeakSettingsV1Provider_Deepgram
    from deepgram.types.think_settings_v1 import ThinkSettingsV1
    from deepgram.types.think_settings_v1provider import ThinkSettingsV1Provider_OpenAi

    msg = ConversationHistoryMessage(type="History", role="user", content="hi")
    audio = AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000))
    think = ThinkSettingsV1(
        provider=ThinkSettingsV1Provider_OpenAi(type="open_ai", model="gpt-4o-mini"),
        prompt="Keep replies brief.",
    )
    speak = SpeakSettingsV1(
        provider=SpeakSettingsV1Provider_Deepgram(type="deepgram", model="aura-2-asteria-en")
    )

    legacy = AgentV1Settings(
        audio=audio,
        agent=AgentV1SettingsAgent(
            language="en",
            greeting="Hello there",
            context=AgentV1SettingsAgentContext(messages=[msg]),
            listen=AgentV1SettingsAgentListen(
                provider=AgentV1SettingsAgentListenProvider_V1(type="deepgram", model="nova-3")
            ),
            think=think,
            speak=speak,
        ),
    )
    canonical = AgentV1Settings(
        audio=audio,
        agent=AgentV1SettingsAgentContext(
            language="en",
            greeting="Hello there",
            context=AgentV1SettingsAgentContextContext(messages=[msg]),
            listen=AgentV1SettingsAgentContextListen(
                provider=AgentV1SettingsAgentContextListenProvider_V1(type="deepgram", model="nova-3")
            ),
            think=think,
            speak=speak,
        ),
    )

    assert legacy.dict() == canonical.dict()
    assert legacy.agent.context is not None
    assert legacy.agent.context.messages == [msg]


def test_settings_agent_still_accepts_agent_id_string() -> None:
    from deepgram.agent.v1.types import AgentV1Settings, AgentV1SettingsAudio, AgentV1SettingsAudioInput

    settings = AgentV1Settings(
        audio=AgentV1SettingsAudio(input=AgentV1SettingsAudioInput(encoding="linear16", sample_rate=24000)),
        agent="agent_123",
    )

    assert settings.agent == "agent_123"


def test_agent_settings_audio_output_container_still_accepts_arbitrary_strings() -> None:
    from deepgram.agent.v1.types import AgentV1SettingsAudioOutput

    output = AgentV1SettingsAudioOutput(container="webm")

    assert output.container == "webm"
