from fabric.api import task, sudo


BOOTSTRAP_SYSTEM_PACKAGES = [
    'git',
    'nginx',
    'uwsgi uwsgi-plugin-python3',

    'build-essential',

    'python3-dev',
    'python3-pip',
    'python-virtualenv',

    'postgresql',
    'libpq-dev',
    'python3-psycopg2',

    # Pillow requirement.
    'libjpeg-dev',
    # lxml requirement.
    'libxml2-dev',
    'libxslt1-dev',

    # Utils.
    'mc',
    'htop',
    'certbot',
    'net-tools',
]

__all__ = ['upgrade_os', 'update', 'upgrade', 'install', 'remove', 'bootstrap']

@task
def upgrade_os():
    """Initiates remote OS packages update and upgrade procedure."""
    update()
    upgrade()


@task
def upgrade():
    """Initiates remote OS upgrade procedure."""
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
