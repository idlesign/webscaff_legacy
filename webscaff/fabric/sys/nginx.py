from os import path
from contextlib import contextmanager

from fabric.api import task, sudo, run

from ..settings import PATH_REMOTE_PROJECT_BASE, PROJECT_NAME, NAME_CONFIGS_DIR
from ..utils import get_symlink_command, get_paths
from .fs import tail, rm


NGINX_MAINTENANCE_FILEPATH = path.join(PATH_REMOTE_PROJECT_BASE, '503')


@contextmanager
def stopped():
    """Temporarily stops Nginx."""
    sudo('service nginx stop')
    try:
        yield

    finally:
        sudo('service nginx start')


@contextmanager
def maintenance():
    """Temporarily puts Nginx into maintenance mode."""
    maintenance_on()
    try:
        yield

    finally:
        maintenance_off()


@task
def restart():
    """Restarts nginx."""
    sudo('service nginx restart')


@task
def restart():
    """Restarts nginx."""
    sudo('service nginx restart')


@task
def reload():
    """Reloads nginx."""
    sudo('service nginx reload')


@task
def log_access():
    """Tails nginx access log."""
    # todo use project prefix
    tail('/var/log/nginx/access.log')


@task
def log_error():
    """Tails nginx error log."""
    # todo use project prefix
    tail('/var/log/nginx/error.log')


@task
def maintenance_on():
    """Turns on maintenance mode."""
    run('touch %s' % NGINX_MAINTENANCE_FILEPATH)


@task
def maintenance_off():
    """Turns off maintenance mode."""
    rm(NGINX_MAINTENANCE_FILEPATH, use_local=False)


@task
def bootstrap():
    """Bootstraps nginx for the project."""
    nginx_config = path.join(get_paths(NAME_CONFIGS_DIR)[1], 'nginx.conf')
    path_sites = '/etc/nginx/sites-enabled/'

    rm(path.join(path_sites, 'default'), use_local=False)
    sudo(get_symlink_command(nginx_config, '%s%s.conf' % (path_sites, PROJECT_NAME)))

    reload()
