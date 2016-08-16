from fabric.api import task, sudo, run

from .apt import upgrade as apt_upgrade
from .certs import update as certs_update
from .nginx import maintenance as nginx_maintenance, stopped as nginx_stopped


@task
def status():
    """Prints out basic remote status information, including uptime."""
    run('uptime')


@task
def info():
    """Prints out remote system information, including kernel info and timezone."""
    run('uname -a')
    run('cat /etc/timezone')
    run('df -h')


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


@task
def swap_make():
    """Creates a swap file."""
    swap_file = '/swapfile'
    sudo('dd if=/dev/zero of=%s bs=1024 count=524288' % swap_file)
    sudo('chmod 600 %s' % swap_file)
    sudo('mkswap %s' % swap_file)
    swap_on()


@task
def swap_on():
    """Turns on swap."""
    swap_file = '/swapfile'
    sudo('swapon %s' % swap_file)


@task
def swap_off():
    """Turns off swap."""
    swap_file = '/swapfile'
    sudo('swapoff %s' % swap_file)
