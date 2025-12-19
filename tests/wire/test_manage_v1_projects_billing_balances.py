from .conftest import get_client, verify_request_count


def test_manage_v1_projects_billing_balances_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.billing.balances.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.billing.balances.list(project_id="123456-7890-1234-5678-901234")
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/balances", None, 1)


def test_manage_v1_projects_billing_balances_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.projects.billing.balances.get.0"
    client = get_client(test_id)
    client.manage.v1.projects.billing.balances.get(
        project_id="123456-7890-1234-5678-901234", balance_id="123456-7890-1234-5678-901234"
    )
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/balances/123456-7890-1234-5678-901234", None, 1
    )
