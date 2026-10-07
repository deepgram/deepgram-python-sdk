from .conftest import get_client, verify_request_count


def test_manage_v1_projects_requests_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.requests.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.requests.list(
        project_id="12345678-90ab-cdef-1234-567890abcdef",
    )
    verify_request_count(test_id, "GET", "/v1/projects/12345678-90ab-cdef-1234-567890abcdef/requests", None, 1)


def test_manage_v1_projects_requests_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.projects.requests.get.0"
    client = get_client(test_id)
    client.manage.v1.projects.requests.get(
        project_id="12345678-90ab-cdef-1234-567890abcdef",
        request_id="a3f1c9d2-4b7e-4f9a-8c3d-2e5f7b9a1c0d",
    )
    verify_request_count(
        test_id,
        "GET",
        "/v1/projects/12345678-90ab-cdef-1234-567890abcdef/requests/a3f1c9d2-4b7e-4f9a-8c3d-2e5f7b9a1c0d",
        None,
        1,
    )
