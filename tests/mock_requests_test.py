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
            'http://192.168.1.1:8080/',
            json={},
            status=200
        )

        responses.add(
            responses.GET,
            'http://192.168.1.1:8080/rest/salt/default',
            json={"salt": c.salt},
            status=200
        )
    
    @responses.activate
    def test_get_salt(self):
        conn = KSession.from_cs("http://admin:admin@192.168.1.1:8080/")
        
        _ = conn.get("/")
        
        self.assertEqual(conn.auth.salt, c.salt)
