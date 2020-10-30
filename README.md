# Python KalliopePBX authentication module

Communication module for Kalliope PBX servers  
(see [Kalliope PBX](<www.kalliopepbx.com/>) for more informations).

## IMPORTANT

**Experimental**  
**Tested only locally and not against a proper Kalliope server**  
**Not an official project of Kalliope or Netresult S.r.l.**

## Install

To install from [Pypi](www.pypi.org/) using `pip`:
```sh
pip install kalliope
```

Or to install directly from git sources:
```bash
git clone https://gitlab.com/geusebi/kalliope.git
cd kalliope
python setup.py install --user
```

To install `kalliope` system-wide, remove `--user` from the last line
and use `sudo` or other subsystems to run the command as a privileged
user.

## Usage example

```python
from kalliope import Session

endpoint = "http://user:password@192.168.1.1/"
conn = Session(endpoint)

accounts = conn.get("/rest/account").json()
print(accounts)
```

## Session

Event though Kalliope servers aren't session-aware a session object
helps regenerating the needed authentication header on every request.

To create a new session use a connection string in the format:
```python
Session("scheme://user:password@host:port/tenants_domain")
```
Where:

- **`scheme`** is either `http` or `https` (optional),
- **`user`** and **`password`** are the credentials (optional),
- **`host`** is the hostname or ip address,
- **`port`** is the port to connect to (optional),
- **`tenants_domain`** is the what the name suggests (optional).

If the scheme is not specified then the default one (`http`) is used but
be aware that you still need to place the double slash in front of the
url as per RFC???.

Username and password must be both present or both missing. If you wish
to give the credentials later use `Session.login`. Without login
information any requests will be performed unauthenticated.

The default tenant's domain is "`default`".

```python
conn = Session("http://admin:nimda@192.168.1.1")

response1 = conn.get("/rest/dashboard")
response2 = conn.get("/rest/account")

print("Req 1:", response1.request.headers["X-authenticate"])
print("Req 2:", response2.request.headers["X-authenticate"])
```
```
Req 1: RestApiUsernameToken Username="admin", Domain="default", Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", Nonce="bfb79078ff44c35714af28b7412a702b", Created="2016-04-29T15:48:26Z"
Req 2: RestApiUsernameToken Username="admin", Domain="default", Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", Nonce="bfb79078ff44c35714af28b7412a702b", Created="2016-04-29T15:48:26Z"
```

## Auth

The `kalliope.Auth` is a standalone class that can be used to generate
headers given the credentials and `salt` value.

```python
from kalliope import Auth

salt = fetch_salt_value(...)

auth = Auth("admin", "nimda", "default", salt)
print(auth.xauth())
```
```
{"X-authenticate": 'RestApiUsernameToken Username="admin", Domain="default", Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", Nonce="bfb79078ff44c35714af28b7412a702b", Created="2016-04-29T15:48:26Z"'}
```

The method `Auth.xauth` returns a `dict` with the newly generated token
and resets itself for the generation of the next one.

The `salt` value must be fetched and provided either while creating the
object or setting it in a second moment (`auth.salt = value`).

For testing purposes, the reset phase, can be inhibited with
`reset=False`. To quickly inspect the values it's also possible to print
the `Auth` object instance, i.e. `print(auth)`

```
X-authenticate: RestApiUsernameToken Username="admin", Domain="default", Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", Nonce="bfb79078ff44c35714af28b7412a702b", Created="2016-04-29T15:48:26Z"
```

### KalliopeAuth

The `requests.AuthBase` implementation is used by `kalliope.Session` to
update requests' headers. It is created upon login by `kalliope.Session`
itself. The salt value is automatically fetched from the server.

## License

This software is released under the
[LGPLv3](www.gnu.org/licenses/lgpl-3.0.html)  
GNU Lesser General Public License Version 3, 29 June 2007.
