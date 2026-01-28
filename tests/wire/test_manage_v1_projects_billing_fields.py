from .conftest import get_client, verify_request_count


def test_manage_v1_projects_billing_fields_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.billing.fields.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.billing.fields.list(project_id="123456-7890-1234-5678-901234", start="start", end="end")
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/billing/fields", {"start": "start", "end": "end"}, 1
    )
