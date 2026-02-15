from .conftest import get_client, verify_request_count


def test_manage_v1_projects_billing_purchases_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.billing.purchases.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.billing.purchases.list(project_id="123456-7890-1234-5678-901234", limit=1.1)
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/purchases", {"limit": "1.1"}, 1)
