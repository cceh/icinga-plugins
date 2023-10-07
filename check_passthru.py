#! /usr/bin/python3
#
# This Icinga plugin requests an URL or opens a file and just passes thru the content
# verbatim.  The content is supposed to be already in the correct format:
#
#   NAME STATUS MESSAGE
#
# The string is also interpreted as space-separated list and the STATUS field
# is returned as the plugin's exit code:
#
#   OK = 0, WARNING = 1, CRITICAL = 2, UNKNOWN = 3.
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_passthru.py <url_returning_string>
#        check_passthru.py <file:///path/to/file>
#

import sys

import requests

USER_AGENT = "check_passthru.py/0.0.1 Icinga Plugin"

headers = {"user-agent": USER_AGENT}

try:
    if len(sys.argv) != 2:
        raise Exception("Usage: %s URL|FILE" % sys.argv[0])

    text = ""
    if sys.argv[1].startswith("http"):
        r = requests.get(sys.argv[1], headers=headers)
        r.raise_for_status()
        text = r.text
    if sys.argv[1].startswith("file://"):
        with open(sys.argv[1][7:]) as fp:
            text = fp.read()

    print(text.strip())

    fields = text.split()
    f = fields[1].strip(":")
    if f == "OK":
        sys.exit(0)
    if f == "WARNING":
        sys.exit(1)
    if f == "CRITICAL":
        sys.exit(2)
    sys.exit(3)

except Exception as exc:
    print("UNKNOWN UNKNOWN: %s" % str(exc))
    sys.exit(3)
