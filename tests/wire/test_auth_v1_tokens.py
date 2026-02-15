from .conftest import get_client, verify_request_count


def test_auth_v1_tokens_grant() -> None:
    """Test grant endpoint with WireMock"""
    test_id = "auth.v1.tokens.grant.0"
    client = get_client(test_id)
    client.auth.v1.tokens.grant()
    verify_request_count(test_id, "POST", "/v1/auth/grant", None, 1)
