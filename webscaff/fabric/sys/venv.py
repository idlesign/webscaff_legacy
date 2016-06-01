from os import path
from contextlib import contextmanager

from fabric.api import cd, prefix, task, run

from ..settings import PATH_REMOTE_PROJECT_BASE, PATH_REMOTE_PROJECT


NAME_VIRTUALENV_DIR = 'venv'
PATH_VENV = path.join(PATH_REMOTE_PROJECT_BASE, NAME_VIRTUALENV_DIR)


@contextmanager
def venv():
    """Temporarily switches into virtual environment."""
    with cd(PATH_REMOTE_PROJECT):
        with prefix('. %s/bin/activate' % PATH_VENV):
            yield


@task
def create(python_path):
    """Creates virtual environment using given Python interpreter path."""
    with cd(PATH_REMOTE_PROJECT_BASE):
        # Call as module in case `virtualenv` app is not [yet] available.
        run('python -m virtualenv -p %s %s/' % (python_path, NAME_VIRTUALENV_DIR))
