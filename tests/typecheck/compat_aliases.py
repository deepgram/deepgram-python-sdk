from typing import Literal

from typing_extensions import assert_type  # 3.10-compatible backport (typing.assert_type is 3.11+)

from deepgram import (
    DeepgramThinkProviderReasoningMode,
    DeepgramThinkLiveProviderV1,
    DeepgramThinkLiveProviderV1Params,
    ThinkLiveSettingsV1,
    ThinkLiveSettingsV1Params,
    ThinkSettingsV1FunctionsItem,
    ThinkSettingsV1FunctionsItemParams,
    ThinkSettingsV1Provider_Deepgram,
    ThinkSettingsV1Provider_DeepgramParams,
)
from deepgram import (
    ListenV1LanguageHint as RootListenV1LanguageHint,
)
from deepgram import (
    ListenV1LanguageHintParams as RootListenV1LanguageHintParams,
)
from deepgram.agent.v1.requests import (
    AgentV1ConversationTextParams,
    AgentV1HistoryContentParams,
    AgentV1HistoryFunctionCallsParams,
    AgentV1InjectDynamicAgentMessageParams,
    AgentV1ThinkLiveUpdatedParams,
    AgentV1UpdateThinkLiveParams,
    ConversationHistoryMessageParams,
    FunctionCallHistoryMessageParams,
)
from deepgram.agent.v1.types import (
    AgentV1ConversationTextConversationalBehavior,
    AgentV1InjectDynamicAgentMessage,
    AgentV1InjectDynamicAgentMessageBehavior,
    AgentV1ThinkLiveUpdated,
    AgentV1UpdateThinkLive,
)
from deepgram.listen import ListenV1ConfigureFailureCode as RootListenV1ConfigureFailureCode
from deepgram.listen.v1 import ListenV1ConfigureFailureCode as V1ListenV1ConfigureFailureCode
from deepgram.listen.v1.requests import ListenV1ConfigureFailureParams
from deepgram.listen.v1.types import ListenV1ConfigureFailure, ListenV1ConfigureFailureCode
from deepgram.requests import (
    CreateKeyV1RequestOneParams,
    CreateKeyV1RequestParams,
    ListenV1LanguageHintParams,
    SharedIntentsParams,
    SharedTopicsParams,
)
from deepgram.requests import (
    DeepgramThinkLiveProviderV1Params as RequestsDeepgramThinkLiveProviderV1Params,
)
from deepgram.requests import (
    ThinkLiveSettingsV1Params as RequestsThinkLiveSettingsV1Params,
)
from deepgram.requests import (
    ThinkSettingsV1FunctionsItemParams as RequestsThinkSettingsV1FunctionsItemParams,
)
from deepgram.requests import (
    ThinkSettingsV1Provider_DeepgramParams as RequestsThinkSettingsV1Provider_DeepgramParams,
)
from deepgram.types import (
    DeepgramThinkLiveProviderV1 as TypesDeepgramThinkLiveProviderV1,
)
from deepgram.types import (
    ListenV1LanguageHint,
    SharedIntents,
    SharedTopics,
)
from deepgram.types import (
    ThinkLiveSettingsV1 as TypesThinkLiveSettingsV1,
)
from deepgram.types import (
    ThinkSettingsV1FunctionsItem as TypesThinkSettingsV1FunctionsItem,
)
from deepgram.types import (
    ThinkSettingsV1Provider_Deepgram as TypesThinkSettingsV1Provider_Deepgram,
)

create_key_request: CreateKeyV1RequestOneParams = {"key": "value"}
history_content: AgentV1HistoryContentParams = {
    "type": "History",
    "role": "user",
    "content": "hello",
}
history_function_calls: AgentV1HistoryFunctionCallsParams = {
    "type": "History",
    "function_calls": [
        {
            "id": "fc_123",
            "name": "lookup_weather",
            "client_side": True,
            "arguments": '{"city":"London"}',
            "response": "sunny",
        }
    ],
}

assert_type(create_key_request, CreateKeyV1RequestParams)
assert_type(history_content, ConversationHistoryMessageParams)
assert_type(history_function_calls, FunctionCallHistoryMessageParams)

# Think Live models, params, and Agent V1 controls are all part of the public
# barrels. These assignments cover presence checks, function filler controls,
# dynamic injection behavior, updates, and response events.
think_live_provider_params: DeepgramThinkLiveProviderV1Params = {
    "type": "deepgram",
    "version": "v1",
    "presence_check_max_count": 3,
    "presence_check_interval_ms": 5000,
}
think_live_settings_params: ThinkLiveSettingsV1Params = {"provider": think_live_provider_params}
filler_function_params: ThinkSettingsV1FunctionsItemParams = {
    "defer_until_eot": True,
    "initial_agent_filler": True,
    "agent_filler_max_count": 2,
    "agent_filler_interval_ms": 3000,
}
dynamic_behavior: AgentV1InjectDynamicAgentMessageBehavior = "queue"
conversation_behavior: AgentV1ConversationTextConversationalBehavior = "filler"
dynamic_injection_params: AgentV1InjectDynamicAgentMessageParams = {
    "type": "InjectAgentMessage",
    "is_dynamic": True,
    "behavior": dynamic_behavior,
}
think_live_update_params: AgentV1UpdateThinkLiveParams = {
    "type": "UpdateThink_Live",
    "think_live": think_live_settings_params,
}
think_live_updated_params: AgentV1ThinkLiveUpdatedParams = {"type": "ThinkLiveUpdated"}
legacy_conversation_text_params: AgentV1ConversationTextParams = {
    "type": "ConversationText",
    "role": "assistant",
    "content": "I am still here.",
}

think_live_provider = DeepgramThinkLiveProviderV1(presence_check_max_count=3, presence_check_interval_ms=5000)
think_live_settings = ThinkLiveSettingsV1(provider=think_live_provider)
deepgram_reasoning_mode: DeepgramThinkProviderReasoningMode = "none"
deepgram_think_provider_params: ThinkSettingsV1Provider_DeepgramParams = {
    "type": "deepgram",
    "version": "v1",
    "model": "think-fast",
    "temperature": 0.2,
    "reasoning_mode": deepgram_reasoning_mode,
    "voice_prompt_opt_out": True,
}
deepgram_think_provider = ThinkSettingsV1Provider_Deepgram(**deepgram_think_provider_params)
filler_function = ThinkSettingsV1FunctionsItem(
    defer_until_eot=True,
    initial_agent_filler=True,
    agent_filler_max_count=2,
    agent_filler_interval_ms=3000,
)
dynamic_injection = AgentV1InjectDynamicAgentMessage(behavior=dynamic_behavior)
think_live_update = AgentV1UpdateThinkLive(think_live=think_live_settings)
think_live_updated = AgentV1ThinkLiveUpdated()

assert_type(think_live_provider, TypesDeepgramThinkLiveProviderV1)
assert_type(think_live_settings, TypesThinkLiveSettingsV1)
assert_type(filler_function, TypesThinkSettingsV1FunctionsItem)
assert_type(dynamic_injection.behavior, AgentV1InjectDynamicAgentMessageBehavior | None)
assert_type(think_live_update.think_live, ThinkLiveSettingsV1)
assert_type(think_live_updated.type, Literal["ThinkLiveUpdated"])
assert_type(think_live_provider_params, RequestsDeepgramThinkLiveProviderV1Params)
assert_type(think_live_settings_params, RequestsThinkLiveSettingsV1Params)
assert_type(filler_function_params, RequestsThinkSettingsV1FunctionsItemParams)
assert_type(deepgram_think_provider_params, RequestsThinkSettingsV1Provider_DeepgramParams)
assert_type(deepgram_think_provider, TypesThinkSettingsV1Provider_Deepgram)

# language_hint backward-compat: the deprecated singular kwarg (str or list) must
# keep type-checking on the V2 listen provider, alongside the canonical plural.
# If the deprecated `language_hint` field is ever dropped, these fail type-checking
# and gate the regression (this file is type-checked by CI, not executed).
from deepgram.types.deepgram_listen_provider_v2 import DeepgramListenProviderV2

_language_hint_str = DeepgramListenProviderV2(model="flux-general-multi", language_hint="en")
_language_hint_list = DeepgramListenProviderV2(model="flux-general-multi", language_hint=["en", "de"])
_language_hints_plural = DeepgramListenProviderV2(model="flux-general-multi", language_hints=["fr"])

# Nova-3 multilingual language hints are public from the root and the type/request
# barrels. The wire accepts scalar hints and repeats a sequence as query parameters.
model_hint_scalar: RootListenV1LanguageHint = "en"
model_hint_list: ListenV1LanguageHint = ["en", "es"]
params_hint_scalar: RootListenV1LanguageHintParams = "en"
params_hint_list: ListenV1LanguageHintParams = ["en", "es"]
params_hint_sequence: ListenV1LanguageHintParams = ("en", "es")
assert_type(model_hint_scalar, ListenV1LanguageHint)
assert_type(model_hint_list, RootListenV1LanguageHint)
assert_type(params_hint_scalar, ListenV1LanguageHintParams)
assert_type(params_hint_list, RootListenV1LanguageHintParams)
assert_type(params_hint_sequence, ListenV1LanguageHintParams)

# Configure failures expose a forward-compatible code union through all public
# Listen barrels. Both the model and Params TypedDict retain that open alias.
known_configure_failure_code: RootListenV1ConfigureFailureCode = "CONFIGURE_KEYTERM_LIMIT_EXCEEDED"
future_configure_failure_code: V1ListenV1ConfigureFailureCode = "CONFIGURE_FUTURE_REASON"
configure_failure = ListenV1ConfigureFailure(
    request_id="550e8400-e29b-41d4-a716-446655440000",
    code=known_configure_failure_code,
    description="Keyterms exceed the limit.",
)
configure_failure_params: ListenV1ConfigureFailureParams = {
    "type": "ConfigureFailure",
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "code": future_configure_failure_code,
    "description": "A future server failure code is still readable.",
}
assert_type(configure_failure.code, ListenV1ConfigureFailureCode)
assert_type(configure_failure_params["code"], ListenV1ConfigureFailureCode)

# Topics and Intents retain their pre-7.12 ``results`` construction and Params paths.
legacy_topics: SharedTopicsParams = {"results": {"topics": {"segments": [{"text": "hello"}]}}}
legacy_intents: SharedIntentsParams = {"results": {"intents": {"segments": [{"text": "hello"}]}}}
assert_type(SharedTopics(results=legacy_topics["results"]), SharedTopics)
assert_type(SharedIntents(results=legacy_intents["results"]), SharedIntents)
