from os import path

from fabric.api import task, put as fabric_put

from ..sys.uwsgi import reload_touch
from ..sys.fs import create_dir, rm
from ..settings import PROJECT_NAME
from ..utils import get_paths


@task
def put_settings(reload_uwsgi=True):
    """Puts Django production settings file to remote and reloads uwsgi."""
    # todo set DEBUG=False automatically
    path_local, path_remote = get_paths('%s/settings/prod.py' % PROJECT_NAME)
    create_dir(path.dirname(path_remote))
    fabric_put(path_local, path_remote)

    reload_uwsgi and reload_touch()


@task
def drop_cache_fs():
    """Drops Django filesystem cache."""
    rm('/tmp/django_cache/*', use_local=False)
