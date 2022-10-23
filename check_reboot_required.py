#! /usr/bin/python3
#
# This Icinga plugin checks if the machine needs rebooting.
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_reboot_required.py [-w seconds] [-c seconds]
#

import argparse
from datetime import timedelta
import os.path
import time
import sys

PATH = "/var/run/reboot-required"
PATH_PKGS = "/var/run/reboot-required.pkgs"

parser = argparse.ArgumentParser (description = 'Icinga Reboot-Required Plugin')
parser.add_argument('-w', '--warning', type = int, default = 0,
                    help = 'the timespan in seconds before a reboot becomes a warning (default: 0)')
parser.add_argument('-c', '--critical', type = int, default = 7 * 86400,
                    help = 'the timespan in seconds before a reboot becomes critical (default: 7 days)')

args = parser.parse_args ()

try:
    delay = 0
    delay_msg = ""

    if os.path.isfile(PATH):
        delay = time.time() - os.path.getmtime(PATH)
        delay_msg = f" - Machine requires a reboot. ({timedelta(seconds = int(delay))})"
        with open(PATH_PKGS, "r") as fp:
            pkgs = [line.strip() for line in fp]
            delay_msg += " Packages: " + ", ".join(pkgs)

    if delay > args.critical:
        print(f"REBOOT ERROR{delay_msg}")
        sys.exit(2)
    if delay > args.warning:
        print(f"REBOOT WARNING{delay_msg}")
        sys.exit(1)
    if delay > 0:
        print("REBOOT OK{delay_msg}")
        sys.exit (0)
    print("REBOOT OK")
    sys.exit (0)

except Exception as exc:
    print ("UNKNOWN UNKNOWN: %s" % str (exc))
    sys.exit (3)
