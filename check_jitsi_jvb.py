#! /usr/bin/python3
#
# Icinga plugin for monitoring Jitsi Videobridge Health
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_jitsi_jvb
#
# Assumes private REST API is configured.  See:
# https://github.com/jitsi/jitsi-videobridge/blob/master/doc/health-checks.md
#

import argparse
import requests
import sys

parser = argparse.ArgumentParser(description="Icinga Jitsi Videobridge Plugin")

parser.add_argument(
    "--host",
    type=str,
    default="localhost",
    help="the REST API host (default: localhost)",
)
parser.add_argument(
    "--port", type=int, default=8080, help="the REST API port (default: 8080)"
)

args = parser.parse_args()


USER_AGENT = "check_jitsi_jvb.py/0.0.1 Icinga Plugin"
headers = {"user-agent": USER_AGENT}
base_url = "http://%s:%d" % (args.host, args.port)

try:
    r = requests.get("%s/about/health" % base_url, headers=headers)

    if r.status_code == 200:
        msg = ""
        try:
            r = requests.get("%s/colibri/stats" % base_url, headers=headers)
            msg = " - {participants} users in {conferences} conferences".format(
                **r.json()
            )
        except Exception as exc:  # xmpp interface not configured
            pass

        print("VIDEOBRIDGE OK%s" % msg)
        sys.exit(0)

except Exception as exc:  # timeout
    pass

print("VIDEOBRIDGE CRITICAL")
sys.exit(2)
