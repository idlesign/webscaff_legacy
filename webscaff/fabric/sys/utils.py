from fabric.api import task, sudo, run

from .apt import upgrade as apt_upgrade
from .certs import update as certs_update
from .fs import chmod
from .nginx import maintenance as nginx_maintenance, stopped as nginx_stopped

__all__ = [
    'set_locale', 'status', 'info', 'reboot', 'upgrade_os_packages',
    'update_certs', 'swap_make', 'swap_on', 'swap_off', 'shutdown']


@task
def set_locale(locale='ru_RU'):
    """Generates and sets given UTF-8 locale.

    Default: ru_Ru

    """
    sudo('locale-gen "%s.UTF-8"' % locale)
    sudo('dpkg-reconfigure locales')
    sudo('update-locale LC_ALL=%(locale)s.UTF-8 LANG=%(locale)s.UTF-8' % {'locale': locale})


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
def shutdown():
    """Turns the remote off immediately."""
    sudo('shutdown now')


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
    chmod(swap_file, 600)
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
