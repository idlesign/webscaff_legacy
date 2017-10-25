from fabric.api import task, sudo, settings, run
from os import path

from .fs import append_to_file, tail, make_tmp_file
from ..settings import PROJECT_NAME, NAME_CONFIGS_DIR, PROJECT_USER
from ..utils import get_symlink_command, get_paths

__all__ = [
    'restart', 'reload', 'psql', 'sizes', 'reindex', 'get_version', 'log_main',
    'dump', 'bootstrap']

@task
def restart():
    """Restarts PostgreSQL."""
    sudo('service postgresql restart')


@task
def reload():
    """Reloads PostgreSQL."""
    sudo('service postgresql reload')


@task
def psql(command=None):
    """Launches psql command line utility."""
    command = command or ''
    if command:
        command = ' -%s "%s"' % ('f' if '/' in command else 'c', command)

    sudo('psql%s' % command, user=PROJECT_USER)


@task
def sizes(limit=10):
    """Launches psql command to output top n table sizes."""
    command = '''
    SELECT
        name AS "Table",
        pg_size_pretty(size_data) AS "Size Data",
        pg_size_pretty(size_idx) AS "Size Indexes",
        pg_size_pretty(size_total) AS "Size Total"

    FROM (

        SELECT
            name,
            pg_table_size(path) AS size_data,
            pg_indexes_size(path) AS size_idx,
            pg_total_relation_size(path) AS size_total

        FROM (
            SELECT
              ('"' || table_schema || '"."' || table_name || '"') AS path,
              (table_schema || '.' || table_name) AS name
            FROM information_schema.tables
        ) AS tables
        ORDER BY size_total DESC

    ) AS pretty_sizes LIMIT %s;
    ''' % limit
    command = command.replace('    ', '')
    command = make_tmp_file(command)
    psql(command)


@task
def reindex(table):
    """Launches psql command to reindex given table.

    Useful to reclaim space from bloated indexes.

    """
    psql('REINDEX TABLE %s' % table)


@task
def get_version():
    """Returns a list with PostgreSQL version number."""
    version = run('pg_config --version')
    version = version.split(' ')[-1].split('.')
    print('PostgreSQL version: %s' % version)
    return version


@task
def log_main():
    """Tails PostgreSQL log."""
    tail('/var/log/postgresql/postgresql-%s-main.log' % '.'.join(get_version()[:2]))


@task
def dump(db_name, target_dir):
    """Dumps DB by name into target directory."""
    target_path = path.join(target_dir, 'db.sql')
    run('pg_dump %s > %s' % (db_name, target_path))
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
    append_to_file('"include = \'%s\'"' % target_name, path_remote_base_config)

    # Create user and db.
    with settings(sudo_user='postgres'):
        sudo('createdb %s' % PROJECT_NAME)
        sudo('createuser -P %s' % PROJECT_NAME)
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (PROJECT_NAME, PROJECT_NAME))
