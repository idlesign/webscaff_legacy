from fabric.api import task, sudo


BOOTSTRAP_SYSTEM_PACKAGES = [
    'git',
    'nginx',
    'uwsgi uwsgi-plugin-python3',

    'python3-dev',
    'python3-pip',
    'python-virtualenv',

    'postgresql',
    'libpq-dev',

    # Pillow requirement.
    'libjpeg-dev',
]


@task
def upgrade():
    """Initiates remote OS upgrade procedure."""
    update()
    sudo('apt-get upgrade')


@task
def update():
    """Initiates apt cache update."""
    sudo('apt-get update')


@task
def install(packages):
    """Installs packages using apt.

    :param packages:

    """
    if not isinstance(packages, list):
        packages = [packages]

    update()
    sudo('apt-get -y install %s' % ' '.join(packages))


@task
def remove(packages):
    """Removes package(s) using apt.

    :param packages:
    """
    sudo('apt-get -y remove %s' % packages)


@task
def bootstrap():
    """Bootstraps system by installing required packages."""
    install(BOOTSTRAP_SYSTEM_PACKAGES)
