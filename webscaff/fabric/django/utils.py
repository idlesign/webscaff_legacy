from os import path

from fabric.api import task, put as fabric_put

from ..settings import PROJECT_NAME
from ..sys.fs import create_dir, rm, chmod
from ..sys.uwsgi import reload_touch
from ..utils import get_paths

DIR_CACHE = '/tmp/django_cache/'


__all__ = ['put_settings', 'cache_fs_drop', 'cache_fs_init']


@task
def put_settings(reload_uwsgi=True):
    """Puts Django production settings file to remote and reloads uwsgi."""
    # todo set DEBUG=False automatically
    path_local, path_remote = get_paths('%s/settings/settings_production.py' % PROJECT_NAME)
    create_dir(path.dirname(path_remote))
    fabric_put(path_local, path_remote)

    reload_uwsgi and reload_touch()


@task
def cache_fs_drop():
    """Drops Django filesystem cache."""
    rm('%s*' % DIR_CACHE, use_local=False)


@task
def cache_fs_init():
    """Initializes django fs cache directory"""
    rm(DIR_CACHE, use_local=False)

    create_dir(DIR_CACHE)
    # Accessed both as project user and webserver
    chmod(DIR_CACHE, 770)
