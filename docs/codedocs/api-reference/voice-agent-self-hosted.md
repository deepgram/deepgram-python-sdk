---
title: "Voice Agent And Self-Hosted"
description: "Reference for reusable voice-agent assets and self-hosted distribution credentials."
---

This page covers the two control-plane domains that sit outside the core runtime websocket: reusable voice-agent assets and self-hosted distribution credentials.

## Imports

```python
from deepgram import DeepgramClient
```

## `voice_agent.configurations`

Source: `src/deepgram/voice_agent/configurations/client.py`

```python
list(project_id: str, *, request_options: RequestOptions | None = None) -> ListAgentConfigurationsV1Response
create(project_id: str, *, config: str, metadata: dict[str, str] | None = OMIT, api_version: int | None = OMIT, request_options: RequestOptions | None = None) -> CreateAgentConfigurationV1Response
get(project_id: str, agent_id: str, *, request_options: RequestOptions | None = None) -> AgentConfigurationV1
update(project_id: str, agent_id: str, *, metadata: dict[str, str], request_options: RequestOptions | None = None) -> AgentConfigurationV1
delete(project_id: str, agent_id: str, *, request_options: RequestOptions | None = None) -> DeleteAgentConfigurationV1Response
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_id` | `str` | — | Project that owns the config. |
| `config` | `str` | — | JSON string representing the `agent` block from a settings message. |
| `metadata` | `dict[str, str] \| None` | omitted | Labels for organization or deployment metadata. |
| `api_version` | `int \| None` | omitted | Configuration API version. |
| `agent_id` | `str` | — | Stored configuration UUID. |

## `voice_agent.variables`

Source: `src/deepgram/voice_agent/variables/client.py`

```python
list(project_id: str, *, request_options: RequestOptions | None = None) -> ListAgentVariablesV1Response
create(project_id: str, *, key: str, value: Any, api_version: int | None = OMIT, request_options: RequestOptions | None = None) -> AgentVariableV1
get(project_id: str, variable_id: str, *, request_options: RequestOptions | None = None) -> AgentVariableV1
delete(project_id: str, variable_id: str, *, request_options: RequestOptions | None = None) -> DeleteAgentVariableV1Response
update(project_id: str, variable_id: str, *, value: Any, request_options: RequestOptions | None = None) -> AgentVariableV1
```

Variables follow the `DG_<NAME>` style naming noted in the generated docstring and can substitute any JSON value into stored agent configurations.

## `self_hosted.v1.distribution_credentials`

Source: `src/deepgram/self_hosted/v1/distribution_credentials/client.py`

```python
list(project_id: str, *, request_options: RequestOptions | None = None) -> ListProjectDistributionCredentialsV1Response
create(
    project_id: str,
    *,
    scopes: DistributionCredentialsCreateRequestScopesItem | Sequence[DistributionCredentialsCreateRequestScopesItem] | None = None,
    provider: Literal["quay"] | None = None,
    comment: str | None = OMIT,
    request_options: RequestOptions | None = None,
) -> CreateProjectDistributionCredentialsV1Response
get(project_id: str, distribution_credentials_id: str, *, request_options: RequestOptions | None = None) -> GetProjectDistributionCredentialsV1Response
delete(project_id: str, distribution_credentials_id: str, *, request_options: RequestOptions | None = None) -> GetProjectDistributionCredentialsV1Response
```

## Example

```python
config = client.voice_agent.configurations.create(
    project_id="PROJECT_ID",
    config='{"listen":{"provider":{"type":"deepgram","model":"nova-3"}}}',
    metadata={"team": "ops"},
)

credential = client.self_hosted.v1.distribution_credentials.create(
    project_id="PROJECT_ID",
    scopes=["self-hosted:products"],
    provider="quay",
    comment="CI pull credential",
)
```
