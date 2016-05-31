from os import path, makedirs
from datetime import datetime

from fabric.api import task, get

from ..sys.apt import bootstrap as apt_bootstrap
from ..sys.venv import create as venv_create
from ..sys.fs import create_dir as fs_create_dir, mkdir as fs_mkdir, gzip_dir as fs_gzip_dir, tail as fs_tail, \
    rm as fs_rm
from ..sys.users import add_to_group as users_add_to_group, add_to_sudoers as users_add_to_sudoers
from ..sys.pip import install as pip_install
from ..sys.pg import bootstrap as pg_bootstrap, dump as pg_dump
from ..sys.git import clone as git_clone, pull as git_pull
from ..sys.nginx import bootstrap as nginx_bootstrap
from ..sys.uwsgi import bootstrap as uwsgi_bootstrap,  reload_touch as uwsgi_reload_touch
from ..sys.utils import reboot
from ..django.utils import put as dj_put_settings
from ..django.manage import manage as dj_manage, migrate as dj_migrate, create_superuser as dj_create_superuser
from ..settings import PROJECT_NAME, PROJECT_USER, PROJECT_GROUP, WEBSERVER_USER, PATH_PYTHON, \
    PATH_REMOTE_PROJECT_BASE, GIT_REPO, PATH_REMOTE_PROJECT, PATH_TEMP, PATH_LOCAL_PROJECT_BASE

from .fs import upload_configs as project_upload_configs


@task(default=True)
def update(deep=False):
    """Updates remotes files using a remote repository."""
    git_pull(PATH_REMOTE_PROJECT)

    if deep:
        dj_manage(['migrate', 'collectstatic --noinput'])

    uwsgi_reload_touch()


@task
def dump():
    """Dumps remote project directories and DB."""

    date_str = datetime.now().strftime('%Y-%m-%dT%H%M')
    dump_basename = '%s-%s_dump' % (date_str, PROJECT_NAME)
    path_dump = path.join(PATH_TEMP, dump_basename)

    fs_mkdir(path_dump, use_sudo=False)

    fs_gzip_dir(
        path.join(PATH_REMOTE_PROJECT, 'data', 'media'),
        path.join(path_dump, 'media'))

    pg_dump(PROJECT_NAME, path_dump)

    path_dump_arch = fs_gzip_dir(path_dump, path.join(PATH_TEMP, dump_basename))

    path_dump_local = path.join(PATH_LOCAL_PROJECT_BASE, 'dumps')

    try:
        makedirs(path_dump_local)
    except OSError:
        pass  # Already exists.

    get(path_dump_arch, local_path=path_dump_local)

    fs_rm(path_dump)
    fs_rm(path_dump_arch)


@task
def pre_bootstrap():
    """Preliminary preparation to bootstrap our machine for our project."""
    users_add_to_sudoers(PROJECT_USER)
    reboot()


@task
def bootstrap():
    """Bootstraps a remote for a project.

    Should be run after `pre_bootstrap` task.

    """
    apt_bootstrap()
    venv_create(PATH_PYTHON)
    fs_create_dir(PATH_REMOTE_PROJECT_BASE)
    git_clone(PATH_REMOTE_PROJECT_BASE, GIT_REPO, PROJECT_NAME)
    pip_install(from_req=True)
    dj_put_settings()
    project_upload_configs()
    pg_bootstrap()
    nginx_bootstrap()
    dj_migrate()
    dj_create_superuser()
    uwsgi_bootstrap()
    users_add_to_group(WEBSERVER_USER, PROJECT_GROUP)
    update(deep=True)


@task
def show_log():
    """Tails project debug log from temporary directory."""
    fs_tail('/tmp/%s_debug.log' % PROJECT_NAME)
