from datetime import datetime
from os import path, makedirs

from fabric.api import task, get
from fabric.contrib.files import exists

from . import fs as project_fs
from ..django.manage import migrate as dj_migrate, manage as dj_manage, create_superuser as dj_create_superuser
from ..django.utils import put_settings
from ..settings import PROJECT_NAME, PROJECT_USER, PROJECT_GROUP, WEBSERVER_USER, PATH_PYTHON, \
    PATH_REMOTE_PROJECT_BASE, GIT_REPO, PATH_REMOTE_PROJECT, PATH_TEMP, PATH_LOCAL_PROJECT_BASE, GIT_REPO_EXTENDED, \
    PATH_GIT_ROOT
from ..sys import apt, venv, fs, users, pip, git, nginx, uwsgi, utils, pg

__all__ = ['update', 'dump', 'bootstrap', 'log_debug']

@task
def update(deep=False):
    """Updates remotes files using a remote repository."""
    git.pull(PATH_GIT_ROOT)

    if deep:
        dj_manage(['migrate', 'collectstatic --noinput'])

    uwsgi.reload_touch()


@task
def dump():
    """Dumps remote project directories and DB."""

    date_str = datetime.now().strftime('%Y-%m-%dT%H%M')
    dump_basename = '%s-%s_dump' % (date_str, PROJECT_NAME)
    path_dump = path.join(PATH_TEMP, dump_basename)

    fs.mkdir(path_dump, use_sudo=False)

    fs.gzip_dir(
        path.join(PATH_REMOTE_PROJECT, 'data', 'media'),
        path.join(path_dump, 'media'))

    pg.dump(PROJECT_NAME, path_dump)

    path_dump_arch = fs.gzip_dir(path_dump, path.join(PATH_TEMP, dump_basename))

    path_dump_local = path.join(PATH_LOCAL_PROJECT_BASE, 'dumps')

    try:
        makedirs(path_dump_local)
    except OSError:
        pass  # Already exists.

    get(path_dump_arch, local_path=path_dump_local)

    fs.rm(path_dump)
    fs.rm(path_dump_arch)


@task
def bootstrap():
    """Bootstraps a remote for your project."""
    users.create(PROJECT_USER)
    users.add_to_group(WEBSERVER_USER, PROJECT_GROUP)

    apt.bootstrap()

    fs.create_dir(PATH_REMOTE_PROJECT_BASE)

    if exists(path.join(PATH_REMOTE_PROJECT, '.git')):
        update()
    else:
        git.clone(PATH_REMOTE_PROJECT_BASE, GIT_REPO, '.' if GIT_REPO_EXTENDED else PROJECT_NAME)

    venv.create(PATH_PYTHON)

    pip.install(package='.', editable=True)
    pip.install(from_req=True)

    project_fs.upload_configs()
    put_settings(reload_uwsgi=False)

    pg.bootstrap()
    nginx.bootstrap()
    uwsgi.bootstrap()

    dj_migrate()
    dj_create_superuser()

    utils.reboot()


@task
def log_debug():
    """Tails project debug log from temporary directory."""
    fs.tail('/tmp/%s_debug.log' % PROJECT_NAME)
