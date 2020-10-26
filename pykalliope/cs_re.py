import re

# The format of conn_str_re matches connection strings of the form:
#   http://user:pass@host/domain
# Where:
#   - scheme is either "http" or "https" and it is non optional,
#   - user and pass are optional but have to be both present or unspecified,
#   - host is a valid hostname (fqdn too),
#   - port is a valid host port and is optional,
#   - domain is the tenant's domain and is optional.

# Common character class definitions
alnum = r"[a-zA-Z0-9]"
alnumd = r"[a-zA-Z0-9-]"
# alpha + digit + special (except colon and at-symbol)
alnumspec = r"[a-zA-Z0-9!-/;-?[-`{-~]"

scheme = r"(?P<scheme>http|https)"
# "user", "password", and "domain" could contain any alphanumeric
#  character and any symbol except ":" (colon) and "@" (at-symbol)
username = fr"(?P<username>{alnumspec}+)"
password = fr"(?P<password>{alnumspec}+)"
domain = fr"(?P<domain>{alnumspec}+)"  # As in "tenant's domain"

# Port number is any digit with a length of 1 to 5 
# ports 0 and from 65536 to 99999 are considered valid because regexes
# tend to be unreadable is these cases (i.e.):
#   "6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{1,3}?"
port = r"(?P<port>[0-9]{1,5})"

# A "host" is a series of one or more labels followed by a "." (dot).
# Every label is an alphanumeric string which could contain "-"s (dash)
# but could not start or end with them.
# The last dot is optional (fqdn).
host = fr"""
  (?P<host>
    (?:{alnum}                # on ore more alphanum sequences that can
      (?:{alnumd}*{alnum})?   # have - inside but not at the start nor
      [.]?                    # at the end and is followed by an optional .
    )+
  )
"""

# Connection string as per definition laid out earlier.
connection_string = fr"""
  ^\s*                            # leading space
  {scheme}://                     # "scheme://"
  (?:{username}:{password}@)?     # optional "user:pass@"
  {host}                          # "address"
  (?::{port})?                    # optional "port"
  (?:/{domain}?)?                 # optional "/" or "/domain"
  \s*$                            # trailing space
"""

connection_string_re = re.compile(connection_string, re.VERBOSE)
# Aliases
conn_str_re = cs_re = connection_string_re


__all__ = ["connection_string_re", "conn_str_re", "cs_re"]
