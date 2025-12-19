from .conftest import get_client, verify_request_count


def test_agent_v1_settings_think_models_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "agent.v1.settings.think.models.list_.0"
    client = get_client(test_id)
    client.agent.v1.settings.think.models.list()
    verify_request_count(test_id, "GET", "/v1/agent/settings/think/models", None, 1)
