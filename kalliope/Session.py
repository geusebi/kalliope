from .Auth import Auth
from .cs_re import cs_re
import requests


# Using requests might solve some problems encountered while using urllib2.
# That being said I won't use Session objects because as of now I see no
# reason to have a session-aware connection (kalliope pbx is not designed
# this way). Even though there may be some advantages I'll try to avoid
# such objects for now.
# Still, I'll mimic some of the functionality (loosely) and try to use
# the same class names.

# todo: test against a kalliope server
# todo: add meaningful documentation


__all__ = ("Session", )


class Session(object):
    _def_headers = {
        "Accept": "application/json"
    }

    def __init__(self, scheme, address, port=None, timeout=4, headers=None):
        """
        Create a session to communicate with a Kalliope PBX server

        Parameters:
        `scheme` -- either `http` or `https`
        `port` -- the port to connect to
        `timeout` -- timeout for data exchanges (see `requests` module)
        `headers` -- dict of headers to merge on every request

        Example usage:

            s = Session("http", "192.168.1.1")
            s.login("admin", "pass", "default")
            accounts = s.get("/rest/account").json()
            print(accounts)

        Or with a more convenient connection string
        (see `Session.from_cs`):

            s = Session.from_cs("http://admin:pass@192.168.1.1/default")
            accounts = s.get("/rest/account").json()
            print(accounts)
        """
        self.scheme, self.address, self.port = scheme, address, port

        self.timeout = timeout

        if headers is None:
            headers = {}
        self.headers = {**Session._def_headers, **headers}

        self.auth = None

    @staticmethod
    def from_connection_string(conn_str, *args, **kwargs):
        """
        Create a session from a proper connection string

        Aliases:    Session.from_cs, Session.from_conn_str,
                    Session.from_connection_string.

        The connection string (`conn_str`) is of the form:

            scheme://user:pass@host:port/domain

        Extra arguments (`args` and `kwargs`) are passed as-is to
        `Session.__init__`.

        Where:

            - `scheme` is either `http` or `https`,
            - `user` and `pass`, if given, must be both present,
            - `host` is a valid ip address, hostname or fqdn,
            - `port` if present is the port to connect to,
            - `domain` if present is the tenant's domain (default: `default`).

        E.g.:

            Session.from_cs("http://admin:secret@server1.local")
            Session.from_cs("https://server1.local/some_other_domain")
            Session.from_cs("http://server1.local:8080")
        """
        match = cs_re.match(conn_str)
        if not match:
            raise ValueError(f"Invalid connection string {conn_str!r}")

        parts = match.groupdict()
        conn = Session(
            parts["scheme"], parts["host"], parts["port"], *args, **kwargs
        )

        if parts["username"] is not None and parts["password"] is not None:
            conn.login(parts["username"], parts["password"], parts["domain"])

        return conn

    from_cs = from_conn_str = from_connection_string

    def login(self, username, password, domain="default"):
        """
        Update login informations for this session

        Parameters:
        `username` -- the username
        `password` -- the password
        `domain` -- the tenant's domain (default: default)

        Kalliope doesn't actually has a login procedure.
        This function will just create and bind an `Auth` object with the
        given credentials.
        Every subsequent requests from this session will include a proper
        `X-authenticate` header as authentication.

        This method support call-chaining.
        """
        self.auth = Auth(self, username, password, domain)
        return self

    def logout(self):
        """Delete login informations for this session"""
        self.auth = None
        return self

    def prepare_url(self, path):
        """
        Create a url from `path`

        Not meant to be used directly.
        """
        if path.startswith("/"):
            path = path[1:]

        port = f":{self.port}" if self.port else ""

        return f"{self.scheme}://{self.address}{port}/{path}"

    def prepare_headers(self, noauth=False, headers=None):
        """
        Create a `dict` of headers based for a request

        Not meant to be used directly.

        Parameters:
        `noauth` -- whether to omit authentication
        `headers` -- additional headers to merge into the request

        The resulting `dict` is the combination of session's default
        headers and the given `headers`.
        If `noauth` is `False` then the `X-authenticate` header is added.

        Raises `ValueError` if login is required but login credentials
        are not available.
        """
        if headers is None:
            headers = {}

        if noauth is False:
            if self.auth is None:
                raise ValueError("Not logged in")
            xheaders = self.auth.xauth()
        else:
            xheaders = {}

        return {**self.headers, **xheaders, **headers}

    def request(
        self, method, path, noauth=False, headers=None, *args, **kwargs
    ):
        """
        Perform a request via `requests.request`

        The `path` is preprocessed by `Session.prepare_url`.
        `headers` are processed by `Session.prepare_headers`.
        `args` and `kwargs` are passed as-is to `requests.request`.

        Return a `Response` object upon success.
        """
        url = self.prepare_url(path)
        headers = self.prepare_headers(noauth, headers)
        return requests.request(method, url, headers=headers, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Perform a `GET` request

        See `Session.request` and `requests.request` for documentation and
        details.
        """
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)
    post.__doc__ = get.__doc__.replace("GET", "POST", 1)  # Lazy

    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
    put.__doc__ = get.__doc__.replace("GET", "PUT", 1)  # Quite lazy

    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)
    delete.__doc__ = get.__doc__.replace("GET", "DELETE", 1)  # Very quite lazy
