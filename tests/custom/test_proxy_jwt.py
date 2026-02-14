"""Tests for proxy JWT creation and validation."""


import jwt as pyjwt
import pytest

from deepgram.proxy.jwt import JWTManager, TokenPayload
from deepgram.proxy.scopes import Scope

API_KEY = "test-api-key-for-jwt"


@pytest.fixture
def manager():
    return JWTManager(API_KEY)


class TestCreateToken:
    def test_returns_string(self, manager):
        token = manager.create_token([Scope.LISTEN])
        assert isinstance(token, str)

    def test_contains_scopes(self, manager):
        token = manager.create_token([Scope.LISTEN, Scope.SPEAK])
        payload = pyjwt.decode(token, API_KEY, algorithms=["HS256"])
        assert payload["scopes"] == ["listen", "speak"]

    def test_contains_exp(self, manager):
        token = manager.create_token([Scope.LISTEN], expires_in=600)
        payload = pyjwt.decode(token, API_KEY, algorithms=["HS256"])
        assert payload["exp"] - payload["iat"] == 600

    def test_contains_jti(self, manager):
        token = manager.create_token([Scope.LISTEN])
        payload = pyjwt.decode(token, API_KEY, algorithms=["HS256"])
        assert "jti" in payload
        assert len(payload["jti"]) > 0

    def test_unique_jti(self, manager):
        t1 = manager.create_token([Scope.LISTEN])
        t2 = manager.create_token([Scope.LISTEN])
        p1 = pyjwt.decode(t1, API_KEY, algorithms=["HS256"])
        p2 = pyjwt.decode(t2, API_KEY, algorithms=["HS256"])
        assert p1["jti"] != p2["jti"]


class TestValidateToken:
    def test_valid_token(self, manager):
        token = manager.create_token([Scope.LISTEN])
        payload = manager.validate_token(token)
        assert isinstance(payload, TokenPayload)
        assert payload.scopes == ["listen"]

    def test_expired_token(self, manager):
        token = manager.create_token([Scope.LISTEN], expires_in=-1)
        with pytest.raises(pyjwt.ExpiredSignatureError):
            manager.validate_token(token)

    def test_bad_signature(self, manager):
        other = JWTManager("wrong-key")
        token = other.create_token([Scope.LISTEN])
        with pytest.raises(pyjwt.InvalidSignatureError):
            manager.validate_token(token)

    def test_malformed_token(self, manager):
        with pytest.raises(pyjwt.DecodeError):
            manager.validate_token("not.a.valid.jwt")

    def test_multiple_scopes(self, manager):
        token = manager.create_token([Scope.LISTEN, Scope.SPEAK, Scope.AGENT])
        payload = manager.validate_token(token)
        assert payload.scopes == ["listen", "speak", "agent"]


class TestExtractTokenFromHeader:
    def test_bearer_token(self):
        assert JWTManager.extract_token_from_header("Bearer abc123") == "abc123"

    def test_bearer_lowercase(self):
        assert JWTManager.extract_token_from_header("bearer abc123") == "abc123"

    def test_no_header(self):
        assert JWTManager.extract_token_from_header(None) is None

    def test_empty_header(self):
        assert JWTManager.extract_token_from_header("") is None

    def test_wrong_scheme(self):
        assert JWTManager.extract_token_from_header("Token abc123") is None

    def test_no_space(self):
        assert JWTManager.extract_token_from_header("Bearerabc123") is None
