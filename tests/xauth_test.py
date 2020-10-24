import unittest
from pykalliope import KAuth


# Values and expected results as per example in documentation:
#   doc/Manuale API REST KalliopePBX V4 per CDR.pdf
_USER = "admin"
_PASS = "admin"
_DOMAIN = "default"
_SALT = "b5a8fdcf2f8d5acdad33c4a072a97d7a"
_CREATED = "2016-04-29T15:48:26Z"
_NONCE = "bfb79078ff44c35714af28b7412a702b"

_EXPECTED_DIGEST = "+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40="
_EXPECTED_DIGEST_PASS = "dd7b0be7fa37d6cbaf0b842bf7532f229cb79ab8d54d509c2aa7eea27a53cd5e"
_EXPECTED_XHEADER_KEY = "X-authenticate"
_EXPECTED_XHEADER_VALUE = (
    'RestApiUsernameToken Username="admin", Domain="default", '
    'Digest="+PJg7Tb3v98XnL6iJVv+v5hwhYjdzQ2tIWxvJB2cE40=", '
    'Nonce="bfb79078ff44c35714af28b7412a702b", Created="2016-04-29T15:48:26Z"'
)
_EXPECTED_XHEADER_DICT = {_EXPECTED_XHEADER_KEY: _EXPECTED_XHEADER_VALUE}
_EXPECTED_XHEADER_STR = f"{_EXPECTED_XHEADER_KEY}: {_EXPECTED_XHEADER_VALUE}"


class AuthDocTest(unittest.TestCase):
    def setUp(self):
        self.auth = KAuth(None, _USER, _PASS, _DOMAIN)
        self.auth.salt = _SALT
        self.auth._created = _CREATED
        self.auth._nonce = _NONCE
        
    def test_xauth(self):
        self.assertEqual(str(self.auth), _EXPECTED_XHEADER_STR)
        
        xheader = self.auth.xauth(reset=False)
        self.assertDictEqual(xheader, _EXPECTED_XHEADER_DICT)
    
    def test_digest(self):
        self.assertEqual(self.auth.digest, _EXPECTED_DIGEST)
    
    def test_digest_pass(self):
        self.assertEqual(self.auth.digest_pass, _EXPECTED_DIGEST_PASS)
    
    def test_nonce(self):
        self.assertEqual(self.auth.nonce, _NONCE)
    
    def test_created(self):
        self.assertEqual(self.auth.created, _CREATED)
    
    def test_salt(self):
        self.assertEqual(self.auth.salt, _SALT)
