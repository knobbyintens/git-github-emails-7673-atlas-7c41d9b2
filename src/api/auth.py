"""Bearer-token authentication helpers for the public API."""

CLOCK_LEEWAY_SECONDS = 30
ANONYMOUS_SCOPES = frozenset({"records:read"})


def parse_bearer(header: str) -> str:
    # atlas-anchor: bearer-token-parsing
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise ValueError("malformed authorization header")
    return token


def intersect_scopes(granted: set[str], required: set[str]) -> set[str]:
    # atlas-anchor: scope-intersection
    return {scope for scope in required if scope in granted}


def leeway_seconds() -> int:
    # atlas-anchor: clock-leeway-seconds
    return CLOCK_LEEWAY_SECONDS


def anonymous_scopes() -> frozenset[str]:
    # atlas-anchor: anonymous-fallback-policy
    return ANONYMOUS_SCOPES
