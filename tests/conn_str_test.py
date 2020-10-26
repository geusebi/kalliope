import unittest
from pykalliope.cs_re import cs_re


test_values = [
    ('http://example.com', ('http', None, None, 'example.com', None, None)),
    ('https://example.com', ('https', None, None, 'example.com', None, None)),
    ('http://example.com/default', ('http', None, None, 'example.com', None, 'default')),
    ('http://example.com:8080/default', ('http', None, None, 'example.com', '8080', 'default')),
    ('http://user:pass@example.com/default', ('http', 'user', 'pass', 'example.com', None, 'default')),
    ('   http://user:pass@example.com/default   ', ('http', 'user', 'pass', 'example.com', None, 'default')),
    ('http://user#:pass,@example.com/default-', ('http', 'user#', 'pass,', 'example.com', None, 'default-')),
    ('htp://example.com', None),
    ('http://user@example.com', None),
    ('http://user:@example.com', None),
]


class ConnectionStringTest(unittest.TestCase):
    def test_connection_string(self):
        for i, (conn_str, expected) in enumerate(test_values):
            with self.subTest(sub_test_num=i):
                match = cs_re.match(conn_str)
                if match:
                    self.assertEqual(match.groups(), expected)
                else:
                    self.assertEqual(None, expected)
