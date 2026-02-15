from .conftest import get_client, verify_request_count


def test_manage_v1_projects_keys_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.keys.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.keys.list(project_id="123456-7890-1234-5678-901234", status="active")
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/keys", {"status": "active"}, 1)


def test_manage_v1_projects_keys_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "manage.v1.projects.keys.create.0"
    client = get_client(test_id)
    client.manage.v1.projects.keys.create(
        project_id="project_id",
        request={
            "key": "value",
        },
    )
    verify_request_count(test_id, "POST", "/v1/projects/project_id/keys", None, 1)


def test_manage_v1_projects_keys_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.projects.keys.get.0"
    client = get_client(test_id)
    client.manage.v1.projects.keys.get(project_id="123456-7890-1234-5678-901234", key_id="123456789012345678901234")
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/keys/123456789012345678901234", None, 1
    )


def test_manage_v1_projects_keys_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "manage.v1.projects.keys.delete.0"
    client = get_client(test_id)
    client.manage.v1.projects.keys.delete(project_id="123456-7890-1234-5678-901234", key_id="123456789012345678901234")
    verify_request_count(
        test_id, "DELETE", "/v1/projects/123456-7890-1234-5678-901234/keys/123456789012345678901234", None, 1
    )
