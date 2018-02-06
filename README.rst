================
 Icinga Plugins
================

A collection of icinga2 plugins.


Wordpress Version Check
=======================

Checks if the installed version of Wordpress is current.

The Wordpress Version Plugin needs a php script in the Wordpress directory.

.. code-block:: bash

   ssh <uni-user>@dialog.rrz.uni-koeln.de

   cd <path/to/your/wp-load.php>
   wget https://raw.githubusercontent.com/cceh/icinga-plugins/master/icinga-wp-version.php
   chmod 755 icinga-wp-version.php

To test the installation enter this URL into your browser:

   http://your.wordpress.site/icinga-wp-version.php

The answer should be one line of text:

   WORDPRESS OK - Version = x.y.z

If it worked, tell Jonathan the URL you just used, so he can add it to the CCeH
Icinga.


Mediawiki Version Check
=======================

check_mediawiki_version.py


Free Memory Check
=================

Would you believe there is no standard icinga plugin to check free memory?

check_memory.py


Check Mensa
===========

Tongue-in-cheek plugin to check how many sections of the mensa are open at
University of Cologne.

* check_mensa.py


Passthru Plugin
===============

Echoes the check results gotten from a remote URL.  Needed for the Wordpress
version check.

* check_passthru.py
