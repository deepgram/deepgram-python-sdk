---
name: using-management-api
description: Use when writing or reviewing Python code in this repo that calls Deepgram Management APIs - projects, API keys, members, invites, usage, billing, models, and reusable Voice Agent configurations. Covers `client.manage.v1.*` (projects/keys/members/invites/usage/billing/models) and `client.voice_agent.configurations.*`. Use `using-voice-agent` when you want to run an agent interactively, this skill to PERSIST/LIST agent configs. Triggers include "management API", "list projects", "API keys", "members", "usage stats", "billing", "list models", "agent configurations", "manage.v1".
---

# Using Deepgram Management API (Python SDK)

Administrative REST endpoints at `api.deepgram.com/v1/projects`, `/v1/models`, and reusable agent configuration storage. All `client.manage.v1.*` + `client.voice_agent.configurations.*`.

## When to use this product

- **Discover / pin models**: `client.manage.v1.models.list()` returns the active STT/TTS set.
- **Project admin**: list/get/update/delete/leave projects.
- **API key lifecycle**: list/create/delete project keys.
- **Member + invite management**: add/remove members, manage roles, send/revoke invites.
- **Usage + billing**: query request volume, balances.
- **Reusable Voice Agent configs**: persist an `AgentV1Settings`-shaped config on the server, reference by `agent_id`.

**Use a different skill when:**
- You want to actually talk to an agent → `using-voice-agent`.
- You want to transcribe or synthesize → STT/TTS skills.

## Authentication

```python
from dotenv import load_dotenv
load_dotenv()

from deepgram import DeepgramClient
client = DeepgramClient()
```

Header: `Authorization: Token <api_key>`. All methods are REST.

## Quick start — projects + models

```python
# Projects
projects = client.manage.v1.projects.list()
for p in projects.projects:
    print(p.project_id, p.name)

project = client.manage.v1.projects.get(project_id=projects.projects[0].project_id)
client.manage.v1.projects.update(project_id=project.project_id, name="New name")
# client.manage.v1.projects.delete(project_id=...)   # irreversible
# client.manage.v1.projects.leave(project_id=...)

# Models
models = client.manage.v1.models.list()
print("STT:", [m.canonical_name for m in models.stt])
print("TTS:", [m.canonical_name for m in models.tts])

# Include deprecated/outdated models
older = client.manage.v1.models.list(include_outdated=True)

# Per-project model access
project_models = client.manage.v1.projects.models.list(project_id=project.project_id)
```

## Quick start — keys / members / invites / usage / billing

```python
# Keys
keys = client.manage.v1.keys.list(project_id=pid)
client.manage.v1.keys.create(project_id=pid, comment="CI key", scopes=["usage:write"])
client.manage.v1.keys.delete(project_id=pid, key_id=kid)

# Members + invites
members = client.manage.v1.members.list(project_id=pid)
invites = client.manage.v1.invites.list(project_id=pid)
client.manage.v1.invites.send(project_id=pid, email="new@example.com", scope="member")

# Usage + billing
usage = client.manage.v1.usage.list(project_id=pid)
balance = client.manage.v1.billing.get(project_id=pid)
```

See `examples/51-55` for each sub-module.

## Quick start — Voice Agent configurations

```python
# List reusable configs
configs = client.voice_agent.configurations.list(project_id=pid)

# Create (config is a JSON string of the AgentV1Settings shape)
import json
config_json = json.dumps({
    "audio": {"input": {"encoding": "linear16", "sample_rate": 24000}},
    "agent": {
        "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
        "think":  {"provider": {"type": "open_ai", "model": "gpt-4o-mini"}, "prompt": "..."},
        "speak":  {"provider": {"type": "deepgram", "model": "aura-2-asteria-en"}},
    },
})
created = client.voice_agent.configurations.create(
    project_id=pid,
    config=config_json,
    metadata={"label": "support-en"},
)
print(created.agent_id)

# Update metadata (immutable config body — create a new one to change behavior)
client.voice_agent.configurations.update(project_id=pid, agent_id=created.agent_id, metadata={"label": "v2"})

# Get / delete
one = client.voice_agent.configurations.get(project_id=pid, agent_id=created.agent_id)
# client.voice_agent.configurations.delete(project_id=pid, agent_id=...)
```

Think-provider model discovery (which LLMs Agent supports):

```python
think_models = client.manage.v1.agent.settings.think.models.list()
```

## Async equivalent

```python
from deepgram import AsyncDeepgramClient
client = AsyncDeepgramClient()
projects = await client.manage.v1.projects.list()
```

## API reference (layered)

1. **In-repo reference**: `reference.md` — "Manage V1 Projects/Keys/Members/Invites/Usage/Billing/Models", "Voice Agent Configurations".
2. **OpenAPI (REST)**: https://developers.deepgram.com/openapi.yaml
3. **Context7**: library ID `/llmstxt/developers_deepgram_llms_txt`.
4. **Product docs**:
   - https://developers.deepgram.com/reference/manage/projects/list
   - https://developers.deepgram.com/reference/manage/models/list
   - https://developers.deepgram.com/reference/voice-agent/agent-configurations/list-agent-configurations
   - https://developers.deepgram.com/reference/voice-agent/agent-configurations/create-agent-configuration
   - https://developers.deepgram.com/reference/voice-agent/think-models

## Gotchas

1. **`Token` auth, not `Bearer`.**
2. **Agent config body is a JSON STRING on create**, not a nested object. Pass `config=json.dumps(...)`.
3. **Agent configs are immutable** — you cannot edit the config body. Create a new one to change behavior. Only metadata is mutable.
4. **Use `include_outdated=True`** on `models.list()` when pinning older models.
5. **Delete is irreversible.** Wire tests typically comment out destructive calls.
6. **Project-scoped vs global models**: `client.manage.v1.models.list()` returns all; `client.manage.v1.projects.models.list(project_id=...)` returns what the project can access.
7. **Returned agent configs are uninterpolated** — raw stored JSON string. Parse before use.

## Example files in this repo

- `examples/50-management-projects.py`
- `examples/51-management-keys.py`
- `examples/52-management-members.py`
- `examples/53-management-invites.py`
- `examples/54-management-usage.py`
- `examples/55-management-billing.py`
- `examples/56-management-models.py`
- `tests/wire/test_manage_v1_projects.py`
- `tests/wire/test_manage_v1_models.py`
- `tests/wire/test_voiceAgent_configurations.py`

## Related skills

- `using-voice-agent` — run an agent (use a config created here)
