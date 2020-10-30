from types import SimpleNamespace as NS
from urllib.parse import urlparse


def parse_conn_str(cs, scheme="http"):
    """
    Parse a connection string into a namespace
    """
    url = NS()

    parts = urlparse(cs.strip(), scheme=scheme)

    url.scheme = parts.scheme
    if url.scheme not in ("http", "https", ):
        raise ValueError(f"Unsupported scheme '{url.scheme}'")

    url.username = (parts.username or "").strip()
    if url.username == "":
        url.username = None

    url.password = (parts.password or "").strip()
    if url.password == "":
        url.password = None

    if (url.username is None) ^ (url.password is None):
        raise ValueError("Incomplete login credentials'")

    url.hostname = parts.hostname
    if url.hostname is None:
        raise ValueError("Missing hostname")

    url.port = parts.port

    url.domain = parts.path.lstrip("/")
    if url.domain == "":
        url.domain = "default"

    return url
