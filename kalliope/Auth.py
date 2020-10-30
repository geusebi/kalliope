from datetime import datetime, tzinfo, timedelta
from random import choices
from hashlib import sha256
from base64 import b64encode

# LGPLv3 -- License notice at the bottom

__all__ = ("Auth", )


class Auth(object):
    exa = "0123456789abcdef"
    datetime_fmt = "%Y-%m-%dT%H:%M:%S%Z"

    def __init__(self, user, password, domain, salt=None):
        self.user, self.password = user, password
        self.domain = domain
        self._salt = salt
        self._created = self._nonce = None

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
        return dt.strftime(Auth.datetime_fmt)

    @property
    def nonce(self):
        if self._nonce is None:
            self._nonce = "".join(choices(Auth.exa, k=32))

        return self._nonce

    @property
    def created(self):
        if self._created is None:
            self._created = self.now()

        return self._created

    @property
    def salt(self):
        if self._salt is None:
            raise ValueError("Missing salt value")
        return self._salt

    @salt.setter
    def salt(self, value):
        self._salt = value

    def __str__(self):
        header = self.xauth(False)
        key = "X-authenticate"
        return f"{key}: {header[key]}"


class Zulu(tzinfo):
    """
    Dummy timezone class with name "Z" and null delta over UTC

    Todo: check if this is correct.
    """
    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "Z"


# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
