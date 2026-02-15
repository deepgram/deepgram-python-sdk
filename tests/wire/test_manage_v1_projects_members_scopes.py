from .conftest import get_client, verify_request_count


def test_manage_v1_projects_members_scopes_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.members.scopes.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.members.scopes.list(
        project_id="123456-7890-1234-5678-901234", member_id="123456789012345678901234"
    )
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/members/123456789012345678901234/scopes", None, 1
    )


def test_manage_v1_projects_members_scopes_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "manage.v1.projects.members.scopes.update.0"
    client = get_client(test_id)
    client.manage.v1.projects.members.scopes.update(
        project_id="123456-7890-1234-5678-901234", member_id="123456789012345678901234", scope="admin"
    )
    verify_request_count(
        test_id, "PUT", "/v1/projects/123456-7890-1234-5678-901234/members/123456789012345678901234/scopes", None, 1
    )
