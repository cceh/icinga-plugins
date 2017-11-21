#! /usr/bin/python3
#
# Icinga plugin for monitoring MediaWiki versions.
#
# Copy this file into /usr/local/lib/nagios/plugins/
#
# Usage: check_mediawiki_version.py <url_of_wiki>
#

import re
import sys

from lxml import etree
import requests

USER_AGENT      = 'check_mediawiki_version.py/0.0.1 Icinga Plugin'
URL_MW_DOWNLOAD = 'https://www.mediawiki.org/wiki/Download'

parser = etree.HTMLParser ()
headers = { 'user-agent': USER_AGENT }

try:
    # Scrape the monitored mediawiki site. Look for:
    # <meta name="generator" content="MediaWiki 1.26.2" />

    current_version = None

    r = requests.get (sys.argv[1], headers = headers)
    r.raise_for_status ()

    root = etree.fromstring (r.content, parser)
    for e in root.xpath ('//meta[@name="generator"]'):
        m = re.match (r'^MediaWiki (\d+\.\d+\.\d+)$', e.get('content'))
        if m:
            current_version = m.group (1).split ('.')
            break

    if current_version is None:
        raise Exception ('<meta name="generator"> not found')

    # print (current_version)

    # Next scrape the mediawiki foundation download site.  Look for:
    # <a href="//releases.wikimedia.org/mediawiki/1.27/mediawiki-1.27.3.tar.gz">download</a>

    supported_versions = []

    r = requests.get (URL_MW_DOWNLOAD, headers = headers)
    r.raise_for_status ()

    root = etree.fromstring (r.content, parser)
    for e in root.xpath ('//table//a[starts-with (@href, "//releases.wikimedia.org/mediawiki/")]'):
        m = re.search ('\d+\.\d+\.\d+', e.get ('href'))
        if m:
            supported_versions.append (m.group (0).split ('.'))

    # print (supported_versions)

    # check if the monitored site is still supported
    # and exit accordingly

    if current_version in supported_versions:
        print ("MEDIAWIKI OK - Version: %s" % '.'.join (current_version))
        sys.exit (0)

    upgrade_paths = [ '.'.join (v) for v in sorted (supported_versions) if v > current_version ]
    # print (upgrade_paths)

    print ("MEDIAWIKI CRITICAL - Version: %s, Supported versions: %s" %
           ('.'.join (current_version), ', '.join (upgrade_paths)))
    sys.exit (2)

except Exception as exc:
    print ("MEDIAWIKI UNKNOWN: %s" % str (exc))
    sys.exit (3)
