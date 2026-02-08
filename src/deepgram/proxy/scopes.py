"""Scope definitions and path matching for the Deepgram proxy."""

import re
from enum import Enum
from typing import List, Optional


class Scope(str, Enum):
    """Scopes that can be granted to proxy JWT tokens."""

    LISTEN = "listen"
    SPEAK = "speak"
    READ = "read"
    AGENT = "agent"
    MANAGE = "manage"
    SELF_HOSTED = "self_hosted"


# Maps each scope to regex patterns that match permitted API paths.
# Patterns use v\d+ to be version-agnostic.
SCOPE_PATH_PATTERNS: dict = {
    Scope.LISTEN: [
        re.compile(r"^/v\d+/listen"),
    ],
    Scope.SPEAK: [
        re.compile(r"^/v\d+/speak"),
    ],
    Scope.READ: [
        re.compile(r"^/v\d+/read"),
    ],
    Scope.AGENT: [
        re.compile(r"^/v\d+/agent"),
    ],
    Scope.MANAGE: [
        re.compile(r"^/v\d+/projects"),
        re.compile(r"^/v\d+/keys"),
        re.compile(r"^/v\d+/members"),
        re.compile(r"^/v\d+/scopes"),
        re.compile(r"^/v\d+/invitations"),
        re.compile(r"^/v\d+/usage"),
        re.compile(r"^/v\d+/billing"),
        re.compile(r"^/v\d+/balances"),
        re.compile(r"^/v\d+/models"),
    ],
    Scope.SELF_HOSTED: [
        re.compile(r"^/v\d+/onprem"),
        re.compile(r"^/v\d+/selfhosted"),
    ],
}

# Paths routed to agent.deepgram.com instead of api.deepgram.com
_AGENT_PATH_PATTERN = re.compile(r"^/v\d+/agent")


def path_matches_scope(path: str, scope: Scope) -> bool:
    """Check if a request path is permitted by a single scope."""
    patterns = SCOPE_PATH_PATTERNS.get(scope, [])
    return any(p.search(path) for p in patterns)


def path_matches_any_scope(path: str, scopes: List[Scope]) -> bool:
    """Check if a request path is permitted by any of the given scopes."""
    return any(path_matches_scope(path, s) for s in scopes)


def get_target_base_url(path: str, production_url: Optional[str] = None, agent_url: Optional[str] = None) -> str:
    """Return the upstream Deepgram base URL for a given path.

    Agent paths route to agent.deepgram.com; everything else to api.deepgram.com.
    """
    if _AGENT_PATH_PATTERN.search(path):
        return agent_url or "https://agent.deepgram.com"
    return production_url or "https://api.deepgram.com"
