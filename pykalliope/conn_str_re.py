import re


alnumspec = "[a-zA-Z0-9!-/;-?[-`{-~]"  # alpha digit special (except colon and at-symbol)

scheme = "(?P<scheme>http|https)"
username = f"(?P<username>{alnumspec}+)"
password = f"(?P<password>{alnumspec}+)"
address = "(?P<address>[a-zA-Z0-9.-]+)"
domain = f"(?P<domain>{alnumspec}+)"

conn_str = f"""
    ^\s*                            # leading space
    {scheme}://                     # "scheme://"
    (?:{username}:{password}@)?     # optional "user:pass@"
    {address}                       # "address"
    (?:/{domain}?)?                 # optional "/" or "/domain"
    \s*$                            # trailing space
"""

conn_str_re = re.compile(conn_str, re.VERBOSE)

__all__ = ["conn_str_re"]