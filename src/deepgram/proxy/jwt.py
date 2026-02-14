"""JWT creation and validation for the Deepgram proxy.

Uses HMAC-SHA256 with the Deepgram API key as the signing secret.
Requires PyJWT (``pip install PyJWT``).
"""

import time
import uuid
from typing import List, NamedTuple, Optional

try:
    import jwt as pyjwt
except ImportError:
    raise ImportError(
        "PyJWT is required for proxy JWT support. "
        "Install it with: pip install 'deepgram-sdk[proxy]' or pip install PyJWT"
    )

from .scopes import Scope


class TokenPayload(NamedTuple):
    """Decoded JWT payload."""

    scopes: List[str]
    exp: int
    iat: int
    jti: str


class JWTManager:
    """Creates and validates HMAC-SHA256 JWTs signed with the Deepgram API key."""

    def __init__(self, api_key: str):
        self._secret = api_key

    def create_token(self, scopes: List[Scope], expires_in: int = 3600) -> str:
        """Create a signed JWT with the given scopes.

        Args:
            scopes: List of Scope values the token is permitted to use.
            expires_in: Token lifetime in seconds (default 3600).

        Returns:
            Encoded JWT string.
        """
        now = int(time.time())
        payload = {
            "scopes": [s.value if isinstance(s, Scope) else s for s in scopes],
            "iat": now,
            "exp": now + expires_in,
            "jti": str(uuid.uuid4()),
        }
        return pyjwt.encode(payload, self._secret, algorithm="HS256")

    def validate_token(self, token: str) -> TokenPayload:
        """Validate a JWT and return its payload.

        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is malformed or signature is invalid.
        """
        data = pyjwt.decode(token, self._secret, algorithms=["HS256"])
        return TokenPayload(
            scopes=data.get("scopes", []),
            exp=data["exp"],
            iat=data["iat"],
            jti=data["jti"],
        )

    @staticmethod
    def extract_token_from_header(authorization: Optional[str]) -> Optional[str]:
        """Extract a bearer token from an Authorization header value.

        Args:
            authorization: The full header value, e.g. ``"Bearer <token>"``.

        Returns:
            The token string, or None if the header is missing/malformed.
        """
        if not authorization:
            return None
        parts = authorization.split(None, 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
        return None
