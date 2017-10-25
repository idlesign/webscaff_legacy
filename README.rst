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
    $ fab -c .fab.conf update

    # Get remote code and DB dumped as .tar.gz.
    $ fab -c .fab.conf dump

    # Upgrade OS packages.
    $ fab -c .fab.conf upgrade_os

    # Upgrade project requirements via PIP.
    $ fab -c .fab.conf upgrade_req


Requirements
------------

* Debian-based OS (e.g. Ubuntu)
* Python 3.2+
* Django (advised)


Expectations
------------

Expected project layout::

    <project_name>/conf/                            * Configs (nginx, uwsgi, etc.)
    <project_name>/venv/                            * Virtual environment
    <project_name>/fabfile.py                       * Fabric commands file
    <project_name>/.fab.conf                        * Fabric config file
    <project_name>/setup.py                         * Minimal setup file
    <project_name>/<project_name>/requirements.txt  * PIP requirements
    <project_name>/<project_name>/wsgi.py           * wsgi application file
    <project_name>/<project_name>/manage.py         * Manage file
    <project_name>/<project_name>/settings/settings_production.py  * Production settings
