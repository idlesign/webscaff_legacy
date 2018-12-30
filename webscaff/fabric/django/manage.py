from os import path

from fabric.api import task, get, put, cd, sudo, run, env

from ..settings import PROJECT_NAME, PATH_TEMP, PATH_REMOTE_PROJECT, WEBSERVER_USER
from ..sys.fs import rm, gzip_dir
from ..sys.venv import venv

__all__ = [
    'manage', 'migrate', 'create_superuser', 'loaddata', 'dumpdata']


@task
def manage(cmd, use_sudo=1):
    """Runs Django manage command(s).

    :param str|list cmd:
    :param bool use_sudo:

    """
    if not isinstance(cmd, list):
        cmd = [cmd]

    use_sudo = int(use_sudo)
    func = sudo if use_sudo else run

    with venv():
        with cd(PATH_REMOTE_PROJECT):
            for c in cmd:
                user = env.sudo_user
                env.sudo_user = WEBSERVER_USER

                try:
                    func('python manage.py %s' % c)

                except:
                    env.sudo_user = user

@task
def migrate():
    """Runs Django manage command for project to launch migrations."""
    manage('migrate')


@task
def create_superuser():
    """Runs Django manage command for project to create a superuser."""
    manage('createsuperuser')


@task
def loaddata(filename):
    """Runs Django manage command for project to load fixture data.

    :param filename: Fixture filename.

    """
    filename = path.abspath(filename)
    path_remote = path.join(PATH_TEMP, path.basename(filename))
    put(filename, path_remote)

    manage('loaddata %s --ignorenonexistent ' % path_remote)

    rm(path_remote)


@task
def dumpdata(app_name):
    """Runs Django manage command for project to dump data.

    :param app_name: Application name with optional model name after a dot
        E.g. apps or apps.discussion

    """
    dump_basename = '%s_%s_dump' % (PROJECT_NAME, app_name)
    dump_basename_json = '%s.json' % dump_basename
    dump_basename_archive = '%s.tar.gz' % dump_basename

    path_json = path.join(PATH_TEMP, dump_basename_json)
    path_archive = path.join(PATH_TEMP, dump_basename_archive)

    manage('dumpdata %s --indent 4 > %s' % (app_name, path_json))

    gzip_dir(dump_basename_json, path_archive, change_dir=PATH_TEMP)
    get(path_archive, local_path=path.abspath(path.dirname(__file__)))

    rm(path_json)
    rm(path_archive)
