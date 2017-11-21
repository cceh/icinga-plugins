#! /usr/bin/python3
#
# This Icinga plugin requests an URL and just passes thru the string it gets.
# The string is also interpreted as space-separated list and the second field in
# it is interpreted as the plugin status.
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_passthru.py <url_returning_string>
#

import sys

import requests

USER_AGENT = 'check_passthru.py/0.0.1 Icinga Plugin'

headers = { 'user-agent': USER_AGENT }

try:
    if len (sys.argv) != 2:
        raise ("Usage: %s URL" % sys.argv[0])

    r = requests.get (sys.argv[1], headers = headers)
    r.raise_for_status ()

    print (r.text)

    fields = r.text.split ()
    if fields[1] == 'CRITICAL':
        sys.exit (2)
    if fields[1] == 'WARNING':
        sys.exit (1)
    sys.exit (0)

except Exception as exc:
    print ("UNKNOWN UNKNOWN: %s" % str (exc))
    sys.exit (3)
