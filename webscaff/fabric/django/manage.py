from os import path

from fabric.api import task, run, get, put

from ..sys.venv import venv
from ..sys.fs import rm, gzip_dir
from ..settings import PROJECT_NAME, PATH_TEMP


@task
def manage(cmd):
    """Runs Django manage command(s).

    :param str|list cmd:

    """
    if not isinstance(cmd, list):
        cmd = [cmd]

    with venv():
        for c in cmd:
            run('python manage.py %s' % c)


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
