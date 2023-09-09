#! /usr/bin/python3
#
# This Icinga plugin calls pnpm audit
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_pnpm_audit.py <directory> [low|moderate|high|critical]
#
# <directory> is where the file :file:`pnpm-lock.yaml` is located.
#
# The icinga user should have no rights to open a developer's directory.  The secure way
# is to call this script from the developer's cron, like this:
#
#   /path/to/check_pnpm_audit.py > /tmp/pnpm_audit.txt
#
# This puts the result of the audit into an accessible location.  Then use the
# check_passthru plugin to pass the audit result to icinga:
#
#   /path/to/check_passthru.py file:///tmp/pnpm_audit.txt
#

import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="Icinga pnpm Audit Plugin")
parser.add_argument(
    "--pnpm",
    default="pnpm",
    metavar="EXECUTABLE",
    help='the path to the pnpm executable (default: "pnpm")',
)
parser.add_argument(
    "--cwd",
    default=".",
    metavar="DIRECTORY",
    help='the directory where the file pnpm-lock.yaml is located (default: ".")',
)
parser.add_argument(
    "--severity",
    choices=["low", "moderate", "high", "critical"],
    default="low",
    help='the audit level (default: "low")',
)

args = parser.parse_args()


def usage():
    parser.print_usage()


try:
    cp = subprocess.run(
        [args.pnpm, "audit", "--audit-level", args.severity],
        cwd=args.cwd,
        text=True,
        capture_output=True,
    )
    if cp.returncode != 0:
        print("AUDIT WARNING: %s" % cp.stdout.strip())
        sys.exit(1)
    print("AUDIT OK: %s" % cp.stdout.strip())
    sys.exit(0)

except Exception as exc:
    print("UNKNOWN UNKNOWN: %s" % str(exc))
    sys.exit(3)
