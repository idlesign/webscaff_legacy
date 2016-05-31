from os import path

from fabric.api import task, sudo, run

from ..settings import PROJECT_NAME, PATH_REMOTE_PROJECT_BASE, NAME_CONFIGS_DIR
from ..utils import get_symlink_command, get_paths
from .fs import tail


UWSGI_APPS_PATH = '/etc/uwsgi/apps-enabled/'
UWSGI_INI_FILEPATH = path.join(UWSGI_APPS_PATH, '%s.ini' % PROJECT_NAME)
UWSGI_PID_FILEPATH = path.join(PATH_REMOTE_PROJECT_BASE, '%s.pid' % PROJECT_NAME)
UWSGI_TOUCH_RELOAD_FILE = 'reload'
UWSGI_TOUCH_RELOAD_FILEPATH = path.join(PATH_REMOTE_PROJECT_BASE, UWSGI_TOUCH_RELOAD_FILE)


@task
def log():
    """Tails uWSGI log."""
    tail('/var/log/uwsgi/app/%s.log' % PROJECT_NAME)


@task
def start():
    """Starts uWSGI using ini file for project."""
    sudo('service uwsgi start %s' % PROJECT_NAME)


@task
def stop():
    """Stops uWSGI."""
    sudo('service uwsgi stop %s' % PROJECT_NAME)


@task
def reload(force=False):
    """Reloads uWSGI."""
    force_clause = ''
    if force:
        force_clause = 'force-'
    sudo('service uwsgi %sreload %s' % (force_clause, PROJECT_NAME))


@task
def reload_touch():
    """Touches a file to initiate uwsgi reload procedure."""
    run('touch %s' % UWSGI_TOUCH_RELOAD_FILEPATH)


@task
def bootstrap():
    """Bootstraps uWSGI for the project."""
    uwsgi_config = path.join(get_paths(NAME_CONFIGS_DIR)[1], 'uwsgi.ini')
    sudo(get_symlink_command(uwsgi_config, UWSGI_INI_FILEPATH))

    start()
