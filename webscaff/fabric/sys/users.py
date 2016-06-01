from fabric.api import task, sudo, run, local, warn_only

from .fs import append_to_file


@task
def create(user):
    """Creates a user."""
    if get_id(user) is None:
        sudo('adduser %s' % user)


@task
def add_to_sudoers(user):
    """Adds a user to sudoers."""
    append_to_file("'%s ALL=(ALL:ALL) ALL'", '/etc/sudoers')


@task
def add_to_group(user, group):
    """Adds a user into a group."""
    sudo('usermod -a %s -G %s' % (user, group))


@task
def get_id(user):
    """Returns user ID. Might be used to check whether user exists."""
    with warn_only():
        result = sudo('id -u %s' % user).strip()

    return int(result) if result.isdigit() else None
