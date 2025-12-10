from .conftest import get_client, verify_request_count


def test_manage_v1_models_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "manage.v1.models.list_.0"
    client = get_client(test_id)
    client.manage.v1.models.list(include_outdated=True)
    verify_request_count(test_id, "GET", "/v1/models", {"include_outdated": "true"}, 1)


def test_manage_v1_models_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "manage.v1.models.get.0"
    client = get_client(test_id)
    client.manage.v1.models.get(model_id="af6e9977-99f6-4d8f-b6f5-dfdf6fb6e291")
    verify_request_count(test_id, "GET", "/v1/models/af6e9977-99f6-4d8f-b6f5-dfdf6fb6e291", None, 1)
