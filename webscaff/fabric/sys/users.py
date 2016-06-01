from fabric.api import task, sudo

from .fs import append_to_file


@task
def create(user):
    """Creates a user."""
    sudo('adduser %s' % user)


@task
def add_to_sudoers(user):
    """Adds a user to sudoers."""
    append_to_file("'%s ALL=(ALL:ALL) ALL'", '/etc/sudoers')


@task
def add_to_group(user, group):
    """Adds a user into a group."""
    sudo('usermod -a %s -G %s' % (user, group))
