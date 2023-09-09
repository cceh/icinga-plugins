#! /usr/bin/python3
#
# Icinga plugin for monitoring the Uni Mensa
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_mensa
#

import datetime
import re
import sys
import traceback

from lxml import html
import requests

SERVICE_NAME = "MENSA"
SECTIONS = ["EG Nord", "EG Süd", "MG Nord", "MG Süd"]
URL = "https://www.kstw.de/gastronomie/speiseplan?l=1"
USER_AGENT = "check_mensa.py/0.0.1 Icinga Plugin"

try:
    # Scrape the mensa site.

    r = requests.get(URL, headers={"user-agent": USER_AGENT})
    r.raise_for_status()

    # The server just sends an HTML fragment without encoding information. It
    # works for them because the fragment gets inserted into an utf-8 encoded
    # page, thus inheriting the encoding.  But we have to declare the encoding
    # explicitly.
    # r.encoding = 'utf-8'

    # Look for <div class="tx-epwerkmenu-menu-locationpart-title"><strong>MG Nord</strong></div>

    up = set()
    root = html.fromstring(r.text)
    for e in root.xpath(
        '//div[contains (concat (" ", @class, " "), " tx-epwerkmenu-menu-locationpart-title ")]'
    ):
        # print (e.text_content ())
        m = re.search(r"(EG|MG)\s+(Nord|Süd)", e.text_content())
        if m:
            up.add("%s %s" % (m.group(1), m.group(2)))

    down = set(SECTIONS) - up

    # exit

    data = {
        "name": SERVICE_NAME,
        "up": len(up),
        "down": len(down),
        "ups": ", ".join(sorted(up)),
        "downs": ", ".join(sorted(down)),
    }

    if data["down"] == 0:
        print("{name} OK - {up} UP ({ups})".format(**data))
        sys.exit(0)

    if data["up"] >= 1:
        print("{name} WARNING - {up} UP ({ups}) - {down} DOWN ({downs})".format(**data))
        sys.exit(1)

    print("{name} CRITICAL - {down} DOWN ({downs})".format(**data))
    sys.exit(2)

except Exception as exc:
    print("%s UNKNOWN - %s" % (SERVICE_NAME, str(exc)))
    traceback.print_exc()
    sys.exit(3)
