from .conftest import get_client, verify_request_count


def test_manage_v1_projects_members_invites_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.members.invites.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.members.invites.list(project_id="123456-7890-1234-5678-901234")
    verify_request_count(test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/invites", None, 1)


def test_manage_v1_projects_members_invites_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "manage.v1.projects.members.invites.create.0"
    client = get_client(test_id)
    client.manage.v1.projects.members.invites.create(
        project_id="123456-7890-1234-5678-901234", email="email", scope="scope"
    )
    verify_request_count(test_id, "POST", "/v1/projects/123456-7890-1234-5678-901234/invites", None, 1)


def test_manage_v1_projects_members_invites_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "manage.v1.projects.members.invites.delete.0"
    client = get_client(test_id)
    client.manage.v1.projects.members.invites.delete(
        project_id="123456-7890-1234-5678-901234", email="john.doe@example.com"
    )
    verify_request_count(
        test_id, "DELETE", "/v1/projects/123456-7890-1234-5678-901234/invites/john.doe@example.com", None, 1
    )
