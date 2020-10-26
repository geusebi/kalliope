import re


alnum = r"[a-zA-Z0-9]"
alnumd = r"[a-zA-Z0-9-]"
# alpha + digit + special (except colon and at-symbol)
alnumspec = r"[a-zA-Z0-9!-/;-?[-`{-~]"

scheme = r"(?P<scheme>http|https)"
username = fr"(?P<username>{alnumspec}+)"
password = fr"(?P<password>{alnumspec}+)"
port = r"(?P<port>[0-9]{1,5})" 
domain = fr"(?P<domain>{alnumspec}+)"  # As in "tenant's domain"

host = fr"""
  (?P<host>
    (?:{alnum}                # on ore more alphanum sequences that can
      (?:{alnumd}*{alnum})?   # have - inside but not at the start nor
      [.]?                    # at the end and followed by an optional .
    )+
  )
"""

conn_str = fr"""
  ^\s*                            # leading space
  {scheme}://                     # "scheme://"
  (?:{username}:{password}@)?     # optional "user:pass@"
  {host}                          # "address"
  (?::{port})?                    # optional "port"
  (?:/{domain}?)?                 # optional "/" or "/domain"
  \s*$                            # trailing space
"""

conn_str_re = re.compile(conn_str, re.VERBOSE)

__all__ = ["conn_str_re"]
