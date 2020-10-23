from datetime import datetime, tzinfo, timedelta
from random import choices, seed as _seed

from socket import timeout as Timeout

# Workaround for IncompleteRead errors
import http.client as http
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from json import loads as json_parse

from hashlib import sha256
from base64 import b64encode


class KAuth(object):
    exa = "0123456789abcdef"
    datetime_fmt = "%Y-%m-%dT%H:%M:%S%Z"

    def __init__(self,
        scheme, ip, user, password, domain="default",
        nonce=None, created=None, salt=None
    ):
        self.scheme, self.ip = scheme, ip
        self.user, self.password = user, password
        self.domain, self.salt = domain, salt
        self.created, self.nonce, self._last_nonce = created, nonce, None
    
    def xauth(self, reset=True):
        value = (
            f'RestApiUsernameToken '
            f'Username="{self.user}", Domain="{self.domain}", '
            f'Digest="{self.digest}", '
            f'Nonce="{self.nonce}", Created="{self.created}"'
        )

        if reset:
            self.nonce = None
            self.created = None
        
        return {"X-authenticate": value}

    @property
    def digest(self):
        data = (
            self.nonce + self.digest_pass +
            self.user + self.domain + self.created
        )
        message = sha256(bytearray(data, "utf-8"))
        return b64encode(message.digest()).decode("utf-8")

    @property
    def digest_pass(self):
        data = f"{self.password}{{{self.salt}}}"
        message = bytearray(data, "utf-8")
        return sha256(message).hexdigest()

    @property
    def address(self):
        return f"{self.scheme}://{self.ip}"
    
    def now(self, delta={}):
        dt = datetime.now(Zulu()) + timedelta(**delta)
        return dt.strftime(XAuthGenerator.datetime_fmt)

    @property
    def nonce(self):
        if self._nonce in (self._last_nonce, None):
            self._nonce = "".join(choices(XAuthGenerator.exa, k=32))

        return self._nonce
    
    @nonce.setter
    def nonce(self, value):
        self._nonce = value

    @property
    def created(self):
        if self._created == None:
            self._created = self.now()
        
        return self._created
    
    @created.setter
    def created(self, value):
        self._created = value

    @property
    def salt(self):
        if self._salt is None:
            data = get(f"{self.address}/rest/salt/{self.domain}")
            self.salt = data["salt"]
        
        return self._salt

    @salt.setter
    def salt(self, value):
        self._salt = value

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"scheme={self.scheme!r}, "
            f"ip={self.ip!r}, "
            f"user={self.user!r}, "
            f"password={self.password!r}, "
            f"domain={self.domain!r}, "
            f"salt={self.salt!r}, "
            f"created={self.created!r}, "
            f"nonce={self.nonce!r}"
            f")"
        )
    
    def __str__(self):
        header = self.xauth(False)
        key = "X-authenticate"
        return f"{key}: {header[key]}"


class Zulu(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)
    
    def dst(self, dt):
        return timedelta(0)
    
    def tzname(self, dt):
        return "Z"


_def_headers = {"Accept": "application/json"}

def get(url, headers=_def_headers, timeout=4):
    headers = {**_def_headers, **headers}

    try:
        req = Request(url, headers=headers)
        response = urlopen(req, timeout=timeout)

        try:
            data = response.read().decode('utf-8')
        except http.client.IncompleteRead as frag:
            data = frag.partial.decode('utf-8')

        return json_parse(data)
    
    except (URLError, HTTPError, Timeout):
        raise


class KRequest(object):
    DATATYPES = ("json", "str", )

    def __init__(self, auth, datatype="json"):
        self.def_headers = {}

        self.datatype = datatype.lower()
        if self.datatype not in KConnection.DATATYPES:
            raise ValueError(f"Invalid datatype '{datatype}'")
        
        if self.datatype == "json":
            self.def_headers = {"accept": "application/json"}

    def get(self, *args, **kwargs):
        if self.datatype == "json":
            return self.get_json(*args, **kwargs)
        return self.get_str(*args, **kwargs)

    def get_json(self, *args, **kwargs):
        return json_parse(self.get_str(*args, **kwargs))
        
    def get_str(self, url, headers={}, timeout=4):
        headers = {**self.def_headers, **headers}

        try:
            req = Request(url, headers=headers)
            response = urlopen(req, timeout=timeout)

            try:
                data = response.read().decode('utf-8')
            except http.client.IncompleteRead as frag:
                data = frag.partial.decode('utf-8')

            return data
        
        except (URLError, HTTPError, Timeout):
            raise

    
    def _unimplemented(self, *args, **kwargs):
        raise NotImplemented

    post_str = KConnection._unimplemented
    post_json = KConnection._unimplemented
    post = post_json

    delete_str = KConnection._unimplemented
    delete_json = KConnection._unimplemented
    delete = delete_json

    put_str = KConnection._unimplemented
    put_json = KConnection._unimplemented
    put = delete_json
