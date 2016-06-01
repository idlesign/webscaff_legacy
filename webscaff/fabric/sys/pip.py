from os import path

from fabric.api import task, run, put, lcd, local

from .venv import venv
from .uwsgi import reload_touch

from ..utils import get_paths
from ..settings import PROJECT_NAME, PATH_LOCAL_PROJECT


PIP_REQUIREMENTS_FILENAME = 'requirements.txt'


@task
def install_from_vcs(package, vcs_path):
    """Installs python package(s) using pip from VCS

    :param str|list package: E.g.: sitetree
    :param str vcs_path: E.g.:https://github.com/idlesign/sitetree/@branch

    """
    with venv():
        run('pip install -e git+%s#egg=%s' % (vcs_path, package))


@task
def install(package='', update=False, from_req=False, editable=False):
    """Installs python package(s) using pip

    :param str|list package:
    :param bool update:
    :param bool from_req:
    :param bool editable: Editable install, aka developer install.

    """
    flags = []

    update and flags.append('-U')
    editable and flags.append('-e')

    if from_req:
        package = '-r %s' % PIP_REQUIREMENTS_FILENAME

    if not isinstance(package, list):
        package = [package]

    with venv():
        run('pip install %s %s' % (' '.join(flags), ' '.join(package)))


@task
def upgrade(package):
    """Upgrades a package."""
    install(package=package, update=True)


@task
def upgrade_req():
    """Upgrades env with requirements from file."""
    path_local, path_remote = get_paths(path.join(PROJECT_NAME, PIP_REQUIREMENTS_FILENAME))
    put(path_local, path_remote)
    install(update=True, from_req=True)
    reload_touch()


@task
def freeze():
    """Created pip requirements file locally."""
    lcd(PATH_LOCAL_PROJECT)
    with venv():
        local('pip freeze > %s' % PIP_REQUIREMENTS_FILENAME)
