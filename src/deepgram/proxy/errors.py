"""Exception classes for the Deepgram proxy."""


class ProxyError(Exception):
    """Base exception for proxy errors."""

    def __init__(self, message: str, status_code: int = 500, detail: str = ""):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class AuthenticationError(ProxyError):
    """Raised when JWT is missing, invalid, or expired."""

    def __init__(self, message: str = "Authentication required", detail: str = ""):
        super().__init__(message=message, status_code=401, detail=detail)


class AuthorizationError(ProxyError):
    """Raised when the token's scopes don't permit the requested path."""

    def __init__(self, message: str = "Insufficient scope", detail: str = ""):
        super().__init__(message=message, status_code=403, detail=detail)


class UpstreamError(ProxyError):
    """Raised when Deepgram returns an error or is unreachable."""

    def __init__(self, message: str = "Upstream error", status_code: int = 502, detail: str = ""):
        super().__init__(message=message, status_code=status_code, detail=detail)
