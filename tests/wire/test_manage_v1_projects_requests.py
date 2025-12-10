from datetime import datetime

from .conftest import get_client, verify_request_count


def test_manage_v1_projects_requests_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.projects.requests.list_.0"
    client = get_client(test_id)
    client.manage.v1.projects.requests.list(
        project_id="123456-7890-1234-5678-901234",
        start=datetime.fromisoformat("2024-01-15T09:30:00Z"),
        end=datetime.fromisoformat("2024-01-15T09:30:00Z"),
        limit=1.1,
        page=1.1,
        accessor="12345678-1234-1234-1234-123456789012",
        request_id="12345678-1234-1234-1234-123456789012",
        deployment="hosted",
        endpoint="listen",
        method="sync",
        status="succeeded",
    )
    verify_request_count(
        test_id,
        "GET",
        "/v1/projects/123456-7890-1234-5678-901234/requests",
        {
            "start": "2024-01-15T09:30:00Z",
            "end": "2024-01-15T09:30:00Z",
            "limit": "1.1",
            "page": "1.1",
            "accessor": "12345678-1234-1234-1234-123456789012",
            "request_id": "12345678-1234-1234-1234-123456789012",
            "deployment": "hosted",
            "endpoint": "listen",
            "method": "sync",
            "status": "succeeded",
        },
        1,
    )


def test_manage_v1_projects_requests_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.projects.requests.get.0"
    client = get_client(test_id)
    client.manage.v1.projects.requests.get(
        project_id="123456-7890-1234-5678-901234", request_id="123456-7890-1234-5678-901234"
    )
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/requests/123456-7890-1234-5678-901234", None, 1
    )
