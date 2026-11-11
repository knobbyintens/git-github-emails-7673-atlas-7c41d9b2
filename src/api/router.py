"""Route table for the Service Atlas HTTP surface."""

from typing import Callable

Handler = Callable[[dict], dict]

ROUTES = {
    "/v1/records": "records",
    "/v1/records/{record_id}": "record_detail",
}


def resolve(path: str, routes: dict[str, str]) -> str:
    # atlas-anchor: route-table-precedence
    for pattern, handler in routes.items():
        if path.startswith(pattern.split("{")[0]):
            return handler
    raise KeyError(path)


def normalize_path(path: str) -> str:
    # atlas-anchor: path-trailing-slash
    if path != "/" and path.endswith("/"):
        return path.rstrip("/")
    return path


def fallback_method(method: str) -> str:
    # atlas-anchor: method-not-allowed-fallback
    return method if method in {"GET", "POST", "PUT", "DELETE"} else "GET"
