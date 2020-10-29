import unittest
from kalliope.utils import parse_conn_str 
from types import SimpleNamespace as NS


test_values = [
    ('http://example.com', NS(domain='default', hostname='example.com', password=None, port=None, scheme='http', username=None)),
    ('https://example.com', NS(domain='default', hostname='example.com', password=None, port=None, scheme='https', username=None)),
    ('http://example.com/default', NS(domain='default', hostname='example.com', password=None, port=None, scheme='http', username=None)),
    ('http://example.com:8080/default', NS(domain='default', hostname='example.com', password=None, port=8080, scheme='http', username=None)),
    ('http://user:pass@example.com/default', NS(domain='default', hostname='example.com', password='pass', port=None, scheme='http', username='user')),
    ('   http://user:pass@example.com/default   ', NS(domain='default', hostname='example.com', password='pass', port=None, scheme='http', username='user')),
    ('http://user#:pass,@example.com/default-', NS(domain='default', hostname='user', password=None, port=None, scheme='http', username=None)),
    ('htp://example.com', (ValueError, "Unsupported scheme 'htp'")),
    ('http://user@example.com', (ValueError, "Incomplete login credentials'")),
    ('http://user:   @example.com', (ValueError, "Incomplete login credentials'")),
]


class ConnectionStringTest(unittest.TestCase):
    def test_connection_string(self):
        for i, (conn_str, expected) in enumerate(test_values):
            with self.subTest(sub_test_num=i):
                if isinstance(expected, tuple):
                    exception, message = expected
                    with self.assertRaises(exception, msg=message):
                        parts = parse_conn_str(conn_str)
                        print(parts)
                else:
                    parts = parse_conn_str(conn_str)
                    self.assertEqual(parts, expected)
