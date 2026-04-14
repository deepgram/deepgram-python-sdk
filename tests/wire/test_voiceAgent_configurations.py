from .conftest import get_client, verify_request_count


def test_voiceAgent_configurations_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "voice_agent.configurations.list_.0"
    client = get_client(test_id)
    client.voice_agent.configurations.list(
        project_id="123456-7890-1234-5678-901234",
    )
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/agents", None, 1)


def test_voiceAgent_configurations_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "voice_agent.configurations.create.0"
    client = get_client(test_id)
    client.voice_agent.configurations.create(
        project_id="123456-7890-1234-5678-901234",
        config="config",
    )
    verify_request_count(test_id, "POST", "/v1/projects/123456-7890-1234-5678-901234/agents", None, 1)


def test_voiceAgent_configurations_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "voice_agent.configurations.get.0"
    client = get_client(test_id)
    client.voice_agent.configurations.get(
        project_id="123456-7890-1234-5678-901234",
        agent_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    )
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890", None, 1
    )


def test_voiceAgent_configurations_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "voice_agent.configurations.update.0"
    client = get_client(test_id)
    client.voice_agent.configurations.update(
        project_id="123456-7890-1234-5678-901234",
        agent_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        metadata={"key": "value"},
    )
    verify_request_count(
        test_id, "PUT", "/v1/projects/123456-7890-1234-5678-901234/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890", None, 1
    )


def test_voiceAgent_configurations_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "voice_agent.configurations.delete.0"
    client = get_client(test_id)
    client.voice_agent.configurations.delete(
        project_id="123456-7890-1234-5678-901234",
        agent_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    )
    verify_request_count(
        test_id,
        "DELETE",
        "/v1/projects/123456-7890-1234-5678-901234/agents/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        None,
        1,
    )
