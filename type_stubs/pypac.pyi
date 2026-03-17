# Adapted from https://github.com/carsonyl/pypac

from typing import Any

from requests.auth import HTTPProxyAuth

def pac_context_for_url(
    url: str,
    proxy_auth: HTTPProxyAuth | None = None,
    pac: Any | None = None,
) -> Any: ...
