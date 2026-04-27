---
title: "Manage"
description: "Reference for project, key, model, usage, and billing administration APIs."
---

The Manage domain is the administrative control plane for Deepgram projects. It is broad, so this page groups methods by subclient.

## Imports

```python
from deepgram import DeepgramClient
```

Source files include:

- `src/deepgram/manage/v1/projects/client.py`
- `src/deepgram/manage/v1/projects/keys/client.py`
- `src/deepgram/manage/v1/projects/usage/client.py`
- `src/deepgram/manage/v1/models/client.py`

## `ProjectsClient`

Import path: `client.manage.v1.projects`

```python
list(*, request_options: RequestOptions | None = None) -> ListProjectsV1Response
get(project_id: str, *, limit: float | None = None, page: float | None = None, request_options: RequestOptions | None = None) -> GetProjectV1Response
delete(project_id: str, *, request_options: RequestOptions | None = None) -> DeleteProjectV1Response
update(project_id: str, *, name: str | None = OMIT, request_options: RequestOptions | None = None) -> UpdateProjectV1Response
leave(project_id: str, *, request_options: RequestOptions | None = None) -> LeaveProjectV1Response
```

| Method | Description |
|--------|-------------|
| `list()` | Return projects visible to the API key. |
| `get()` | Fetch one project, optionally paginating embedded results. |
| `update()` | Rename or update project properties. |
| `delete()` | Delete a project. |
| `leave()` | Remove the authenticated member from a project. |

## `KeysClient`

Import path: `client.manage.v1.projects.keys`

```python
list(project_id: str, *, status: KeysListRequestStatus | None = None, request_options: RequestOptions | None = None) -> ListProjectKeysV1Response
create(project_id: str, *, request: CreateKeyV1RequestOne, request_options: RequestOptions | None = None) -> CreateKeyV1Response
get(project_id: str, key_id: str, *, request_options: RequestOptions | None = None) -> GetProjectKeyV1Response
delete(project_id: str, key_id: str, *, request_options: RequestOptions | None = None) -> DeleteProjectKeyV1Response
```

## `ModelsClient`

Import paths:

- `client.manage.v1.models`
- `client.manage.v1.projects.models`

```python
list(*, request_options: RequestOptions | None = None) -> ListModelsV1Response
get(model_id: str, *, request_options: RequestOptions | None = None) -> GetModelV1Response
```

## `UsageClient`

Import path: `client.manage.v1.projects.usage`

```python
get(
    project_id: str,
    *,
    start: str | None = None,
    end: str | None = None,
    accessor: str | None = None,
    alternatives: bool | None = None,
    callback_method: bool | None = None,
    callback: bool | None = None,
    channels: bool | None = None,
    custom_intent_mode: bool | None = None,
    custom_intent: bool | None = None,
    custom_topic_mode: bool | None = None,
    custom_topic: bool | None = None,
    deployment: UsageGetRequestDeployment | None = None,
    detect_entities: bool | None = None,
    detect_language: bool | None = None,
    diarize: bool | None = None,
    dictation: bool | None = None,
    encoding: bool | None = None,
    endpoint: UsageGetRequestEndpoint | None = None,
    extra: bool | None = None,
    filler_words: bool | None = None,
    intents: bool | None = None,
    keyterm: bool | None = None,
    keywords: bool | None = None,
    language: bool | None = None,
    measurements: bool | None = None,
    method: UsageGetRequestMethod | None = None,
    model: str | None = None,
    multichannel: bool | None = None,
    numerals: bool | None = None,
    paragraphs: bool | None = None,
    profanity_filter: bool | None = None,
    punctuate: bool | None = None,
    redact: bool | None = None,
    replace: bool | None = None,
    sample_rate: bool | None = None,
    search: bool | None = None,
    sentiment: bool | None = None,
    smart_format: bool | None = None,
    summarize: bool | None = None,
    tag: str | None = None,
    topics: bool | None = None,
    utt_split: bool | None = None,
    utterances: bool | None = None,
    version: bool | None = None,
    request_options: RequestOptions | None = None,
) -> UsageV1Response
```

The `get(...)` signature is intentionally large because it can filter by endpoint shape and nearly every major request feature used across the API surface.

Additional usage subclients:

- `client.manage.v1.projects.usage.breakdown.get(...)`
- `client.manage.v1.projects.usage.fields.list(...)`

## Billing Subclients

Import path: `client.manage.v1.projects.billing`

- `balances.list(project_id, ...)`
- `balances.get(project_id, balance_id, ...)`
- `breakdown.list(project_id, ...)`
- `fields.list(project_id, ...)`
- `purchases.list(project_id, ...)`

## Example

```python
client = DeepgramClient()
project_id = "PROJECT_ID"

projects = client.manage.v1.projects.list()
keys = client.manage.v1.projects.keys.list(project_id=project_id status="active")
usage = client.manage.v1.projects.usage.get(
    project_id=project_id,
    start="2026-04-01",
    end="2026-04-30",
    model="nova-3",
)
```

## Related Modules

- `/docs/api-reference/voice-agent-self-hosted`
- `/docs/guides/management-and-automation`
