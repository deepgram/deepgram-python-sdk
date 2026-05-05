"""
Manual back-compat smoke test for the SDK regen on 2026-04-29.

Proves the legacy public symbols this PR aliases still work end to end:
  1. module-level identity with the new canonical names
  2. in-memory instantiation through the old class names
  3. TypedDict params usable as the old alias on the new method signature
  4. real wire round-trip via keys.create + keys.delete using
     CreateKeyV1RequestOneParams against the production API

This is *not* a usage example. New code should import the canonical names
(ConversationHistoryMessage, FunctionCallHistoryMessage, CreateKeyV1Request,
CreateKeyV1RequestParams, etc.). This script exists so we can demonstrate
that existing 7.0.0 caller code continues to work without modification.

Requires DEEPGRAM_API_KEY in the environment for step 4. Steps 1-3 are
offline.
"""

from dotenv import load_dotenv

print("Starting backwards-compatibility manual test")
load_dotenv()
print("Environment variables loaded")

# Legacy alias imports — what user code on 7.0.0 looked like.
from deepgram import CreateKeyV1RequestOne
from deepgram.agent.v1.types import (
    AgentV1HistoryContent,
    AgentV1HistoryFunctionCalls,
    AgentV1SettingsAgentContextMessagesItemContent,
    AgentV1SettingsAgentContextMessagesItemFunctionCalls,
)
from deepgram.requests import CreateKeyV1RequestOneParams
from deepgram.types import CreateKeyV1RequestOne as CreateKeyV1RequestOneType

# Canonical (current) names — used as the RHS of identity assertions.
from deepgram import CreateKeyV1Request, DeepgramClient
from deepgram.agent.v1.types import (
    ConversationHistoryMessage,
    FunctionCallHistoryMessage,
)
from deepgram.requests import CreateKeyV1RequestParams  # noqa: F401  (imported for parity)


print("\n[1/4] Identity: legacy aliases resolve to the same class object as the canonical names")
assert CreateKeyV1RequestOne is CreateKeyV1Request
assert CreateKeyV1RequestOneType is CreateKeyV1Request
assert AgentV1HistoryContent is ConversationHistoryMessage
assert AgentV1HistoryFunctionCalls is FunctionCallHistoryMessage
assert AgentV1SettingsAgentContextMessagesItemContent is ConversationHistoryMessage
assert AgentV1SettingsAgentContextMessagesItemFunctionCalls is FunctionCallHistoryMessage
print("  PASS: all legacy aliases share class identity with the canonical types")


print("\n[2/4] Construction: legacy class names build and validate")

history_content = AgentV1HistoryContent(type="History", role="user", content="Hello")
print(
    f"  AgentV1HistoryContent -> {type(history_content).__name__}"
    f" role={history_content.role!r} content={history_content.content!r}"
)

history_function_calls = AgentV1HistoryFunctionCalls(
    type="History",
    function_calls=[
        {
            "id": "fc_demo",
            "name": "lookup_weather",
            "client_side": True,
            "arguments": '{"city":"London"}',
            "response": "sunny",
        }
    ],
)
print(
    f"  AgentV1HistoryFunctionCalls -> {type(history_function_calls).__name__}"
    f" function_calls[0].name={history_function_calls.function_calls[0].name!r}"
)

context_content = AgentV1SettingsAgentContextMessagesItemContent(
    type="History", role="assistant", content="hi"
)
print(f"  AgentV1SettingsAgentContextMessagesItemContent -> {type(context_content).__name__}")

context_function_calls = AgentV1SettingsAgentContextMessagesItemFunctionCalls(
    type="History",
    function_calls=[
        {
            "id": "fc_demo2",
            "name": "lookup_time",
            "client_side": False,
            "arguments": "{}",
            "response": "noon",
        }
    ],
)
print(
    f"  AgentV1SettingsAgentContextMessagesItemFunctionCalls -> {type(context_function_calls).__name__}"
)
print("  PASS: legacy names instantiate and validate correctly")


print("\n[3/4] Typed-dict alias: CreateKeyV1RequestOneParams usable as a request payload")
key_request: CreateKeyV1RequestOneParams = {
    "comment": "back-compat smoke test",
    "scopes": ["usage:read"],
}
print(f"  Built request typed as CreateKeyV1RequestOneParams: {key_request}")


print("\n[4/4] Wire round-trip: keys.create + keys.delete via the legacy alias")
try:
    client = DeepgramClient()
    projects = client.manage.v1.projects.list().projects
    if not projects:
        print("  SKIP: no projects on this account")
    else:
        project_id = projects[0].project_id
        print(f"  Using project: {project_id}")

        created = client.manage.v1.projects.keys.create(
            project_id=project_id, request=key_request
        )
        print(f"  PASS: created key {created.api_key_id} via legacy alias")

        client.manage.v1.projects.keys.delete(
            project_id=project_id, key_id=created.api_key_id
        )
        print(f"  PASS: deleted key {created.api_key_id}")
except Exception as e:
    print(f"  FAIL: {type(e).__name__}: {e}")
    raise

print("\nBackwards-compatibility smoke test completed.")
