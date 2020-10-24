from .auth import KAuth
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

# todo: test against a kalliope server
# todo: add unit tests
# todo: add meaningful documentation


class KSession(object):
    _def_headers = {
        "Accept": "application/json"
    }
    
    def __init__(self, scheme, address, timeout=4, headers=None):
        self.scheme, self.address = scheme, address
        
        self.timeout = timeout
        
        if headers is None:
            headers = {}
        self.headers = {**KSession._def_headers, **headers}
        
        self.auth = None
    
    def login(self, username, password, domain="default"):
        self.auth = KAuth(self, username, password, domain)
        return self
    
    def logout(self):
        self.auth = None
        return self
    
    def prepare_url(self, path):
        if path.startswith("/"):
            path = path[1:]
        return f"{self.scheme}://{self.address}/{path}"
    
    def prepare_headers(self, noauth=False, headers=None):
        if headers is None:
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
        headers = self.prepare_headers(noauth, headers)
        return requests.request(method, url, headers=headers, *args, **kwargs)
    
    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)
    
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.request("DELETE", *args, **kwargs)

'''
# Idea for a connection string
alnumspec = "[a-z0-9!?.,$-]"
urlstring = f"""
    ^
    \s*                                 # leading space
    (?P<scheme>http|https)://           # "scheme" ://
    (                                   # optional "user:pass@"
        (?P<username>{alnumspec}+):     # "user"
        (?P<password>{alnumspec}+)      # "pass"
        @
    )?
    (?P<address>[a-zA-Z0-9.-]+)         # "address"
    (/                                  # optional "/" something
        (?P<tenant>{alnumspec}+)?       # optional tenant
    )?
    \s*                                 # trailing space
    $
"""
#urlstring_re = re.compile(urlstring_re, re.VERBOSE | re.INSENSITIVE)
'''
