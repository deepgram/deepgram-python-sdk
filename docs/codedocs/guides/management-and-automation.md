---
title: "Management And Automation"
description: "Automate projects, keys, usage reporting, agent assets, and self-hosted credentials from one client."
---

The SDK is not only for speech and agent runtime traffic. It also includes administrative APIs for projects, keys, usage, billing, reusable voice-agent assets, and self-hosted distribution credentials.

<Steps>
<Step>

### Start from the management domains

Administrative features are split across three major roots:

- `client.manage.v1` for project, key, usage, billing, and model APIs,
- `client.voice_agent` for reusable agent configs and variables,
- `client.self_hosted.v1` for distribution credentials.

</Step>
<Step>

### List projects and inspect one project

```python
from deepgram import DeepgramClient

client = DeepgramClient()

projects = client.manage.v1.projects.list()
project = client.manage.v1.projects.get(project_id=projects.projects[0].project_id)
print(project.name)
```

</Step>
<Step>

### Create operational assets

```python
project_id = "PROJECT_ID"

key = client.manage.v1.projects.keys.create(
    project_id=project_id,
    request={"comment": "automation key", "scopes": ["usage:read"]},
)

variable = client.voice_agent.variables.create(
    project_id=project_id,
    key="DG_SUPPORT_QUEUE",
    value="priority-escalation",
)
```

</Step>
<Step>

### Pull usage and self-hosted data

```python
usage = client.manage.v1.projects.usage.get(
    project_id=project_id,
    start="2026-04-01",
    end="2026-04-30",
    model="nova-3",
)

credentials = client.self_hosted.v1.distribution_credentials.list(project_id=project_id)
print(usage.resolution)
print(credentials.distribution_credentials)
```

</Step>
</Steps>

## Complete Example

```python
from deepgram import DeepgramClient

client = DeepgramClient()
project_id = "PROJECT_ID"

projects = client.manage.v1.projects.list()
print(f"project count={len(projects.projects)}")

usage = client.manage.v1.projects.usage.get(
    project_id=project_id,
    start="2026-04-01",
    end="2026-04-30",
    tag="support",
)

config = client.voice_agent.configurations.create(
    project_id=project_id,
    config='{"listen":{"provider":{"type":"deepgram","model":"nova-3"}}}',
    metadata={"owner": "ops"},
)

print(usage.resolution)
print(config.agent_id)
```

## Recommended Pattern

- Keep runtime and control-plane credentials separate when possible.
- Use project-level tagging on speech requests so `usage.get(...)` becomes useful later.
- Treat `voice_agent.configurations` and `self_hosted.v1.distribution_credentials` as deployment assets, not throwaway runtime calls.
