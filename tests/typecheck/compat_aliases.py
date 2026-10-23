from typing_extensions import assert_type  # 3.10-compatible backport (typing.assert_type is 3.11+)

from deepgram import (
    ListenV1LanguageHint as RootListenV1LanguageHint,
)
from deepgram import (
    ListenV1LanguageHintParams as RootListenV1LanguageHintParams,
)
from deepgram.agent.v1.requests import (
    AgentV1HistoryContentParams,
    AgentV1HistoryFunctionCallsParams,
    ConversationHistoryMessageParams,
    FunctionCallHistoryMessageParams,
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
from deepgram.types import ListenV1LanguageHint, SharedIntents, SharedTopics

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
