import unittest 
from pykalliope import KSession
from .doc_example import (
    credentials as c,
    expected as expc
)
import responses


class RequestsTest(unittest.TestCase):
    def setUp(self):
        responses.add(
            responses.GET,
            'http://192.168.1.1/',
            json={},
            status=200
        )

        responses.add(
            responses.GET,
            'http://192.168.1.1/rest/salt/default',
            json={"salt": c.salt},
            status=200
        )
    
    @responses.activate
    def test_get_salt(self):
        conn = KSession("http", "192.168.1.1")
        conn.login("admin", "admin", "default")
        
        _ = conn.get("/")
        
        self.assertEqual(conn.auth.salt, c.salt)
