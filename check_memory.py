#! /usr/bin/python3
#
# Icinga plugin for monitoring memory on Linux systems.
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_memory.py [-w 75 -c 90]
#

import argparse
import re
import sys

parser = argparse.ArgumentParser (description = 'Icinga Memory Plugin')
parser.add_argument('-w', '--warning', type = int, default = 90,
                    help = 'the warning level (default: 90%)')
parser.add_argument('-c', '--critical', type = int, default = 95,
                    help = 'the critical level (default: 95%)')

args = parser.parse_args ()

total = 0
available = 0

try:
    with open ('/proc/meminfo', 'r') as fp:
        for line in fp.readlines ():
            m = re.match ('^(\w+):\s+(\d+)\s', line)
            if (m):
                if m.group (1) == 'MemTotal':
                    total = int (m.group (2));
                if m.group (1) == 'MemAvailable':
                    available = int (m.group (2));
except IOError:
    print ("MEMORY UNKNOWN - could not read from /proc/meminfo")
    sys.exit (3)

if total == 0 or available == 0:
    print ("MEMORY UNKNOWN - could not parse format of /proc/meminfo")
    sys.exit (3)

free = (available / total) * 100
used = 100 - free

# perfdata format:
# 'label'=value[UOM];[warn];[crit];[min];[max]
# eaxmple:
# | /backup=574750MB;938671;938721;0;938771

perfdata = " - %.1f%% free | memory=%.2f%%;%.2f;%.2f;%.2f;%.2f" % (free, used, args.warning, args.critical, 0, 100)

if used > args.critical:
    print ("MEMORY CRITICAL" + perfdata)
    sys.exit (2)

if used > args.warning:
    print ("MEMORY WARNING" + perfdata)
    sys.exit (1)

print ("MEMORY OK" + perfdata)
sys.exit (0)
