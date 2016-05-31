from fabric.api import task, sudo


@task
def add_to_sudoers(user):
    """Adds a user to sudoers."""
    sudo("echo '%s ALL=(ALL:ALL) ALL' >> /etc/sudoers" % user)


@task
def add_to_group(user, group):
    """Adds a user into a group."""
    sudo('usermod -a %s -G %s' % (user, group))
