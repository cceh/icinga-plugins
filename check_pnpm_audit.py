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
# is to call this script from the developer's own crontab, like this:
#
#   /path/to/check_pnpm_audit.py > /tmp/pnpm_audit.txt
#
# This puts the result of the audit into an accessible location.  Then use the
# check_passthru plugin to pass the audit result to icinga:
#
#   /path/to/check_passthru.py file:///tmp/pnpm_audit.txt
#

import argparse
import json
import subprocess
import sys

NAME="VULN"

LEVELS={"info": 1, "low": 2, "moderate": 3, "high": 4, "critical": 5}

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
    "-w", "--warning",
    choices=LEVELS.keys(),
    default="low",
    help='the audit level for icinga WARNING status (default: "low")',
)
parser.add_argument(
    "-c", "--critical",
    choices=LEVELS.keys(),
    default="high",
    help='the audit level for icinga CRITICAL status (default: "high")',
)

args = parser.parse_args()


def usage():
    parser.print_usage()


try:
    cp = subprocess.run(
        [args.pnpm, "audit", "--json"],
        cwd=args.cwd,
        text=True,
        capture_output=True,
    )
    jso = json.loads(cp.stdout)

    modules_critical = []
    modules_warning = []
    critical = LEVELS[args.critical]
    warning = LEVELS[args.warning]

    for _, advisory in jso["advisories"].items():
        severity = LEVELS.get(advisory["severity"], LEVELS["high"])
        if severity >= critical:
            modules_critical.append(advisory["module_name"])
        elif severity >= warning:
            modules_warning.append(advisory["module_name"])

    if len(modules_critical):
        print(f"{NAME} CRITICAL - {', '.join(modules_critical)}")
        sys.exit(2)
    if len(modules_warning):
        print(f"{NAME} WARNING - {', '.join(modules_warning)}")
        sys.exit(1)
    print(f"{NAME} OK")
    sys.exit(0)

except Exception as exc:
    print(f"{NAME} UNKNOWN {str(exc)}")
    sys.exit(3)
