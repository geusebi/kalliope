from datetime import datetime, tzinfo, timedelta
from random import choices, seed as _seed
from hashlib import sha256
from base64 import b64encode
import requests


# Using requests might solve some problems encountered while sing urllib2.
# That being said I won't use Session objects because as of now I see no
# reason to have a session-aware connection (kalliope pbx is not designed
# this way). Even though there may be some advantages I'll try to avoid
# such objects for now.
# Still, I'll mimic some of the functionality (loosely) and try to use 
# the same class names.

# Absolutely not tested. 

# Exempli gratia
# sess = KSession("http", "10.0.0.1")
# sess.login("user", "pass")
#
# accounts = sess.get("/rest/account").json()

# todo: split in multiple files and test against a kalliope server
# todo: add unit tests
# todo: add meaningful documentation


class KSession(object):
    _def_headers = {
        "Accept": "application/json"
    }
    
    def __init__(self,
        scheme, address,
        timeout=4, headers=None
    ):
        self.scheme, self.address = scheme, address
        
        self.timeout = timeout
        
        if headers is None:
            headers = {}
        self.headers = {**KSession._def_headers, **headers}
        
        self.auth = None
    
    def login(self, username, password, domain="default"):
        self.auth = Kauth(username, password, domain)
        return self
    
    def logout(self):
        self.auth = None
        return self
    
    def prepare_url(self, path):
        if path.startswith("/"):
            path = path[1:]
        return f"{self.scheme}://{self.address}/{path}"
    
    def prepare_headers(self, noauth=False, headers=None):
        if headers is None
            headers = {}
        
        if noauth is False:
            if self.auth is None:
                raise Exception("Not logged in")
            xheaders = self.auth.xauth()
        else:
            xheaders = {}
        
        return {**self.headers, **xheaders, **headers}
    
    def request(self, method, path, noauth=False, headers=None, *args, **kwargs):
        url = self.prepare_url(path)
        headers = prepare_headers(xauth, headers)
        return requests.request(method, url, headers=headers, *args, **kwargs)
    
    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)
    
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)


class KAuth(object):
    exa = "0123456789abcdef"
    datetime_fmt = "%Y-%m-%dT%H:%M:%S%Z"

    def __init__(self, conn, user, password, domain):
        self.conn = conn
        self.user, self.password, self.domain = user, password, domain 
        
        self._salt = self._created = self._nonce = self._last_nonce = None
    
    def xauth(self, reset=True):
        value = (
            f'RestApiUsernameToken '
            f'Username="{self.user}", Domain="{self.domain}", '
            f'Digest="{self.digest}", '
            f'Nonce="{self.nonce}", Created="{self.created}"'
        )

        if reset:
            self._nonce = None
            self._created = None
        
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
    
    def now(self, delta={}):
        dt = datetime.now(Zulu()) + timedelta(**delta)
        return dt.strftime(KAuth.datetime_fmt)

    @property
    def nonce(self):
        if self._nonce in (self._last_nonce, None):
            self._nonce = "".join(choices(KAuth.exa, k=32))

        return self._nonce

    @property
    def created(self):
        if self._created == None:
            self._created = self.now()
        
        return self._created

    @property
    def salt(self):
        if self._salt is None:
            if conn is None:
                raise ValueError("No connection to get the 'salt' value")
            path = f"/rest/salt/{self.domain}"
            headers={"Accept": "application/json"}
            
            response = self.conn.get(path, noauth=True, headers)
            data = response.json()
            self._salt = data["salt"]
        
        return self._salt

    @salt.setter
    def salt(self, value):
        self._salt = value
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"conn={self.conn!r}, "
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
