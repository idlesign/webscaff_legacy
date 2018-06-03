from fabric.api import task, run, put, lcd, local, cd
from os import path

from .uwsgi import reload_touch
from .venv import venv
from ..settings import PROJECT_NAME, PATH_LOCAL_PROJECT, PATH_GIT_ROOT
from ..utils import get_paths

PIP_REQUIREMENTS_FILENAME = 'requirements.txt'

__all__ = [
    'install_from_vcs', 'install', 'upgrade', 'upgrade_req', 'freeze',
]


@task
def install_from_vcs(package, vcs_path):
    """Installs python package(s) using pip from VCS

    :param str|list package: E.g.: sitetree
    :param str vcs_path: E.g.:https://github.com/idlesign/sitetree/@branch

    """
    with venv():
        run('pip3 install -e git+%s#egg=%s' % (vcs_path, package))


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

    with cd(PATH_GIT_ROOT):
        with venv():
            run('pip3 install %s %s' % (' '.join(flags), ' '.join(package)))


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
        local('pip3 freeze > %s' % PIP_REQUIREMENTS_FILENAME)
