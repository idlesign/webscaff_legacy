from fabric.api import task, sudo, run

from .apt import upgrade as apt_upgrade
from .certs import update as certs_update
from .nginx import maintenance as nginx_maintenance, stopped as nginx_stopped


@task
def status():
    """Returns remote basic status information, including uptime."""
    run('uname -a')
    run('uptime')


@task
def reboot():
    """Reboots remote immediately."""
    sudo('shutdown -r now')


@task
def upgrade_os_packages():
    """Upgrades OS packages."""
    with nginx_maintenance():
        apt_upgrade()


@task
def update_certs():
    """Updates Let's encrypt SSL certificates."""
    with nginx_stopped():
        certs_update()
