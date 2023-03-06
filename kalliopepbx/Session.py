from .Auth import Auth
from .utils import parse_conn_str
import requests
from copy import deepcopy

# Using requests might solve some problems encountered while using
# urllib2.

# todo: test against a kalliope server
# todo: add meaningful documentation


__all__ = ("Session", "KalliopeAuth", )


class Session(requests.Session):
    _def_headers = {
        "Accept": "application/json"
    }

    def __init__(self, connection_string, headers=None, timeout=None):
        """
        Create a session to communicate with a Kalliope PBX server

        Example usage:

            s = Session("http://192.168.1.1")
            s.login("admin", "pass", "default")
            accounts = s.get("/rest/account").json()
            print(accounts)
        """
        super().__init__()

        self._url = url = parse_conn_str(connection_string)
        self.headers = headers if headers is not None else Session._def_headers
        self.timeout = timeout

        if url.username is not None:
            self.login(url.username, url.password, url.domain)

    def login(self, username, password, domain=None):
        """
        Update login informations for this session

        Parameters:
        `username` -- the username
        `password` -- the password
        `domain` -- the tenant's domain (default: default)

        Kalliope doesn't actually has a login procedure.
        This function will just create and bind an `Auth` object with the
        given credentials and the `salt` value from the server.
        Every subsequent requests from this session will include a proper
        `X-authenticate` header as per authentication procedure.
        """
        url = self._url
        url.username, url.password, url.domain = username, password, domain

        self.auth = None

        try:
            response = self.get(f"/rest/salt/{domain}")
            salt = response.json()["salt"]
        except Exception:
            msg = "Could not retrieve salt value"
            raise ValueError(msg)

        self.auth = KalliopeAuth(username, password, domain, salt)
        return self.auth

    def logout(self):
        """Delete login informations for this session"""
        url = self._url
        url.username = url.password = url.domain = None
        self.auth = None

    def make_url(self, path):
        """
        Create a url from `path`

        Not meant to be used directly.
        """
        if path.startswith("/"):
            path = path[1:]

        url = self._url
        port = f":{url.port}" if url.port else ""

        return f"{url.scheme}://{url.hostname}{port}/{path}"

    def send(self, *args, timeout=None, **kwargs):
        timout = timeout if timeout is None else self.timeout
        
        return super().send(*args, timeout=timeout, **kwargs)

    def prepare_request(self, request):
        """
        Perpare a request.

        `request.url` is preprocessed by `Session.make_url`.

        Return a `PreparedRequest` according to `requests.Session.prepare_request`.
        """
        req = deepcopy(request)
        req.url = self.make_url(request.url)
        
        return super().prepare_request(req)


class KalliopeAuth(Auth, requests.auth.AuthBase):
    def __call__(self, r):
        r.headers.update(self.xauth())
        return r
