import unittest 
from kalliope import Session
from .doc_example import (
    credentials as c,
    expected as expc
)
import responses


_DUMMY_DATA = {"foo": "bar"}


class RequestsTest(unittest.TestCase):
    def setUp(self):
        responses.add(
            responses.GET,
            'http://192.168.1.1:8080/rest/account',
            json=_DUMMY_DATA,
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
        conn = Session("http://admin:admin@192.168.1.1:8080/")
        
        _ = conn.get("/rest/account")

        self.assertEqual(conn.auth.salt, c.salt)

    @responses.activate
    def test_get_response(self):
        conn = Session("http://admin:admin@192.168.1.1:8080/")
        
        response = conn.get("/rest/account")

        self.assertIn("X-authenticate", response.request.headers.keys())

        data = response.json()
        self.assertEqual(data, _DUMMY_DATA)
