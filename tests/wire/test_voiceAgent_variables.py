from .conftest import get_client, verify_request_count


def test_voiceAgent_variables_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "voice_agent.variables.list_.0"
    client = get_client(test_id)
    client.voice_agent.variables.list(
        project_id="123456-7890-1234-5678-901234",
    )
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/agent-variables", None, 1)


def test_voiceAgent_variables_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "voice_agent.variables.create.0"
    client = get_client(test_id)
    client.voice_agent.variables.create(
        project_id="project_id",
        key="key",
        value={"key": "value"},
    )
    verify_request_count(test_id, "POST", "/v1/projects/project_id/agent-variables", None, 1)


def test_voiceAgent_variables_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "voice_agent.variables.get.0"
    client = get_client(test_id)
    client.voice_agent.variables.get(
        project_id="123456-7890-1234-5678-901234",
        variable_id="v1a2b3c4-d5e6-7890-abcd-ef1234567890",
    )
    verify_request_count(
        test_id,
        "GET",
        "/v1/projects/123456-7890-1234-5678-901234/agent-variables/v1a2b3c4-d5e6-7890-abcd-ef1234567890",
        None,
        1,
    )


def test_voiceAgent_variables_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "voice_agent.variables.delete.0"
    client = get_client(test_id)
    client.voice_agent.variables.delete(
        project_id="123456-7890-1234-5678-901234",
        variable_id="v1a2b3c4-d5e6-7890-abcd-ef1234567890",
    )
    verify_request_count(
        test_id,
        "DELETE",
        "/v1/projects/123456-7890-1234-5678-901234/agent-variables/v1a2b3c4-d5e6-7890-abcd-ef1234567890",
        None,
        1,
    )


def test_voiceAgent_variables_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "voice_agent.variables.update.0"
    client = get_client(test_id)
    client.voice_agent.variables.update(
        project_id="project_id",
        variable_id="variable_id",
        value={"key": "value"},
    )
    verify_request_count(test_id, "PATCH", "/v1/projects/project_id/agent-variables/variable_id", None, 1)
