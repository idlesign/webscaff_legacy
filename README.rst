webscaff
========
https://github.com/idlesign/webscaff

.. image:: https://img.shields.io/pypi/v/webscaff.svg
    :target: https://pypi.python.org/pypi/webscaff

.. image:: https://img.shields.io/pypi/dm/webscaff.svg
    :target: https://pypi.python.org/pypi/webscaff

.. image:: https://img.shields.io/pypi/l/webscaff.svg
    :target: https://pypi.python.org/pypi/webscaff


Description
-----------

*Scaffolding for web applications.*

This will help you to prepare a remote environment (e.g. on VPS) for your web application.
But not only that, this also will help you managing it: deployment, system upgrades, backups, etc.


Contains:

* Configuration samples for Nginx, PosgreSQL, uWSGI.
* Useful Fabric commands for managing your project (this includes Django-specific commands).


Command examples:

.. code-block:: bash

    # Update project code from repository.
    $ fab update -c .fab.conf

    # Get remote code and DB dumped as .tar.gz.
    $ fab dump -c .fab.conf

    # Upgrade OS packages.
    $ fab upgrade_os -c .fab.conf

    # Upgrade project requirements via PIP.
    $ fab upgrade_req -c .fab.conf


Requirements
------------

* Debian-based OS (e.g. Ubuntu)
* Python 3.2+
* Django (advised)
