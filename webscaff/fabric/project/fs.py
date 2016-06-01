from os import path

from fabric.api import task, put
from fabric.contrib.project import upload_project

from ..sys.fs import create_dir as fs_create_dir
from ..sys.uwsgi import reload_touch as uwsgi_reload_touch
from ..utils import get_paths
from ..settings import NAME_CONFIGS_DIR


@task
def upload_configs():
    """Uploads project configuration files (under `conf` dir) to remote."""
    path_local, path_remote = get_paths(NAME_CONFIGS_DIR)
    fs_create_dir(path_remote)
    upload_project(path_local, path.dirname(path_remote))


@task
def put_files(files):
    """Puts files to remote and reloads uwsgi.

    :param files: local space-delimited filepaths relative to project root
        or absolute.

    """
    if ' ' in files:
        files = files.split()

    if not isinstance(files, list):
        files = [files]

    for fpath in files:
        path_local, path_remote = get_paths(fpath)
        put(path_local, path_remote)

    uwsgi_reload_touch()
