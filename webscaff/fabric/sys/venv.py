from contextlib import contextmanager
from fabric.api import cd, prefix, task, run
from fabric.contrib.files import exists
from os import path

from ..settings import PATH_REMOTE_PROJECT_BASE

NAME_VIRTUALENV_DIR = 'venv'
PATH_VENV = path.join(PATH_REMOTE_PROJECT_BASE, NAME_VIRTUALENV_DIR)


__all__ = ['venv', 'create']


@contextmanager
def venv():
    """Temporarily switches into virtual environment."""
    with prefix('. %s/bin/activate' % PATH_VENV):
        yield


@task
def create(python_path):
    """Creates virtual environment using given Python interpreter path
    if not already created.

    """
    if exists(path.join(PATH_REMOTE_PROJECT_BASE, NAME_VIRTUALENV_DIR)):
        return

    with cd(PATH_REMOTE_PROJECT_BASE):
        # Call as module in case `virtualenv` app is not [yet] available.
        run('python -m virtualenv -p %s %s/' % (python_path, NAME_VIRTUALENV_DIR))
