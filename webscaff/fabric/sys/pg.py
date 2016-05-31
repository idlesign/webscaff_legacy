from os import path

from fabric.api import task, sudo, settings, run

from ..settings import PROJECT_NAME, NAME_CONFIGS_DIR
from ..utils import get_symlink_command, get_paths


@task
def restart():
    """Restarts PostgreSQL."""
    sudo('service postgresql restart')


@task
def reload():
    """Reloads PostgreSQL."""
    sudo('service postgresql reload')


@task
def get_version():
    """Returns a list with PostgreSQL version number."""
    version = run('pg_config --version')
    version = version.split(' ')[-1].split('.')
    print('PostgreSQL version: %s' % version)
    return version


@task
def dump(db_name, target_dir):
    """Dumps DB by name into target directory."""
    target_path = path.join(target_dir, 'db.sql')
    sudo('pg_dump %s > %s' % (db_name, target_path))
    return target_path


@task
def bootstrap():
    """Bootstraps PostgreSQL for the project."""
    version = '.'.join(get_version()[:-1])

    path_pg_confs = '/etc/postgresql/%s/main/' % version
    path_remote_base_config = path.join(path_pg_confs, 'postgresql.conf')
    target_name = '%s.conf' % PROJECT_NAME

    path_pg_config_remote = path.join(get_paths(NAME_CONFIGS_DIR)[1], 'postgres.conf')
    sudo(get_symlink_command(path_pg_config_remote, path.join(path_pg_confs, target_name)))

    # Append into main config an include line.
    sudo('echo "include = \'%s\'" >> %s' % (target_name, path_remote_base_config))

    # Create user and db.
    with settings(sudo_user='postgres'):
        sudo('createdb %s' % PROJECT_NAME)
        sudo('createuser -P %s' % PROJECT_NAME)
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (PROJECT_NAME, PROJECT_NAME))
