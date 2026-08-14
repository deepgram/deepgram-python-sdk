---
name: deepgram-python-management-api
description: Use when writing or reviewing Python code in this repo that calls Deepgram Management APIs - projects, API keys, members, invites, usage, billing, models, and reusable Voice Agent configurations. Covers `client.manage.v1.projects`, project-scoped resources under `client.manage.v1.projects.*` (keys, members, members.invites, usage, billing, models, requests), global `client.manage.v1.models`, think-model discovery at `client.agent.v1.settings.think.models`, and `client.voice_agent.configurations.*`. Use `deepgram-python-voice-agent` when you want to run an agent interactively, this skill to PERSIST/LIST agent configs. Triggers include "management API", "list projects", "API keys", "members", "usage stats", "billing", "list models", "agent configurations", "manage.v1".
---

# Using Deepgram Management API (Python SDK)

Administrative REST endpoints at `api.deepgram.com/v1/projects`, `/v1/models`, and reusable agent configuration storage. Project-scoped resources live under `client.manage.v1.projects.*` (keys, members, members.invites, usage, billing, models, requests). Global models at `client.manage.v1.models`. Think-model discovery at `client.agent.v1.settings.think.models`. Reusable agent configs at `client.voice_agent.configurations.*`.

**Use a different skill when:**
- Running an agent interactively → `deepgram-python-voice-agent`.
- Transcribing or synthesizing → STT/TTS skills.

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

All project-scoped resources live under `client.manage.v1.projects.*`:

```python
# Keys — `create` takes a single `request=` payload, not top-level kwargs
keys = client.manage.v1.projects.keys.list(project_id=pid)
client.manage.v1.projects.keys.create(
    project_id=pid,
    request={"comment": "CI key", "scopes": ["usage:write"]},
)
client.manage.v1.projects.keys.delete(project_id=pid, key_id=kid)

# Members + invites (invites are nested under members; method is `create`, not `send`)
members = client.manage.v1.projects.members.list(project_id=pid)
invites = client.manage.v1.projects.members.invites.list(project_id=pid)
client.manage.v1.projects.members.invites.create(project_id=pid, email="new@example.com", scope="member")

# Usage (get, not list) + billing balances (nested)
usage = client.manage.v1.projects.usage.get(project_id=pid)
usage_breakdown = client.manage.v1.projects.usage.breakdown.list(project_id=pid)
balance = client.manage.v1.projects.billing.balances.get(project_id=pid)
```

See `examples/51-55` for each sub-module.

## Quick start — Voice Agent configurations

**Important:** The stored config is the `agent` block only (listen/think/speak providers + prompt) as a JSON string, NOT the full `AgentV1Settings`. Top-level fields like `audio` go in the live Settings message at connect time. The returned `agent_id` replaces the inline `agent` object in future Settings messages. Configs are immutable -- create a new one to change behavior; only metadata is mutable.

```python
import json
configs = client.voice_agent.configurations.list(project_id=pid)

config_json = json.dumps({
    "listen": {"provider": {"type": "deepgram", "model": "nova-3"}},
    "think":  {"provider": {"type": "open_ai", "model": "gpt-4o-mini"}, "prompt": "..."},
    "speak":  {"provider": {"type": "deepgram", "model": "aura-2-asteria-en"}},
})
created = client.voice_agent.configurations.create(
    project_id=pid, config=config_json, metadata={"label": "support-en"},
)
print(created.agent_id)

client.voice_agent.configurations.update(project_id=pid, agent_id=created.agent_id, metadata={"label": "v2"})
one = client.voice_agent.configurations.get(project_id=pid, agent_id=created.agent_id)
```

Think-provider model discovery (which LLMs Agent supports):

```python
think_models = client.agent.v1.settings.think.models.list()
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

## Destructive operation guard

Delete operations (projects, keys, agent configs) are **irreversible**. Always verify the resource before deleting:

```python
# Confirm before deleting a key
key = client.manage.v1.projects.keys.list(project_id=pid)
target = next((k for k in key.api_keys if k.api_key_id == kid), None)
assert target is not None, f"Key {kid} not found"
print(f"Deleting key: {target.comment}")
client.manage.v1.projects.keys.delete(project_id=pid, key_id=kid)
```

## Gotchas

1. **`Token` auth, not `Bearer`.**
2. **Project-scoped resources are nested under `.projects.*`.** No top-level `client.manage.v1.keys` etc. Use `client.manage.v1.projects.keys`, `...projects.members`, `...projects.members.invites`, `...projects.usage`, `...projects.billing.balances`, `...projects.requests`.
3. **Think-model discovery is on the Agent client**, not Manage: `client.agent.v1.settings.think.models.list()`.
4. **Agent config body is a JSON STRING on create**: pass `config=json.dumps(...)`. See the Voice Agent configurations section above for full details.
5. **Use `include_outdated=True`** on `models.list()` when pinning older models.
6. **Project-scoped vs global models**: `client.manage.v1.models.list()` returns all; `client.manage.v1.projects.models.list(project_id=...)` returns what the project can access.
7. **Returned agent configs are uninterpolated** -- raw stored JSON string. Parse before use.

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

- `deepgram-python-voice-agent` — run an agent (use a config created here)

For cross-language Deepgram product knowledge, install the central skills: `npx skills add deepgram/skills`.
