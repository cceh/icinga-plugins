================
 Icinga Plugins
================

A collection of icinga2 plugins.

Copy the plugins into `/usr/local/lib/nagios/plugins/`


Wordpress Version Check
=======================

Checks if the installed version of Wordpress is current.

Installation
------------

The Wordpress Version Plugin needs a php script in the Wordpress directory.

.. code-block:: bash

   ssh <uni-user>@dialog.rrz.uni-koeln.de

   cd <path/to/your/wp-load.php>
   wget https://raw.githubusercontent.com/cceh/icinga-plugins/master/icinga-wp-version.php
   chmod 644 icinga-wp-version.php

To test the installation enter this URL into your browser:

   https://your.wordpress.site/icinga-wp-version.php

The answer should be one line of text:

   WORDPRESS OK - Version = x.y.z

Then use the passthru icinga plugin to connect to the php plugin:

   /path/to/check_passthru.py https://your.wordpress.site/icinga-wp-version.php


Mediawiki Version Check
=======================

* check_mediawiki_version.py


Free Memory Check
=================

Would you believe there is no standard icinga plugin to check free memory?

* check_memory.py


Reboot Required Check
=====================

Checks if the machine needs rebooting after a software update.

* check_reboot_required.py


Check Mensa
===========

Tongue-in-cheek plugin to check how many sections of the mensa are open at
University of Cologne.

* check_mensa.py


Passthru Plugin
===============

Echoes the check results obtained from a remote URL or local file.  Needed for the
Wordpress version check and pnpm audit.

* check_passthru.py


pnpm Audit
==========

Performs a pnpm audit of your project's javascript dependencies.

* check_pnpm_audit.py
