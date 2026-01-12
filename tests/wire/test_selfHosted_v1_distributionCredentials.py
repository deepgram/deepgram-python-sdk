from .conftest import get_client, verify_request_count


def test_selfHosted_v1_distributionCredentials_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "self_hosted.v1.distribution_credentials.list_.0"
    client = get_client(test_id)
    client.self_hosted.v1.distribution_credentials.list(project_id="123456-7890-1234-5678-901234")
    verify_request_count(
        test_id, "GET", "/v1/projects/123456-7890-1234-5678-901234/self-hosted/distribution/credentials", None, 1
    )


def test_selfHosted_v1_distributionCredentials_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "self_hosted.v1.distribution_credentials.create.0"
    client = get_client(test_id)
    client.self_hosted.v1.distribution_credentials.create(project_id="123456-7890-1234-5678-901234", provider="quay")
    verify_request_count(
        test_id,
        "POST",
        "/v1/projects/123456-7890-1234-5678-901234/self-hosted/distribution/credentials",
        {"provider": "quay"},
        1,
    )


def test_selfHosted_v1_distributionCredentials_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "self_hosted.v1.distribution_credentials.get.0"
    client = get_client(test_id)
    client.self_hosted.v1.distribution_credentials.get(
        project_id="123456-7890-1234-5678-901234", distribution_credentials_id="8b36cfd0-472f-4a21-833f-2d6343c3a2f3"
    )
    verify_request_count(
        test_id,
        "GET",
        "/v1/projects/123456-7890-1234-5678-901234/self-hosted/distribution/credentials/8b36cfd0-472f-4a21-833f-2d6343c3a2f3",
        None,
        1,
    )


def test_selfHosted_v1_distributionCredentials_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "self_hosted.v1.distribution_credentials.delete.0"
    client = get_client(test_id)
    client.self_hosted.v1.distribution_credentials.delete(
        project_id="123456-7890-1234-5678-901234", distribution_credentials_id="8b36cfd0-472f-4a21-833f-2d6343c3a2f3"
    )
    verify_request_count(
        test_id,
        "DELETE",
        "/v1/projects/123456-7890-1234-5678-901234/self-hosted/distribution/credentials/8b36cfd0-472f-4a21-833f-2d6343c3a2f3",
        None,
        1,
    )
