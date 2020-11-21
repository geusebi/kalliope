import unittest
from kalliopepbx import Auth
from .doc_example import (
    credentials as c,
    expected as expc
)


class AuthDocTest(unittest.TestCase):
    def setUp(self):
        self.auth = Auth(c.username, c.password, c.domain, c.salt)
        self.auth._created = c.created
        self.auth._nonce = c.nonce

    def test_xauth(self):
        self.assertEqual(str(self.auth), expc.xheader_str)

        xheader = self.auth.xauth(reset=False)
        self.assertDictEqual(xheader, expc.xheader_dict)

    def test_digest(self):
        self.assertEqual(self.auth.digest, expc.digest)

    def test_digest_pass(self):
        self.assertEqual(self.auth.digest_pass, expc.digest_pass)

    def test_nonce(self):
        self.assertEqual(self.auth.nonce, c.nonce)

    def test_created(self):
        self.assertEqual(self.auth.created, c.created)

    def test_salt(self):
        self.assertEqual(self.auth.salt, c.salt)
