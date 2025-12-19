from .conftest import get_client, verify_request_count


def test_manage_v1_projects_usage_fields_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.usage.fields.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.usage.fields.list(project_id="123456-7890-1234-5678-901234", start="start", end="end")
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/usage/fields", {"start": "start", "end": "end"}, 1
    )
