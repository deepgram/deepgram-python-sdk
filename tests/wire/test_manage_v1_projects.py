from .conftest import get_client, verify_request_count


def test_manage_v1_projects_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.list()
    verify_request_count(test_id, "GET", "/v1/projects", None, 1)


def test_manage_v1_projects_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.projects.get.0"
    client = get_client(test_id)
    client.manage.v1.projects.get(project_id="123456-7890-1234-5678-901234", limit=1.1, page=1.1)
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234", {"limit": "1.1", "page": "1.1"}, 1
    )


def test_manage_v1_projects_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "manage.v1.projects.delete.0"
    client = get_client(test_id)
    client.manage.v1.projects.delete(project_id="123456-7890-1234-5678-901234")
    verify_request_count(test_id, "DELETE", "/v1/projects/123456-7890-1234-5678-901234", None, 1)


def test_manage_v1_projects_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "manage.v1.projects.update.0"
    client = get_client(test_id)
    client.manage.v1.projects.update(project_id="123456-7890-1234-5678-901234")
    verify_request_count(test_id, "PATCH", "/v1/projects/123456-7890-1234-5678-901234", None, 1)


def test_manage_v1_projects_leave() -> None:
    """Test leave endpoint with WireMock"""
    test_id = "manage.v1.projects.leave.0"
    client = get_client(test_id)
    client.manage.v1.projects.leave(project_id="123456-7890-1234-5678-901234")
    verify_request_count(test_id, "DELETE", "/v1/projects/123456-7890-1234-5678-901234/leave", None, 1)
