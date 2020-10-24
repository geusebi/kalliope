from datetime import datetime, tzinfo, timedelta
from random import choices, seed as _seed
from hashlib import sha256
from base64 import b64encode


__all__ = ("KAuth", )


class KAuth(object):
    exa = "0123456789abcdef"
    datetime_fmt = "%Y-%m-%dT%H:%M:%S%Z"

    def __init__(self, conn, user, password, domain):
        self.conn = conn
        self.user, self.password, self.domain = user, password, domain 
        
        self._salt = self._created = self._nonce = None
    
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
        if self._nonce is None:
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
            
            response = self.conn.get(path, noauth=True, headers=headers)
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
